""" Cash asset class."""

from .asset import Asset


class Cash(Asset):
    """
    Stores meta data about a cash asset.

    Parameters
    ----------
    currency : str, optional
        The currency of the Cash Asset. Defaults to USD.
    """

    def __init__(self, currency: str = "USD"):
        self.cash_like = True
        self.currency = currency
