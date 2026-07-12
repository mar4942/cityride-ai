from dataclasses import dataclass


@dataclass(frozen=True)
class Wallet:
    saldo_cent: int


class WalletUnterdeckungError(Exception):
    def __init__(self, saldo_cent: int, betrag_cent: int):
        self.saldo_cent = saldo_cent
        self.betrag_cent = betrag_cent
        super().__init__(
            f"Wallet-Unterdeckung: Saldo {saldo_cent} < Betrag {betrag_cent}"
        )


def belasten(wallet: Wallet, betrag_cent: int) -> Wallet:
    """Gibt ein neues Wallet mit reduziertem Saldo zurueck.

    Wirft WalletUnterdeckungError, wenn der Saldo nicht ausreicht.
    Reine Funktion, keine I/O.
    """
    if wallet.saldo_cent < betrag_cent:
        raise WalletUnterdeckungError(wallet.saldo_cent, betrag_cent)
    return Wallet(saldo_cent=wallet.saldo_cent - betrag_cent)
