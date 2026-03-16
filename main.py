import logging
import asyncio

from modules.action import run_crawler


logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)

asyncio.run(run_crawler(headless=False))
