def test_execute_limit_order():
    """
    Tests that the SimulatedBroker correctly executes a limit order
    when the limit price is met.
    """
    # Create a simulated broker, exchange, and data handler
    start_dt = pd.Timestamp('2020-01-01 15:00:00', tz=pytz.UTC)
    exchange = SimulatedExchange(start_dt)
    data_handler = Mock()
    data_handler.get_asset_latest_bid_ask_price.return_value = (101.0, 102.0)
    broker = SimulatedBroker(start_dt, exchange, data_handler)

    # Create a portfolio and subscribe funds
    portfolio_id = 'test_portfolio'
    broker.create_portfolio(portfolio_id)
    broker.subscribe_funds_to_portfolio(portfolio_id, 100000.0)

    # Create a limit order with a limit price that will be met by the current market price
    order = Order(
        dt=start_dt,
        asset='EQ:TEST',
        quantity=100,
        order_type='LIMIT',
        limit_price=101.5
    )

    # Execute the limit order
    broker.submit_order(portfolio_id, order)
    broker.update(start_dt)

    # Check if the order was executed
    executed_order = broker.portfolios[portfolio_id].transactions[0]
    assert executed_order.quantity == order.quantity
    assert executed_order.price == order.limit_price
    assert executed_order.asset == order.asset
    assert broker.portfolios[portfolio_id].cash == 100000.0 - (order.quantity * order.limit_price)

    # Create a limit order with a limit price that will not be met by the current market price
    order = Order(
        dt=start_dt,
        asset='EQ:TEST',
        quantity=100,
        order_type='LIMIT',
        limit_price=103.0
    )

    # Execute the limit order
    broker.submit_order(portfolio_id, order)
    broker.update(start_dt)

    # Check if the order was not executed
    assert len(broker.portfolios[portfolio_id].transactions) == 1  # No new transactions should be added
