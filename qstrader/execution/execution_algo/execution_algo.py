"""execution_algo.py"""

from typing import List
from abc import ABCMeta, abstractmethod

import pandas as pd
from qstrader.execution.order import Order


# pylint: disable=too-few-public-methods


class ExecutionAlgorithm(object):
    """
    Callable which takes in a list of desired rebalance Orders
    and outputs a new Order list with a particular execution
    algorithm strategy.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, dt: pd.Timestamp, initial_orders: List[Order]):
        raise NotImplementedError("Should implement __call__()")
