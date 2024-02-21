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

        # Generate a date range for each business day
        business_days = pd.date_range(
            start=self.start_date, end=self.end_date, freq='B', tz=pytz.UTC
        )

        # Generate hourly timestamps within each business day
        hourly_rebalances = []
        for day in business_days:
            business_hours = pd.date_range(
                start=day + pd.Timedelta(hours=14, minutes=30),
                end=day + pd.Timedelta(hours=21),
                freq=Hour(),
                tz=pytz.UTC
            )
            hourly_rebalances.extend(business_hours)

        return hourly_rebalances
