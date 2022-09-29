import asyncio
import tzlocal

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from DBconnect import data_transfer

GS_POLLING_INTERVAL = 1


if __name__ == '__main__':
    """
    Здесь происходит запуск планировщика, вызывающего
    метод data_transfer() с интервалом, указанным в переменной
    GS_POLLING_INTERVAL.
    """
    scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

    async def db_data_transfer():
        data_transfer()

    print('Starting script...')

    scheduler.add_job(
        db_data_transfer,
        "interval",
        minutes=GS_POLLING_INTERVAL
    )
    scheduler.start()

    print('Press Ctrl+C to exit\n')

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        asyncio.get_event_loop().stop()
