# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""A module that contains definitions of custom exception classes."""

from automl.client.core.common.exceptions import ErrorTypes


# TODO Rename this
class AzureMLForecastException(Exception):
    """Base exception class for all exceptions in the Azure ML Forecasting toolkit."""

    pass


class PipelineException(AzureMLForecastException):
    """
    Exception raised for errors in AzureMLForecastPipeline.

    Attributes:
        message: terse error message as defined in 'Messages' class of the
            'verify' module
        error_detail: optional, detailed error message

    """

    def __init__(self, message, error_detail=None):
        """Create a PipelineException."""
        if error_detail is not None:
            super().__init__("PipelineException: {0}, {1}".format(message, error_detail))
        else:
            super().__init__("PipelineException: {0}".format(message))


class TransformException(AzureMLForecastException):
    """
    Exception raised for errors in a transform class in the AzureML Forecasting SDK.

    Attributes:
        message: terse error message as defined in 'Messages' class of the 'verify' module
        error_detail: optional, detailed error message

    """

    def __init__(self, message, error_detail=None):
        """Create a TransformException."""
        if error_detail is not None:
            super().__init__("TransformException: {0}, {1}".format(message, error_detail))
        else:
            super().__init__("TransformException: {0}".format(message))


class TransformValueException(TransformException):
    """
    Exception raised for value errors in a transform class in the AzureML Forecasting SDK.

    :param message:
        terse error message as defined in 'Messages'
        class of the 'verify' module
    :type message: str

    :param error_detail: optional, detailed error message
    :type error_detail: str
    """

    def __init__(self, message, error_detail=None):
        """Create a TransformValueException."""
        if error_detail is not None:
            super().__init__("TransformValueException: {0}, {1}"
                             .format(message, error_detail))
        else:
            super().__init__("TransformValueException: {0}".format(message))


class TransformTypeException(TransformException):
    """
    Exception raised for type errors in a transform class in the AzureML Forecasting SDK.

    :param message:
        terse error message as defined in 'Messages'
        class of the 'verify' module
    :type message: str

    :param error_detail: optional, detailed error message
    :type error_detail: str
    """

    def __init__(self, message, error_detail=None):
        """Create a TransformTypeException."""
        if error_detail is not None:
            super().__init__("TransformTypeException: {0}, {1}"
                             .format(message, error_detail))
        else:
            super().__init__("TransformTypeException: {0}".format(message))


class NotTimeSeriesDataFrameException(AzureMLForecastException):
    """
    Exception raised if the data frame is not of TimeSeriesDataFrame.

    Attributes:
        message: terse error message as defined in 'Messages' class of the 'verify' module
        error_detail: optional, detailed error message

    """

    def __init__(self, message, error_detail=None):
        """Create a NotTimeSeriesDataFrameException."""
        if error_detail is not None:
            super().__init__("NotTimeSeriesDataFrameException: {0}, {1}".format(message, error_detail))
        else:
            super().__init__("NotTimeSeriesDataFrameException: {0}".format(message))


class NotSupportedException(AzureMLForecastException):
    """NotSupportedException."""

    def __init__(self, message, error_detail=None):
        """Create a NotSupportedException."""
        if error_detail is not None:
            super().__init__("NotSupportedException: {0}, {1}".format(message, error_detail))
        else:
            super().__init__("NotSupportedException: {0}".format(message))


class DataFrameTypeException(AzureMLForecastException):
    """DataFrameTypeException."""

    def __init__(self, message):
        """Create a DataFrameTypeException."""
        super().__init__("Data frame type is invalid. {0}".format(message))


class DataFrameValueException(AzureMLForecastException):
    """DataFrameValueException."""

    def __init__(self, message):
        """Create a DataFrameValueException."""
        super().__init__("Data frame value is invalid. {0}".format(message))


class DataFrameFrequencyException(AzureMLForecastException):
    """DataFrameFrequencyException."""

    def __init__(self, message):
        """Create a DataFrameFrequencyException."""
        super().__init__("Data frequency is invalid. {0}".format(message))


class DataFrameMissingColumnException(AzureMLForecastException):
    """DataFrameMissingColumnException."""

    def __init__(self, message):
        """Create a DataFrameMissingColumnException."""
        super().__init__("Data frame is missing a required column. {0}".format(message))


class DatetimeConversionException(AzureMLForecastException):
    """DatetimeConversionException."""

    def __init__(self, message):
        """Create a DateTimeConversionException."""
        super().__init__("Unable to do datetime conversion. {0}".format(message))


class DataFrameIncorrectFormatException(AzureMLForecastException):
    """DataFrameIncorrectFormatException."""

    def __init__(self, message, error_detail=None):
        """Create a DataFrameIncorrectFormatException."""
        if error_detail is not None:
            super().__init__("DataFrameIncorrectFormatException: {0}, {1}".format(message, error_detail))
        else:
            super().__init__("DataFrameIncorrectFormatException: {0}".format(message))


FORECASTING_USER_EXCEPTIONS = {
    NotSupportedException,
    DataFrameTypeException,
    DataFrameValueException,
    DataFrameMissingColumnException,
    DataFrameFrequencyException}


FORECASTING_CLIENT_EXCEPTIONS = {
    PipelineException,
    TransformException,
    TransformValueException,
    TransformTypeException,
    NotTimeSeriesDataFrameException
}


def classify_forecasting_exception(exception: AzureMLForecastException) -> str:
    """
    Classify the forecasting exceptions for the error type for the error classification.

    :param exception: an AzureMLForecastException need to be classified.
    :return: The error type of the exception.
    """
    if exception.__class__ in FORECASTING_USER_EXCEPTIONS:
        return ErrorTypes.User
    elif exception.__class__ in FORECASTING_CLIENT_EXCEPTIONS:
        return ErrorTypes.Client
    else:
        return ErrorTypes.Unclassified
