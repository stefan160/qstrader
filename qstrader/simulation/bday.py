"""
The business day simulation engine.
"""

import datetime

import pandas as pd
import pytz

from qstrader.simulation.sim_engine import SimulationEngine
from qstrader.simulation.event import SimulationEvent
from qstrader.utils.times import BusinessDays


class BusinessDaysSimulationEngine(SimulationEngine):
    """
    A SimulationEngine subclass that generates events on a daily
    frequency defaulting to typical business days, that is
    Monday-Friday.

    In particular it does not take into account any specific
    regional holidays, such as Federal Holidays in the USA or
    Bank Holidays in the UK.

    It produces a pre-market event, a market open event,
    a market closing event and a post-market event for every day
    between the starting and ending dates.

    Parameters
    ----------
    starting_day : `pd.Timestamp`
        The starting day of the simulation.
    ending_day : `pd.Timestamp`
        The ending day of the simulation.
    pre_market : `Boolean`, optional
        Whether to include a pre-market event
    post_market : `Boolean`, optional
        Whether to include a post-market event
    """

    def __init__(
        self,
        start_dt: pd.Timestamp,
        end_dt: pd.Timestamp,
        pre_market: bool = True,
        post_market: bool = True,
    ):
        if end_dt < start_dt:
            raise ValueError(
                "Ending date time %s is earlier than starting date time %s. "
                "Cannot create DailyBusinessDaySimulationEngine "
                "instance." % (end_dt, start_dt)
            )

        self.start_dt = start_dt
        self.end_dt = end_dt
        self.pre_market = pre_market
        self.post_market = post_market
        self.business_days = BusinessDays(
            self.start_dt,
            self.end_dt,
            pre_market=self.pre_market,
            post_market=self.post_market,
        ).rebalances

    def __iter__(self):
        """
        Generate the daily timestamps and event information
        for pre-market, market open, market close and post-market.

        Yields
        ------
        `SimulationEvent`
            Market time simulation event to yield
        """
        for index, bday in enumerate(self.business_days):
            year = bday.year
            month = bday.month
            day = bday.day

            if self.pre_market:
                yield SimulationEvent(
                    pd.Timestamp(datetime.datetime(year, month, day), tz="UTC"),
                    event_type="pre_market",
                )

            yield SimulationEvent(
                pd.Timestamp(datetime.datetime(year, month, day, 14, 30), tz=pytz.utc),
                event_type="market_open",
            )

            yield SimulationEvent(
                pd.Timestamp(datetime.datetime(year, month, day, 21, 00), tz=pytz.utc),
                event_type="market_close",
            )

            if self.post_market:
                yield SimulationEvent(
                    pd.Timestamp(datetime.datetime(year, month, day, 23, 59), tz="UTC"),
                    event_type="post_market",
                )
