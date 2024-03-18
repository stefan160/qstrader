""" Abstract Rebalance Class. """

from abc import ABCMeta, abstractmethod


class Rebalance(object):
    """
    Interface to a generic list of system logic and
    trade order rebalance timestamps.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def _generate_rebalances(self):
        raise NotImplementedError("Should implement _generate_rebalances()")
