import asyncio

from playwright.async_api import async_playwright


def run_crwaler(headless=True):
    asyncio.run(playwright_action(headless=headless))


async def playwright_action(headless=True):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()

        await page.goto("https://pubchem.ncbi.nlm.nih.gov/compound/1")
