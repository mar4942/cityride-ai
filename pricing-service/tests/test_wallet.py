import pytest

from pricing_service.wallet import Wallet, WalletUnterdeckungError, belasten


def test_belasten_reduziert_saldo():
    wallet = Wallet(saldo_cent=500)
    neues_wallet = belasten(wallet, 300)
    assert neues_wallet.saldo_cent == 200


def test_belasten_wirft_bei_unterdeckung():
    wallet = Wallet(saldo_cent=100)
    with pytest.raises(WalletUnterdeckungError):
        belasten(wallet, 300)


def test_belasten_original_wallet_unveraendert():
    wallet = Wallet(saldo_cent=500)
    belasten(wallet, 300)
    assert wallet.saldo_cent == 500

    with pytest.raises(WalletUnterdeckungError):
        belasten(wallet, 1000)
    assert wallet.saldo_cent == 500
