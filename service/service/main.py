import asyncio

import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bool_values import read_value, writing_false_value
from DBconnect import check_and_transfer, data_transfer

GS_POLLING_INTERVAL = 1


if __name__ == '__main__':
    """
    Здесь происходит запуск планировщика, вызывающего
    метод check_and_transfer() с интервалом, указанным в переменной
    GS_POLLING_INTERVAL.
    """
    print('Скрипт начал свою работу. Для выхода нажмите Ctrl+C.')

    scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

    if read_value():
        data_transfer()
        writing_false_value()

    async def db_data_transfer():
        check_and_transfer()

    scheduler.add_job(
        db_data_transfer,
        "interval",
        minutes=GS_POLLING_INTERVAL
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        asyncio.get_event_loop().stop()
