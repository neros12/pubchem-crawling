from typing import TypedDict, Literal


PropertyCode = Literal[
    "boiling_point",
    "melting_point",
    "flash_point",
    "density",
    "vapor_density",
    "vapor_pressure",
    "viscosity",
]


class ExperimentalProperty(TypedDict):
    property_name: PropertyCode
    value: str
    source: str


class CrawledData(TypedDict):
    CID: int
    compound_name: str
    IUPAC_name: str | None
    InChI: str | None
    SMILES: str | None
    CASRN: str | None
    properties: list[ExperimentalProperty]
    available_properties: list[PropertyCode]
