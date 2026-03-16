# from apscheduler.schedulers.blocking import BlockingScheduler

from modules.action import run_crawler


run_crawler(headless=False)
