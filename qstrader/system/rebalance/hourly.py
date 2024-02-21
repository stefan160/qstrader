from qstrader.system.rebalance.rebalance import Rebalance
from pandas.tseries.offsets import Hour
import pandas as pd
import pytz


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

    def __init__(self, start_date, end_date, pre_market=False):
        self.start_date = start_date
        self.end_date = end_date
        self.rebalances = self._generate_rebalances()

    def _generate_rebalances(self):
        """
        Output the rebalance timestamp list.

        Returns
        -------
        `list[pd.Timestamp]`
            The list of rebalance timestamps.
        """

        # range of all hours in the dates
        rebalances = pd.date_range(
            start=self.start_date, end=self.end_date, freq="h", tz=pytz.UTC
        )

        # filter for hours within market hours
        rebalances_market_hours = rebalances[
            rebalances.indexer_between_time("14:30", "21:00")
        ]

        rebalance_times = [pd.Timestamp(time) for time in rebalances_market_hours]

        return rebalance_times
