# coding:utf-8
import os
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

jobstores = {
    # 'mongo': {'type': 'mongodb'},
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BlockingScheduler()
scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


@scheduler.scheduled_job('cron', day_of_week='1', hour=11)
def crawl_games():
    os.system("scrapy crawl netease -a url='https://play.163.com,https://game.163.com'")


@scheduler.scheduled_job('cron', day_of_week='3', hour=21)
def crawl_sports():
    os.system("scrapy crawl netease -a url='https://sports.163.com'")


@scheduler.scheduled_job('cron', day_of_week='5', hour=3)
def crawl_renjian():
    os.system("scrapy crawl netease -a url='https://renjian.163.com'")


if __name__ == '__main__':
    try:
        print("爬取任务管理已启动按ctrl+C退出执行")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

