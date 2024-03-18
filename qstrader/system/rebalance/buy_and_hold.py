""" Buy and Hold Rebalance Class. """

from typing import List

import pandas as pd

from qstrader.system.rebalance import Rebalance


class BuyAndHoldRebalance(Rebalance):
    """
    Generates a single rebalance timestamp at the start date in
    order to create a single set of orders at the beginning of
    a backtest, with no further rebalances carried out.
    """

    def __init__(self, start_dt: pd.Timestamp) -> None:
        self.start_dt = start_dt
        self.rebalances = self._generate_rebalances()

    def _generate_rebalances(self) -> List[pd.Timestamp]:
        return [self.start_dt]
