""" Universe Meta Class. """

from abc import ABCMeta, abstractmethod


class Universe:
    """
    Interface specification for an Asset Universe.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_assets(self, dt):
        """get assets"""
        raise NotImplementedError("Should implement get_assets()")
