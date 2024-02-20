from qstrader.system.rebalance.rebalance import Rebalance
from pandas.tseries.offsets import Hour


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

    def __init__(
        self,
        start_date,
        end_date,
        pre_market=False
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.market_time = self._set_market_time(pre_market)
        self.rebalances = self._generate_rebalances()

    def _set_market_time(self, pre_market):
        """
        Determines whether to use market open or market close
        as the rebalance time.

        Parameters
        ----------
        pre_market : `Boolean`
            Whether the rebalance is carried out at market open/close.

        Returns
        -------
        `str`
            The time string used for Pandas timestamp construction.
        """
        return "14:30:00" if pre_market else "21:00:00"

    def _generate_rebalances(self):
        """
        Output the rebalance timestamp list.

        Returns
        -------
        `list[pd.Timestamp]`
            The list of rebalance timestamps.
        """
        rebalance_dates = pd.date_range(
            start=self.start_date,
            end=self.end_date,
            freq=Hour()
        )

        rebalance_times = [
            pd.Timestamp(
                "%s %s" % (date, self.market_time), tz=pytz.utc
            )
            for date in rebalance_dates
        ]

        return rebalance_times
