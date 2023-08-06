# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2019

from decimal import Decimal

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser

WALLET = "Ledger Live"

def parse_ledger_live(in_row):
    if in_row[2] == "IN":
        return TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                    DataParser.parse_timestamp(in_row[0]),
                                    buy_quantity=Decimal(in_row[3]) + Decimal(in_row[4]),
                                    buy_asset=in_row[1],
                                    fee_quantity=Decimal(in_row[4]),
                                    fee_asset=in_row[1],
                                    wallet=WALLET)

    if in_row[2] == "OUT":
        return TransactionOutRecord(TransactionOutRecord.TYPE_WITHDRAWAL,
                                    DataParser.parse_timestamp(in_row[0]),
                                    sell_quantity=Decimal(in_row[3]) - Decimal(in_row[4]),
                                    sell_asset=in_row[1],
                                    fee_quantity=Decimal(in_row[4]),
                                    fee_asset=in_row[1],
                                    wallet=WALLET)
    else:
        raise ValueError("Unrecognised Operation Type: " + in_row[2])

DataParser(DataParser.TYPE_WALLET,
           "Ledger Live",
           ['Operation Date', 'Currency Ticker', 'Operation Type', 'Operation Amount',
            'Operation Fees', 'Operation Hash', 'Account Name', 'Account id'],
           row_handler=parse_ledger_live)
