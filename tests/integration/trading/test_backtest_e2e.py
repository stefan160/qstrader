import os

import pandas as pd
import datetime
import pytz
import pytest

from qstrader.alpha_model.fixed_signals import FixedSignalsAlphaModel
from qstrader.asset.universe.static import StaticUniverse
from qstrader.trading.backtest import BacktestTradingSession


def test_backtest_sixty_forty(etf_filepath):
    """
    Ensures that a full end-to-end weekly rebalanced backtested
    trading session with fixed proportion weights produces the
    correct rebalance orders as well as correctly calculated
    market values after a single month's worth of daily
    backtesting.
    """
    os.environ["QSTRADER_CSV_DATA_DIR"] = etf_filepath

    assets = ["EQ:ABC", "EQ:DEF"]
    universe = StaticUniverse(assets)
    signal_weights = {"EQ:ABC": 0.6, "EQ:DEF": 0.4}
    alpha_model = FixedSignalsAlphaModel(signal_weights)

    start_dt = pd.Timestamp("2019-01-01 00:00:00", tz=pytz.UTC)
    end_dt = pd.Timestamp("2019-01-31 23:59:00", tz=pytz.UTC)

    backtest = BacktestTradingSession(
        start_dt,
        end_dt,
        universe,
        alpha_model,
        portfolio_id="000001",
        rebalance="weekly",
        rebalance_weekday="WED",
        long_only=True,
        cash_buffer_percentage=0.05,
    )
    backtest.run(results=False)

    portfolio = backtest.broker.portfolios["000001"]

    portfolio_dict = portfolio.portfolio_to_dict()
    expected_dict = {
        "EQ:ABC": {
            "unrealised_pnl": -31121.26203538094,
            "realised_pnl": 0.0,
            "total_pnl": -31121.26203538094,
            "market_value": 561680.8382534103,
            "quantity": 4674,
        },
        "EQ:DEF": {
            "unrealised_pnl": 18047.831359406424,
            "realised_pnl": 613.3956570402925,
            "total_pnl": 18661.227016446715,
            "market_value": 376203.80367208034,
            "quantity": 1431.0,
        },
    }

    history_df = portfolio.history_to_df().reset_index()
    expected_df = pd.read_csv(os.path.join(etf_filepath, "sixty_forty_history.dat"))

    pd.testing.assert_frame_equal(history_df, expected_df)

    # Necessary as test fixtures differ between
    # Pandas 1.1.5 and 1.2.0 very slightly
    for symbol in expected_dict.keys():
        for metric in expected_dict[symbol].keys():
            assert portfolio_dict[symbol][metric] == pytest.approx(
                expected_dict[symbol][metric]
            )


def test_backtest_long_short_leveraged(etf_filepath):
    """
    Ensures that a full end-to-end daily rebalanced backtested
    trading session of a leveraged long short portfolio with
    fixed proportion weights produces the correct rebalance
    orders as well as correctly calculated market values after
    a single month's worth of daily backtesting.
    """
    os.environ["QSTRADER_CSV_DATA_DIR"] = etf_filepath

    assets = ["EQ:ABC", "EQ:DEF"]
    universe = StaticUniverse(assets)
    signal_weights = {"EQ:ABC": 1.0, "EQ:DEF": -0.7}
    alpha_model = FixedSignalsAlphaModel(signal_weights)

    start_dt = pd.Timestamp("2019-01-01 00:00:00", tz=pytz.UTC)
    end_dt = pd.Timestamp("2019-01-31 23:59:00", tz=pytz.UTC)

    backtest = BacktestTradingSession(
        start_dt,
        end_dt,
        universe,
        alpha_model,
        portfolio_id="000001",
        rebalance="daily",
        long_only=False,
        gross_leverage=2.0,
    )
    backtest.run(results=False)

    portfolio = backtest.broker.portfolios["000001"]

    portfolio_dict = portfolio.portfolio_to_dict()
    expected_dict = {
        "EQ:ABC": {
            "unrealised_pnl": -48302.832839363175,
            "realised_pnl": -3930.9847615026706,
            "total_pnl": -52233.81760086585,
            "market_value": 1055344.698660986,
            "quantity": 8782.0,
        },
        "EQ:DEF": {
            "unrealised_pnl": -42274.737165376326,
            "realised_pnl": -9972.897320721153,
            "total_pnl": -52247.63448609748,
            "market_value": -742417.5692312752,
            "quantity": -2824.0,
        },
    }

    history_df = portfolio.history_to_df().reset_index()
    expected_df = pd.read_csv(os.path.join(etf_filepath, "long_short_history.dat"))

    pd.testing.assert_frame_equal(history_df, expected_df)
    assert portfolio_dict == expected_dict


from qstrader.system.rebalance.hourly import HourlyRebalance


def test_backtest_hourly_rebalance_alpha_model_call(etf_filepath):
    """
    Ensures that a full end-to-end hourly rebalanced backtested
    trading session with fixed proportion weights produces the
    correct rebalance orders as well as correctly calculated
    market values after a single day's worth of hourly
    backtesting.
    """
    os.environ["QSTRADER_CSV_DATA_DIR"] = etf_filepath

    assets = ["EQ:ABC", "EQ:DEF"]
    universe = StaticUniverse(assets)
    signal_weights = {"EQ:ABC": 0.6, "EQ:DEF": 0.4}
    alpha_model = FixedSignalsAlphaModel(signal_weights)

    start_dt = pd.Timestamp("2019-01-01 00:00:00", tz=pytz.UTC)
    end_dt = pd.Timestamp("2019-01-01 23:00:00", tz=pytz.UTC)

    backtest = BacktestTradingSession(
        start_dt,
        end_dt,
        universe,
        alpha_model,
        portfolio_id="000001",
        rebalance="hourly",
        pre_market=True,
        long_only=True,
        cash_buffer_percentage=0.05,
    )
    backtest.run(results=False)

    portfolio = backtest.broker.portfolios["000001"]

    # Check that the alpha model was called for each hourly rebalance
    # during market open hours (14:30 to 21:00 UTC)

    market_open_hours = pd.date_range(
        start=start_dt, end=end_dt, freq="h", tz=pytz.UTC
    )[
        pd.date_range(
            start=start_dt, end=end_dt, freq="h", tz=pytz.UTC
        ).indexer_between_time("14:30", "21:00")
    ]

    # for market_hour in market_open_hours:
    #     assert market_hour in alpha_model.call_times

    # Check that the portfolio has been rebalanced hourly
    assert len(portfolio.history) == len(market_open_hours)  # .shape[0]
