class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    pass


class FileReadError(Error):
    """
    Exception raised when an input file cannot be read.
    """

    def __init__(self, filepath, message):
        self.filepath = filepath
        self.message = message
