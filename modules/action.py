import logging
from typing import TypedDict, Literal

from playwright.async_api import async_playwright, Page, Browser

from . import utils as u


AvailablePropertyTag = Literal[
    "Boiling-Point",
    "Melting-Point",
    "Flash-Point",
    "Vapor-Pressure",
    "Density",
    "Viscosity",
]

AvailableProperties = Literal[
    "boiling_point",
    "melting_point",
    "flash_point",
    "vapor_pressure",
    "density",
    "viscosity",
]


class ExperimentalProperty(TypedDict):
    name: AvailableProperties
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
    experimental_properties: list[ExperimentalProperty]
    available_properties: list[AvailableProperties]


async def parse_computed_descriptors(page: Page, tag: str) -> str | None:
    _locator = page.locator(f"#{tag}")
    if await _locator.count() > 0:
        _name = await _locator.locator("div.break-words.space-y-1").first.text_content()

        return _name


def convert_tag_to_name(tag: AvailablePropertyTag) -> AvailableProperties:
    tag = tag.lower()  # type: ignore
    tag = tag.replace("-", "_")  # type: ignore

    return tag  # type: ignore


async def parse_experimental_properties(
    page: Page,
    tag: AvailablePropertyTag,
    properties: list[ExperimentalProperty],
    available_properties: list[AvailableProperties],
):
    _locator = page.locator(f"#{tag}")
    _property_name = convert_tag_to_name(tag)
    _property: ExperimentalProperty | None = None

    if await _locator.count() > 0:
        available_properties.append(_property_name)
        _inner_div = _locator.locator("div.px-1.py-3.space-y-2 > div")
        _count = await _inner_div.count()
        for i in range(_count):
            _div = _inner_div.nth(i)
            _div_class = await _div.get_attribute("class")

            if _div_class == "break-words space-y-1":
                _property = {"name": _property_name, "value": "", "reference": ""}
                _property["value"] = await _div.inner_text()
                continue

            if _div_class == "pl-2 pb-4" and _property:
                _property["reference"] = await _div.inner_text()
                properties.append(_property)
                _property = None
                continue

    return properties, available_properties


async def playwright_action(browser: Browser, cid: int) -> CrawledResult | None:
    compound_name: str | None = None
    IUPAC_name: str | None = None
    InChI: str | None = None
    SMILES: str | None = None
    molecular_formula: str | None = None
    CASRN: str | None = None
    experimental_properties: list[ExperimentalProperty] = []
    available_properties: list[AvailableProperties] = []
    property_tags: list[AvailablePropertyTag] = [
        "Boiling-Point",
        "Melting-Point",
        "Flash-Point",
        "Vapor-Pressure",
        "Density",
        "Viscosity",
    ]
    crawled_result: CrawledResult | None = None
    page = await browser.new_page()
    try:
        response = await page.goto(
            f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
            wait_until="networkidle",
        )
        await page.wait_for_selector(".app-wrapper")

        if response and response.status == 404:
            raise ValueError("404 Page Not Found")

        compound_name = await page.locator("h1").first.inner_text()

        IUPAC_name = await parse_computed_descriptors(page, "IUPAC-Name")
        InChI = await parse_computed_descriptors(page, "InChI")
        SMILES = await parse_computed_descriptors(page, "SMILES")
        molecular_formula = await parse_computed_descriptors(page, "Molecular-Formula")
        CASRN = await parse_computed_descriptors(page, "CAS")

        for property_tag in property_tags:
            experimental_properties, available_properties = (
                await parse_experimental_properties(
                    page,
                    property_tag,
                    experimental_properties,
                    available_properties,
                )
            )

        if len(available_properties) > 0:
            crawled_result = {
                "CID": cid,
                "compound_name": compound_name,
                "IUPAC_name": IUPAC_name,
                "CASRN": CASRN,
                "molecular_formula": molecular_formula,
                "InChI": InChI,
                "SMILES": SMILES,
                "experimental_properties": experimental_properties,
                "available_properties": available_properties,
            }

    except Exception as e:
        logging.info(f"CID {cid} has been skipped: {e}")

    await page.close()

    return crawled_result


async def run_crawler(headless=True):
    starting_cid = u.get_checkpoint()
    ending_cid = 177929229

    l_cid = (starting_cid // 10000) * 10000 + 1
    u_cid = l_cid + 9999
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
        for cid in range(starting_cid, ending_cid + 1):
            result = await playwright_action(browser, cid)

            if result:
                u.save_data(l_cid, u_cid, result)

            if cid == u_cid:
                u.update_checkpoint(cid)
                l_cid = cid + 1
                u_cid = l_cid + 9999

        await browser.close()
