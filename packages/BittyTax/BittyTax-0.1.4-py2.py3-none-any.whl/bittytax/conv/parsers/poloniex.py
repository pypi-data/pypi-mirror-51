# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2019

from decimal import Decimal, ROUND_UP

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser

WALLET = "Poloniex"

PRECISION = Decimal('0.00000000')

def parse_poloniex_trades(in_row):
    if in_row[3] == "Buy":
        fee_quantity = Decimal(in_row[5]) - Decimal(in_row[5]) * \
                (Decimal(in_row[7].replace('%', '')) / Decimal(100))
        fee_quantity = fee_quantity.quantize(PRECISION, rounding=ROUND_UP)
        return TransactionOutRecord(TransactionOutRecord.TYPE_TRADE,
                                    DataParser.parse_timestamp(in_row[0]),
                                    buy_quantity=in_row[5],
                                    buy_asset=in_row[1].split('/')[0],
                                    sell_quantity=in_row[6],
                                    sell_asset=in_row[1].split('/')[1],
                                    fee_quantity=Decimal(in_row[5]) - fee_quantity,
                                    fee_asset=in_row[1].split('/')[0],
                                    wallet=WALLET)
    elif in_row[3] == "Sell":
        fee_quantity = Decimal(in_row[6]) - Decimal(in_row[6]) * \
                (Decimal(in_row[7].replace('%', '')) / Decimal(100))
        fee_quantity = fee_quantity.quantize(PRECISION, rounding=ROUND_UP)
        return TransactionOutRecord(TransactionOutRecord.TYPE_TRADE,
                                    DataParser.parse_timestamp(in_row[0]),
                                    buy_quantity=in_row[6],
                                    buy_asset=in_row[1].split('/')[1],
                                    sell_quantity=in_row[5],
                                    sell_asset=in_row[1].split('/')[0],
                                    fee_quantity=Decimal(in_row[6]) - fee_quantity,
                                    fee_asset=in_row[1].split('/')[1],
                                    wallet=WALLET)
    else:
        raise ValueError("Unrecognised Type: " + in_row[3])

def parse_poloniex_deposits_withdrawals(in_row):
    if "COMPLETE:" in in_row[4]:
        return TransactionOutRecord(TransactionOutRecord.TYPE_WITHDRAWAL,
                                    DataParser.parse_timestamp(in_row[0]),
                                    sell_quantity=in_row[2],
                                    sell_asset=in_row[1],
                                    wallet=WALLET)
    else:
        return TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                    DataParser.parse_timestamp(in_row[0]),
                                    buy_quantity=in_row[2],
                                    buy_asset=in_row[1],
                                    wallet=WALLET)

def parse_poloniex_withdrawals(in_row):
    return TransactionOutRecord(TransactionOutRecord.TYPE_WITHDRAWAL,
                                DataParser.parse_timestamp(in_row[0]),
                                sell_quantity=Decimal(in_row[2]) - Decimal(in_row[3]),
                                sell_asset=in_row[1],
                                fee_quantity=in_row[3],
                                fee_asset=in_row[1],
                                wallet=WALLET)

DataParser(DataParser.TYPE_EXCHANGE,
           "Poloniex Trades",
           ['Date', 'Market', 'Category', 'Type', 'Price', 'Amount', 'Total', 'Fee', 'Order Number',
            'Base Total Less Fee', 'Quote Total Less Fee'],
           row_handler=parse_poloniex_trades)

DataParser(DataParser.TYPE_EXCHANGE,
           "Poloniex Deposits/Withdrawals",
           ['Date', 'Currency', 'Amount', 'Address', 'Status'],
           row_handler=parse_poloniex_deposits_withdrawals)

DataParser(DataParser.TYPE_EXCHANGE,
           "Poloniex Withdrawals",
           ['Date', 'Currency', 'Amount', 'Fee Deducted', 'Amount - Fee', 'Address', 'Status'],
           row_handler=parse_poloniex_withdrawals)
