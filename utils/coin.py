
"""
Questa classe è utilizzata per creare criptovalute degli utenti in maniera più comoda
"""
class Coin: 
    def __init__(self, name, symbol, balance):
        self.name = name
        self.symbol = symbol
        self.balance = balance

    def as_dict(self):
        return {
                "name": self.name,
                "symbol": self.symbol,
                "balance": self.balance
                }
