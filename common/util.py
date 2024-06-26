import asyncio
from datetime import datetime
from typing import List, Dict, Any
import numpy as np
from pymongo import MongoClient

# Assume we have equivalent functions in these Python modules for the APIs
import okex
import binance
import bybit
from utils import get_timestamp, get_iso_string, get_count_by_hours_ago

# MongoDB client setup (replace with your connection details)
client = MongoClient('mongodb://localhost:27017/')
db = client['database_name']

Job_Granularity = {
    'FiveMins': 60 * 5,
    'FifteenMins': 60 * 15,
    'HalfHour': 60 * 30,
    'OneHour': 60 * 60,
    'TwoHour': 60 * 120,
    'FourHour': 60 * 240,
    'SixHour': 60 * 360,
    'TwelveHour': 60 * 720,
    'OneDay': 60 * 1440,
    'Weekly': 60 * 1440 * 7,
}


async def exec_job(granularity: int, limit: int = None):
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute

    # 获取所有合约信息
    insts = list(db.instrument_info.find({}))

    # 5min / 30min / 2h / 6h / 1w
    jobs_for_btc_only = [
        Job_Granularity['FiveMins'],
        Job_Granularity['HalfHour'],
        Job_Granularity['TwoHour'],
        Job_Granularity['SixHour'],
        Job_Granularity['Weekly'],
    ]

    def custom_filter(i: Dict[str, Any]) -> bool:
        if granularity in jobs_for_btc_only:
            return i['base_currency'] == 'BTC'
        else:
            return i['quote_currency'] == 'USDT'

    valid_insts = sorted(filter(custom_filter, insts),
                         key=lambda x: x['instrument_id'])

    # 最近 4 条K线数据
    count = limit or 4

    if minute_now == 0 and granularity == Job_Granularity['FifteenMins']:
        count = 8

    # 每12h更新过去24h全量数据 (15mins, 1h)
    if (
        hour_now % 12 == 0 and
        granularity in [Job_Granularity['FifteenMins'],
                        Job_Granularity['OneHour']]
    ):
        count = get_count_by_hours_ago(24, granularity)

    await asyncio.gather(
        okex.get_history_klines(
            [i for i in valid_insts if i['exchange'] == 'Okex'],
            {
                'count': count,
                'includeInterval': [granularity],
            },
        ),
        binance.get_history_klines(
            [i for i in valid_insts if i['exchange'] == 'Binance'],
            {
                'count': count,
                'delay': 50,
                'includeInterval': [granularity],
            },
        ),
        # bybit.get_history_klines(
        #     [i for i in valid_insts if i['exchange'] == 'Bybit'],
        #     {
        #         'count': count,
        #         'delay': 200,
        #         'includeInterval': [granularity],
        #     },
        # ),
    )


def get_command_opts(args: List[str]) -> Dict[str, Any]:
    opt: Dict[str, Any] = {}
    # param for instrument_id
    if '-i' in args and len(args) > args.index('-i') + 1:
        opt['includeInst'] = [args[args.index('-i') + 1]]

    # param for granularity
    if '-g' in args and len(args) > args.index('-g') + 1:
        opt['includeInterval'] = [int(args[args.index('-g') + 1])]

    # param for count
    if '-n' in args and len(args) > args.index('-n') + 1:
        opt['count'] = [int(args[args.index('-n') + 1])]

    return opt


# Usage
if __name__ == '__main__':
    # Example of running the exec_job function
    asyncio.run(exec_job(Job_Granularity['OneHour']))

    # Example of getting command options
    args = ['-i', 'instrument1', '-g', '60', '-n', '10']
    opts = get_command_opts(args)
    print(opts)
