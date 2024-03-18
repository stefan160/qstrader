""" Hourly Rebalance Class. """

from typing import List
import pandas as pd
from qstrader.system.rebalance.rebalance import Rebalance
from qstrader.utils.times import BusinessHours


class HourlyRebalance(Rebalance):
    """
    Generates a list of rebalance timestamps for pre- or post-market,
    for every hour between the starting and ending dates provided.

    All timestamps produced are set to UTC.

    Parameters
    ----------
    start_date : `pd.Timestamp`
        The starting timestamp of the rebalance range.
    end_date : `pd.Timestamp`
        The ending timestamp of the rebalance range.
    pre_market : `Boolean`, optional
        Whether to carry out the rebalance at market open/close.
    """

    def __init__(self, start_date, end_date, pre_market=False, post_market=False):
        self.start_date = start_date
        self.end_date = end_date
        self.pre_market = pre_market
        self.post_market = post_market
        self.rebalances = self._generate_rebalances()

    def _generate_rebalances(self) -> List[pd.Timestamp]:
        return [
            event
            for event in BusinessHours(
                start_date=self.start_date,
                end_date=self.end_date,
                pre_market=self.pre_market,
                post_market=self.post_market,
            ).rebalances
        ]
