# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Code used to fit pipeline."""
import datetime
import json
import logging
import math
from typing import Any, Dict, Optional

import numpy as np
import sklearn.pipeline

import azureml.automl.core.inference as inference
from automl.client.core.common import constants, logging_utilities, utilities
from automl.client.core.common.datasets import DatasetBase
from automl.client.core.common.exceptions import ClientException, ErrorTypes
from automl.client.core.common.limit_function_call_exceptions import TimeoutException
from azureml.automl.core.cpu_utilities import _get_num_physical_cpu_cores_model_explanations
from . import package_utilities, pipeline_run_helper, training_utilities
from .automl_base_settings import AutoMLBaseSettings
from .automl_pipeline import AutoMLPipeline
from .automl_run_context import AutoMLAbstractRunContext
from .data_context import TransformedDataContext
from .ensemble_base import EnsembleBase
from .fit_output import FitOutput
from .onnx_convert import OnnxConverter
from .systemusage_telemetry import SystemResourceUsageTelemetryFactory


class FitPipelineComponentName:
    """Constants for the FitPipeline Component names."""

    PREPRARE_DATA = "PrepareData"
    COMPLETE_RUN = "CompleteRun"


def fit_pipeline(automl_pipeline: AutoMLPipeline,
                 automl_settings: AutoMLBaseSettings,
                 automl_run_context: AutoMLAbstractRunContext,
                 fit_iteration_parameters_dict: Optional[Dict[str, Any]] = None,
                 remote: bool = True,
                 logger: logging.Logger = logging_utilities.get_logger(),
                 transformed_data_context: Optional[TransformedDataContext] = None,
                 dataset: Optional[DatasetBase] = None,
                 elapsed_time: Optional[int] = None,
                 onnx_cvt: Optional[OnnxConverter] = None) -> FitOutput:
    """
    Run a single iteration of an AutoML experiment.

    This method is automatically called during a regular AutoML
    experiment. fit_pipeline will evaluate the pipeline for this iteration, fit the pipeline with the provided data,
    calculate the various metrics relevant for this experiment, and log all the results in the specified AzureML Run's
    history.

    :param automl_pipeline: AutoMLPipeline object containing pipeline id and serialized script.
    :param automl_settings: User settings specified when creating AutoMLConfig.
    :param automl_run_context: child run context object
    :param fit_iteration_parameters_dict: Remaining data specific parameters for fit such as 'x_raw_column_names'.
    :param remote: flag whether this is a remote run or local run.
    :param logger: logger for info/error messages.
    :param transformed_data_context: TransformedDataContext, contains X,y and other transformed data.
    :param dataset: Containing X, y and other transformed data info.
    :param elapsed_time: How long this experiment has already taken in minutes
    :param onnx_cvt: The onnx converter.
    :return: AzureML Run Properties for this child run
    """
    logging_utilities.log_system_info(logger, prefix_message="[RunId:{}]".format(automl_run_context.run_id))

    start_time = datetime.datetime.now()

    # log all dependencies
    all_dependencies = package_utilities._all_dependencies()
    logger.info("All versions str:\n{}".format(json.dumps(all_dependencies)))

    telemetry_logger = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(
        logger, interval=10)

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Starting fit_pipeline]".format(automl_run_context.run_id),
        is_sending_telemetry=automl_settings.send_telemetry
    )

    logging_utilities.log_system_info(logger, prefix_message="[RunId:{}]".format(automl_run_context.run_id))

    fit_output = FitOutput(automl_settings, automl_pipeline)

    logger.info("Using child run {0}".format(automl_run_context.run_id))

    if (dataset is None and transformed_data_context is None and fit_iteration_parameters_dict is None):
        raise ValueError("Can't create a ClientDataset without transformed_data_context or "
                         "fit_iteration_parameters_dict")

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Before preprocess]".format(automl_run_context.run_id),
        is_sending_telemetry=automl_settings.send_telemetry
    )

    try:
        if dataset is None:
            if transformed_data_context is not None:
                logger.info("Generating ClientDataset from transformed data.")
                dataset = training_utilities.init_client_dataset(transformed_data_context=transformed_data_context,
                                                                 cache_store=transformed_data_context.cache_store,
                                                                 automl_settings=automl_settings,
                                                                 remote=remote,
                                                                 keep_in_memory=False)

            else:
                assert fit_iteration_parameters_dict is not None, \
                    "transformed_data_context and fit_iteration_parameters_dict both are None"
                logger.info("Generating ClientDataset from fit iteration params dictionary.")
                dataset = training_utilities.init_client_dataset_from_fit_iteration_params(
                    fit_iteration_parameters_dict=fit_iteration_parameters_dict,
                    automl_settings=automl_settings,
                    remote=remote,
                    keep_in_memory=False
                )

        assert dataset is not None, "Can't continue without a dataset object"

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][Before executing pipeline]".format(automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        logger.info(
            "Start executing pipeline {0}.".format(
                logging_utilities.remove_blacklisted_logging_keys_from_json_str(
                    automl_pipeline.pipeline_script
                )
            )
        )
        logger.info("Running with the following AutoML settings:\n{}".format(
            automl_settings._format_selective(logging_utilities.BLACKLISTED_LOGGING_KEYS)))

        try:
            iteration_timeout_min = _check_iteration_time(
                automl_settings, FitPipelineComponentName.PREPRARE_DATA, start_time, logger, elapsed_time
            )

            pipeline_run_output = pipeline_run_helper.run_pipeline(automl_settings,
                                                                   automl_pipeline,
                                                                   automl_run_context,
                                                                   iteration_timeout_min,
                                                                   dataset,
                                                                   logger,
                                                                   remote)
            fit_output.record_pipeline_results(pipeline_run_output)
        except Exception as e:
            fit_output.add_error('fit', e)
            raise

        # Check the result after the fit step. If the primary metric is not available, an exception will raise here.
        _check_fit_output_result(fit_output)

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][After executing pipeline]".format(
                automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )

        logger.info("Pipeline execution finished with a score of {0}".format(fit_output.score))
        logger.info("Start logging metrics for child run.")
        with logging_utilities.log_activity(logger,
                                            activity_name=constants.TelemetryConstants.METRIC_AND_SAVE_MODEL_NAME,
                                            custom_dimensions={'run_id': automl_run_context.run_id}):
            with automl_run_context.get_run() as run:
                # save versions to artifacts
                try:
                    automl_run_context.save_str_output(
                        json.dumps(all_dependencies, indent=4), constants.DEPENDENCIES_PATH)
                except Exception:
                    logger.warning("Failed uploading version file to artifact services.")

                # save conda environment file into artifacts
                try:
                    automl_run_context.save_str_output(
                        inference._create_conda_env_file(), constants.CONDA_ENV_FILE_PATH)
                    run.add_properties(
                        {inference.AutoMLInferenceArtifactIDs.CondaEnvDataLocation:
                            automl_run_context._get_atrifact_id(constants.CONDA_ENV_FILE_PATH)})
                except Exception as e:
                    logger.warning("Failed to create conda environment file. Error seen is: " + str(e))

                # save scoring file into artifacts
                try:
                    if dataset.get_raw_data_type() is not None:
                        scoring_file_str, model_name = inference._get_scoring_file(
                            if_pandas_type=(dataset.get_raw_data_type() == inference.PandasParameterType),
                            input_sample_str=dataset._get_raw_data_snapshot_str(),
                            automl_run_id="{}".format(run.id),
                            is_forecasting=automl_settings.is_timeseries)
                        automl_run_context.save_str_output(scoring_file_str, constants.SCORING_FILE_PATH)
                        run.add_properties({inference.AutoMLInferenceArtifactIDs.ModelName: model_name})
                        run.add_properties(
                            {inference.AutoMLInferenceArtifactIDs.ScoringDataLocation:
                                automl_run_context._get_atrifact_id(constants.SCORING_FILE_PATH)})
                    else:
                        logger.warning("Failed to score inference file: dataset's raw_data_type is not set.")
                except Exception as e:
                    logger.warning("Failed to score inference file. Error seen is: " + str(e))

                # save model as a pickle file into artifacts
                automl_run_context.save_model_output(fit_output.fitted_pipeline, constants.MODEL_PATH)
                run.add_properties(
                    {inference.AutoMLInferenceArtifactIDs.ModelDataLocation:
                        automl_run_context._get_atrifact_id(constants.MODEL_PATH)})

                if onnx_cvt is not None:
                    # Convert to ONNX, after we got this valid fitted_pipeline.
                    # Ingect the exp name, run id data into the onnx model.
                    onnx_mdl_name = 'AutoML_ONNX_Model_[{}]'.format(run.id)
                    exp_name = ''
                    if hasattr(run, 'experiment') and run.experiment is not None and \
                            hasattr(run.experiment, 'name'):
                        exp_name = run.experiment.name
                    onnx_mdl_desc = {
                        'AutoMLSDKVer': onnx_cvt.producer_version,
                        'ExperimentName': exp_name,
                        'RunId': run.id,
                        'PipeId': automl_pipeline.pipeline_id
                    }
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][Start ONNX Convert in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                    with logging_utilities.log_activity(logger,
                                                        activity_name=constants.TelemetryConstants.ONNX_CONVERSION,
                                                        custom_dimensions={'run_id': automl_run_context.run_id}):
                        onnx_model, _ = onnx_cvt.convert(raw_model=fit_output.fitted_pipeline,
                                                         model_name=onnx_mdl_name,
                                                         model_desc=onnx_mdl_desc
                                                         )
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][End ONNX Convert in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                    # If user indicates using ONNX compatible models, save the ONNX model.
                    if automl_settings.enable_onnx_compatible_models and onnx_model is not None:
                        automl_run_context.save_onnx_model_output(onnx_model, constants.MODEL_PATH_ONNX)
                        fit_output.set_onnx_model(onnx_model)
                        onnx_resource = onnx_cvt.get_converted_onnx_model_resource()
                        fit_output.set_onnx_model_resource(onnx_resource)
                        if onnx_resource:
                            automl_run_context.save_onnx_model_resource(
                                onnx_resource, constants.MODEL_RESOURCE_PATH_ONNX)

                need_CV_trained_models = automl_settings.enable_ensembling or \
                    (hasattr(automl_settings, "enable_stack_ensembling") and
                     automl_settings.enable_stack_ensembling)
                if need_CV_trained_models and \
                        fit_output.fitted_pipelines_train != constants.Defaults.INVALID_PIPELINE_OBJECT:
                    # we need to persist the partially trained fitted models as well
                    # they will be used for computing the scores during ensemble hill climbing
                    automl_run_context.save_model_output(
                        fit_output.fitted_pipelines_train, constants.MODEL_PATH_TRAIN)

                _log_metrics(run, fit_output.scores, logger)
                _log_metrics_info(fit_output.scores, logger, pipeline_id=fit_output.pipeline_id,
                                  run_id=automl_run_context.run_id)

                run.complete()

                # check to see if model_explainability set or not
                remaining_time = _check_iteration_time(
                    automl_settings, FitPipelineComponentName.COMPLETE_RUN, start_time,
                    logger, elapsed_time,
                    raise_exception=False
                )
                if automl_settings.model_explainability and (
                        automl_settings.iteration_timeout_minutes is None or remaining_time is None or
                        remaining_time > automl_settings.iteration_timeout_minutes / 2):
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][Start model explain in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                    try:
                        with dataset.open_dataset():
                            _explain_model_in_fit(run, fit_output.fitted_pipeline, dataset,
                                                  automl_settings.max_cores_per_iteration, logger)
                    except Exception as e:
                        fit_output.add_error('model_explanation', e, is_critical=False)
                        logging_utilities.log_traceback(e, logger, is_critical=False)
                        logger.warning(
                            "[RunId:{}]Failed model explanation in fit pipeline. Error Message: {}.".format(
                                run.id, e)
                        )
                    telemetry_logger.send_usage_telemetry_log(
                        prefix_message="[RunId:{}][End model explain in fit pipeline]".format(
                            automl_run_context.run_id),
                        is_sending_telemetry=automl_settings.send_telemetry
                    )
                elif automl_settings.model_explainability:
                    # model_explain is enabled but not have enought time.
                    logger.warning("Remaining time is not enough for model explanation.")
                    print("Remaining time is not enough for model explanation. "
                          "Please use explain_model() to generate explanations for this iteration..")

    except Exception as e:
        if 'fit' not in fit_output.errors:
            fit_output.add_error('overall', e)
        with automl_run_context.get_run() as run:
            logging_utilities.log_traceback(e, logger)
            run.fail(
                error_details=utilities.build_run_failure_error_detail(e), error_code=utilities.get_error_code(e))
    except KeyboardInterrupt:
        with automl_run_context.get_run() as run:
            run.fail(error_details="User cancelled the run.", error_code=ErrorTypes.User)
    finally:
        # TODO: remove once backend can handle nulls
        fit_output_sanitized = fit_output.get_sanitized_output_dict()

        with automl_run_context.get_run() as run:
            run.set_tags(fit_output_sanitized)
            # TODO: move to tags once JOS is updated
            # Check to see if any property already exists, and exclude if already present
            fit_output_sanitized.update({
                'dependencies_versions': json.dumps(package_utilities.get_sdk_dependencies())
            })
            existing_properties = run.get_properties()
            run.add_properties({
                k: fit_output_sanitized[k]
                for k in fit_output_sanitized
                if k not in existing_properties
            })

        telemetry_logger.send_usage_telemetry_log(
            prefix_message="[RunId:{}][End fit_pipeline]".format(automl_run_context.run_id),
            is_sending_telemetry=automl_settings.send_telemetry
        )
        telemetry_logger.stop()
        return fit_output


def _extract_data(fit_iteration_parameters_dict=None, transformed_data_context=None):
    # if transformed_data_context is not None, then use data in transformed_data_context. If None, then to
    # use data in fit_iteration_parameters_dict.
    if transformed_data_context is not None:
        X = transformed_data_context.X
        y = transformed_data_context.y
        X_valid = transformed_data_context.X_valid
        y_valid = transformed_data_context.y_valid
        sample_weight = transformed_data_context.sample_weight
        sample_weight_valid = transformed_data_context.sample_weight_valid
        cv_splits_indices = transformed_data_context.cv_splits_indices
        x_raw_column_names = transformed_data_context.x_raw_column_names
    elif fit_iteration_parameters_dict is not None:
        X = fit_iteration_parameters_dict.get('X')
        y = fit_iteration_parameters_dict.get('y')
        X_valid = fit_iteration_parameters_dict.get('X_valid')
        y_valid = fit_iteration_parameters_dict.get('y_valid')
        sample_weight = fit_iteration_parameters_dict.get('sample_weight')
        sample_weight_valid = fit_iteration_parameters_dict.get('sample_weight_valid')
        cv_splits_indices = fit_iteration_parameters_dict.get('cv_splits_indices')
        x_raw_column_names = fit_iteration_parameters_dict.get('x_raw_column_names')
    else:
        raise ValueError('Either a transformed data context or parameters dict is required.')
    return X, y, X_valid, y_valid, sample_weight, sample_weight_valid, cv_splits_indices, x_raw_column_names


def _check_iteration_time(automl_settings: AutoMLBaseSettings,
                          component_name: str,
                          start_time: datetime.datetime,
                          logger: logging.Logger,
                          elapsed_time: Optional[int] = None,
                          raise_exception: Optional[bool] = True) -> Optional[int]:
    iteration_timeout_min = automl_settings.iteration_timeout_minutes
    running_min = (datetime.datetime.now() - start_time).total_seconds() / 60.
    logger.info("Component {} finished after {} minutes.".format(component_name, running_min))
    if iteration_timeout_min is not None:
        iteration_timeout_min = math.ceil(iteration_timeout_min - running_min)
    if automl_settings.experiment_timeout_minutes is not None and elapsed_time is not None:
        experiment_max_time_min = int(automl_settings.experiment_timeout_minutes) - elapsed_time
        if iteration_timeout_min is None or experiment_max_time_min < iteration_timeout_min:
            iteration_timeout_min = experiment_max_time_min

    if iteration_timeout_min and iteration_timeout_min <= 0 and raise_exception:
        if automl_settings.experiment_timeout_minutes is not None:
            raise TimeoutException('Timeout reached after running for {} minutes, skipping iteration. Please '
                                   'consider increasing experiment_timeout_minutes or iteration_timeout_minutes.'.
                                   format(elapsed_time))
        else:
            raise TimeoutException('Timeout reached after running iteration for {} minutes, skipping iteration. '
                                   'Please consider increasing iteration_timeout_minutes.'.
                                   format(running_min))

    return iteration_timeout_min


def _log_metrics_info(scores, logger, pipeline_id=None, run_id=None):
    reduced_scores = _get_reduced_scores(scores)
    log_fmt = "run_id:{}, pipeline_id:{},The following metrics have been logged for the child run: {}."
    logger.info(log_fmt.format(run_id, pipeline_id, reduced_scores))


def _get_reduced_scores(scores):
    reduced_scores = dict()
    for name, score in scores.items():
        is_score_NoneOrNumeric = score is None or isinstance(score, int) or isinstance(score, float)
        if name in constants.Metric.SCALAR_FULL_SET or is_score_NoneOrNumeric:
            reduced_scores[name] = score
        else:
            reduced_scores[name] = type(score)
    return reduced_scores


def _log_metrics(child_run, scores, logger):
    for name, score in scores.items():
        try:
            if name in constants.Metric.SCALAR_FULL_SET:
                child_run.log(name, score)
            elif name == constants.Metric.AccuracyTable:
                child_run.log_accuracy_table(name, score)
            elif name == constants.Metric.ConfusionMatrix:
                child_run.log_confusion_matrix(name, score)
            elif name == constants.Metric.Residuals:
                child_run.log_residuals(name, score)
            elif name == constants.Metric.PredictedTrue:
                child_run.log_predictions(name, score)
            # TODO support these schemas before logging them:
            # elif name == constants.Metric.ForecastResiduals:
            #     child_run.log_residuals(name, score)
            # elif name == constants.Metric.ForecastMAPE:
            #     child_run.log_mape(name, score)
            else:
                logger.warning(
                    "Did not recognize metric: {}. Will not log.".format(name))
        except Exception as e:
            logger.warning(
                "Failed to log the metric {} with value {}, exception {}".format(name, score, e))


def _explain_model_in_fit(child_run, pipeline, dataset, max_cores_per_iteration, logger):
    """
    Explain the model in the fit stage and store the explanation in child_run.

    :param child_run: the run to store information
    :type child_run: azureml.core.run.Run
    :param pipeline: the pipeline to explain
    :type pipeline: sklearn.pipeline.Pipeline
    :param dataset: Containing X, y and other transformed data info
    :type dataset: ClientDatasets
    :param max_cores_per_iteration: Number of cores on which surrogate model can run
    :type max_cores_per_iteration: int
    :param logger: logger for info/error messages.
    :return: None
    """
    from azureml.explain.model.mimic.mimic_explainer import MimicExplainer
    from azureml.explain.model.mimic.models.lightgbm_model import LGBMExplainableModel
    from azureml.explain.model._internal.explanation_client import ExplanationClient

    logger.info("[RunId:{}]Start model explanation in fit pipeline.".format(child_run.id))
    # Set the engineered/raw features information for model explanation
    columns = dataset.get_engineered_feature_names()

    # Convert columns from type ndarray to list
    if columns is not None and isinstance(columns, np.ndarray):
        columns = columns.tolist()

    # To explain the pipeline which should exclude datatransformer and laggingtransformer
    pipeline = EnsembleBase._transform_single_fitted_pipeline(pipeline)

    # Set the number of cores for LightGBM model
    explainable_model_args = {}
    explainable_model_args['n_jobs'] = _get_num_physical_cpu_cores_model_explanations(max_cores_per_iteration)
    logger.info("The number of core being set for explainable model is: " + str(explainable_model_args['n_jobs']))

    X, X_valid = (dataset.get_meta('X'), dataset.get_meta('X_valid'))
    class_labels = dataset.get_class_labels()
    y_transformer = dataset.get_y_transformer()
    if y_transformer is not None:
        class_labels = y_transformer.inverse_transform(class_labels)

    if training_utilities._is_sparse_matrix_int_type(X):
        logger.info("Integer type detected for X, need to upgrade to float type")
    if training_utilities._is_sparse_matrix_int_type(X_valid):
        logger.info("Integer type detected for X_valid, need to upgrade to float type")

    # If the training data is in integer format, then the data needs to reformated into float data
    # for LightGBM surrogate model. For different types of workloads, following needs to done:-
    # 1. If this is non-preprocessing/non-timeseries experiment then copy needs to be made via this
    #    conversion.
    # 2. If this is preprocessing/timeseries, then we should read from file cache and update the type
    #    in inplace. Currently we can't. TODO: Once the training data is read from the cache, then update
    #    the code below to change the type inplace.
    explainer_data_X = training_utilities._upgrade_sparse_matrix_type(X)
    explainer_data_X_valid = training_utilities._upgrade_sparse_matrix_type(X_valid)
    # Create the mimicexplainer
    explainer = MimicExplainer(
        pipeline, explainer_data_X, LGBMExplainableModel, features=columns, classes=class_labels,
        augment_data=False, explainable_model_args=explainable_model_args
    )

    if explainer_data_X_valid is None:
        explanation = explainer.explain_global(explainer_data_X)
    else:
        explanation = explainer.explain_global(explainer_data_X_valid)
    # Explain the model and save the explanation information to artifact
    # And don't display explain status bar
    client = ExplanationClient.from_run(child_run)
    client.upload_model_explanation(explanation, top_k=100)

    child_run.tag(constants.MODEL_EXPLANATION_TAG, 'True')

    logger.info("[RunId:{}]End model explanation in fit pipeline.".format(child_run.id))


def _check_fit_output_result(fit_output: FitOutput) -> None:
    """Check the run results."""
    if fit_output.score is None or np.isnan(fit_output.score) \
            or fit_output.score == constants.Defaults.DEFAULT_PIPELINE_SCORE:
        raise ClientException("Primary metric {} is not available.".format(fit_output.primary_metric))
