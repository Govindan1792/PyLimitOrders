import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client = MagicMock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_executed_on_price_below_limit(self):
        # Add a buy order with a limit of 100
        self.agent.add_order('buy', 'IBM', 1000, 100)

        # Simulate a price tick below the limit price
        self.agent.on_price_tick('IBM', 99)

        # Check if the order was executed
        self.execution_client.execute_order.assert_called_with('buy', 'IBM', 1000, 99)

    def test_sell_order_executed_on_price_above_limit(self):
        # Add a sell order with a limit of 200
        self.agent.add_order('sell', 'IBM', 500, 200)

        # Simulate a price tick above the limit price
        self.agent.on_price_tick('IBM', 201)

        # Check if the order was executed
        self.execution_client.execute_order.assert_called_with('sell', 'IBM', 500, 201)

    def test_order_not_executed_if_price_does_not_meet_limit(self):
        # Add a buy order with a limit of 100
        self.agent.add_order('buy', 'IBM', 1000, 100)

        # Simulate a price tick above the limit price (should not trigger the buy)
        self.agent.on_price_tick('IBM', 101)

        # Ensure no execution occurs
        self.execution_client.execute_order.assert_not_called()

if __name__ == '__main__':
    unittest.main()
