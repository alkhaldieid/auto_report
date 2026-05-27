"""Domain exceptions used by the command-line interface."""


class AutoReportError(Exception):
    """Base class for expected user-facing errors."""


class ConfigurationError(AutoReportError):
    """Raised when report configuration is invalid."""


class AssetNotFoundError(AutoReportError):
    """Raised when a required logo or cover asset is missing."""


class DateParseError(AutoReportError):
    """Raised when a date cannot be parsed from user input."""


class NoImagesFoundError(AutoReportError):
    """Raised when no reportable images are found."""


class LatexNotFoundError(AutoReportError):
    """Raised when XeLaTeX is required but not installed."""


class FontNotFoundError(AutoReportError):
    """Raised when a configured font is not available."""

