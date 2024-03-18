""" Business hours simulation engine. """

import datetime

import pandas as pd
import pytz

from qstrader.simulation.sim_engine import SimulationEngine
from qstrader.simulation.event import SimulationEvent
from qstrader.utils.times import BusinessHours


# pylint: disable=too-few-public-methods


class BusinessHoursSimulationEngine(SimulationEngine):
    """
    A SimulationEngine subclass that generates events on a hourly
    frequency limited to hours on typical business days
    between the starting and ending dates. Business days are from
    Monday to Friday. Defaulting to event within trading hours,
    that is 14:30 to 21:00 UTC every business day. Events only
    occur on whole hours. With pre_market set events before 14:30
    are generated as well and with post_market set the events
    after 21:00 are generated as well. es.

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
        pre_market: bool = False,
        post_market: bool = False,
    ):
        """
        Initialize the simulation engine.
        """
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.pre_market = pre_market
        self.post_market = post_market
        self.business_events = BusinessHours(
            self.start_dt,
            self.end_dt,
            pre_market=pre_market,
            post_market=post_market,
        ).rebalances

    def __iter__(self):
        """
        Generate the hourly timestamps and event information
        for pre-market, market open, market close and post-market.

        Yields
        ------
        `SimulationEvent`
            Market time simulation event to yield
        """
        for index, event_time in enumerate(self.business_events):
            year = event_time.year
            month = event_time.month
            day = event_time.day
            hour = event_time.hour

            yield SimulationEvent(
                pd.Timestamp(
                    datetime.datetime(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute=0,
                        second=0,
                    ),
                    tz=pytz.utc,
                ),
                event_type="market_open",
            )

            # if self.pre_market:
            #     yield SimulationEvent(
            #         pd.Timestamp(datetime.datetime(year, month, day), tz="UTC"),
            #         event_type="pre_market",
            #     )

            # yield SimulationEvent(
            #     pd.Timestamp(datetime.datetime(year, month, day, 14, 30), tz=pytz.utc),
            #     event_type="market_open",
            # )

            # yield SimulationEvent(
            #     pd.Timestamp(datetime.datetime(year, month, day, 21, 00), tz=pytz.utc),
            #     event_type="market_close",
            # )

            # if self.post_market:
            #     yield SimulationEvent(
            #         pd.Timestamp(datetime.datetime(year, month, day, 23, 59), tz="UTC"),
            #         event_type="post_market",
            #     )
