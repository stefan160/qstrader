""" Equity asset class. """

from .asset import Asset


class Equity(Asset):
    """
    Stores meta data about an equity common stock or ETF.

    Parameters
    ----------
    name : `str`
        The asset's name (e.g. the company name and/or
        share class).
    symbol : `str`
        The asset's original ticker symbol.
        TODO: This will require modification to handle proper
        ticker mapping.
    tax_exempt: `boolean`, optional
        Is the share exempt from government taxation?
        Necessary for taxation on share transactions, such
        as UK stamp duty.
    """

    def __init__(self, name: str, symbol: str, tax_exempt: bool = True):
        self.cash_like = False
        self.name = name
        self.symbol = symbol
        self.tax_exempt = tax_exempt

    def __repr__(self) -> str:
        """
        String representation of the Equity Asset.
        """
        return f"Equity(name={self.name}, symbol={self.symbol}, tax_exempt={self.tax_exempt}"
