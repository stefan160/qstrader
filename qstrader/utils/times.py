import pandas as pd
import pytz
from pandas.tseries.offsets import Hour, BDay


class BusinessDays(object):
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
        self.rebalances = self._generate()

    def _generate(self):
        """
        Output the timestamp list.

        Returns
        -------
        `list[pd.Timestamp]`
            The list of timestamps.
        """

        # Generate a date range for each business day
        business_days = pd.date_range(
            start=self.start_date, end=self.end_date, freq="B", tz=pytz.UTC
        )

        return business_days


class BusinessHours(object):
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
        self.rebalances = self._generate()

    def _generate(self):
        """
        Output the timestamp list.

        Returns
        -------
        `list[pd.Timestamp]`
            The list of timestamps.
        """

        # Generate a date range for each business day
        business_days = pd.date_range(
            start=self.start_date, end=self.end_date, freq="B", tz=pytz.UTC
        )

        # Generate a time range for each hour
        if self.pre_market:
            start_time = pd.Timedelta(hours=0)
        else:
            start_time = pd.Timedelta(hours=14, minutes=30).ceil("1h")

        if self.post_market:
            end_time = pd.Timedelta(hours=21)
        else:
            end_time = pd.Timedelta(hours=23)

        # Generate a list of hourly timestamps
        hourly = []
        for day in business_days:
            business_hours = pd.date_range(
                start=day + start_time,
                end=day + end_time,
                freq=Hour(),
                tz=pytz.UTC,
            )
            hourly.extend(business_hours)

        return hourly
