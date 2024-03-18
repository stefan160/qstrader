"""
Interface to a live or backtested trading session.
"""

from abc import ABCMeta, abstractmethod


class TradingSession:
    """
    Interface to a live or backtested trading session.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self) -> None:
        """
        Run the session.
        """
        raise NotImplementedError("Should implement run()")
