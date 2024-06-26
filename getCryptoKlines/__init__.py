import datetime
from azure.functions import TimerRequest
from pymongo import MongoClient
from enum import Enum

class JobGranularity(Enum):
    FIFTEEN_MINS = 1
    ONE_HOUR = 2
    TWO_HOUR = 3
    FOUR_HOUR = 4
    ONE_DAY = 5
    SIX_HOUR = 6
    TWELVE_HOUR = 7

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    return db

async def exec_job(granularity: JobGranularity):
    # Implement your job execution logic here
    pass

async def init_instruments():
    # Implement your instrument initialization logic here
    pass

async def delete_old_signals():
    # Implement your signal deletion logic here
    pass

async def main(mytimer: TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        print('The timer is past due!')

    start_time = datetime.datetime.now()
    day_now = start_time.day
    hour_now = start_time.hour
    minute_now = start_time.minute

    db = connect_mongo()

    # 15 minutes.
    if minute_now % 15 == 0:
        await exec_job(JobGranularity.FIFTEEN_MINS)

    # hourly
    if minute_now == 0:
        await init_instruments()
        await exec_job(JobGranularity.ONE_HOUR)

    # 2hourly
    if hour_now % 2 == 0 and minute_now == 0:
        await exec_job(JobGranularity.TWO_HOUR)

    # 4hourly
    if hour_now % 4 == 0 and minute_now == 0:
        await exec_job(JobGranularity.FOUR_HOUR)
        await exec_job(JobGranularity.ONE_DAY)

    # 6hourly
    if hour_now % 6 == 0 and minute_now == 0:
        await exec_job(JobGranularity.SIX_HOUR)

    # 12hourly
    if hour_now % 12 == 0 and minute_now == 0:
        await init_instruments()
        await exec_job(JobGranularity.TWELVE_HOUR)

    # At minute 0 on every day.
    if hour_now == 0 and minute_now == 0:
        await delete_old_signals()

    print(f'Python timer trigger function ran at {utc_timestamp}')