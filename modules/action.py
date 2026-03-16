import asyncio
from typing import TypedDict, List, Literal

from playwright.async_api import async_playwright


class ExperimentalProperty(TypedDict):
    name: Literal[
        "boiling_point",
        "melting_point",
        "flash point",
        "vapor pressure",
        "density",
        "viscosity",
    ]
    value: str
    reference: str


class CrawledResult(TypedDict):
    CID: int
    compound_name: str
    IUPAC_name: str | None
    InChI: str | None
    SMILES: str | None
    molecular_formula: str | None
    CASRN: str | None
    experimental_properties: List[ExperimentalProperty]


def run_crawler(headless=True):
    asyncio.run(playwright_action(cid=1, headless=headless))


async def playwright_action(cid: int, headless=True):
    compound_name: str | None = None
    IUPAC_name: str | None = None
    InChI: str | None = None
    SMILES: str | None = None
    molecular_formula: str | None = None
    CASRN: str | None = None
    experimental_properties: List[ExperimentalProperty] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--start-maximized",
            ],
        )
        page = await browser.new_page()

        await page.goto(f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}")
        await page.wait_for_selector(".app-wrapper")

        #
        IUPAC_locator = page.locator("#IUPAC-Name")
        if await IUPAC_locator.count() > 0:
            pass
