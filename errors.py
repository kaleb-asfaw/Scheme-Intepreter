import sys 

sys.setrecursionlimit(100000)

#############################
# Scheme-related Exceptions #
#############################

class Error(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SyntaxError(Error):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class NameError(Error):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class EvaluationError(Error):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass