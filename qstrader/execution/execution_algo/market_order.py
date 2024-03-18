"""market_order.py"""

from typing import List
import pandas as pd
from qstrader.execution.execution_algo.execution_algo import ExecutionAlgorithm
from qstrader.execution.order import Order


# pylint: disable=too-few-public-methods


class MarketOrderExecutionAlgorithm(ExecutionAlgorithm):
    """
    Simple execution algorithm that creates an unmodified list
    of market Orders from the rebalance Orders.
    """

    def __call__(self, dt: pd.Timestamp, initial_orders: List[Order]) -> List[Order]:
        """
        Simply returns the initial orders list in a 'pass through' manner.

        Parameters
        ----------
        dt : `pd.Timestamp`
            The current time used to populate the Order instances.
        rebalance_orders : `list[Order]`
            The list of rebalance orders to execute.

        Returns
        -------
        `list[Order]`
            The final list of orders to send to the Broker to be executed.
        """
        return initial_orders
