from apscheduler.schedulers.blocking import BlockingScheduler

from modules.action import run_crwaler


run_crwaler(headless=False)
