from .utils import http_request, write_log
from .parser import (
    match_heading,
    parse_computed_descriptors,
    parse_experimental_properties,
)
from .dto import CrawledData


def get_pubchem_data(CID: int) -> CrawledData | None:
    IUPAC_name: str | None = None
    InChI: str | None = None
    SMILES: str | None = None
    CASRN: str | None = None
    experimental_property_data = []
    available_properties = []

    data = http_request(
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{CID}/JSON"
    )
    try:
        if not data:
            raise ValueError("HTTP reqeust body not found")

        record = data["Record"]
        compound_name = record["RecordTitle"]
        record_section = record["Section"]
        references = record["Reference"]

        # ==================== Parse Names and Identifiers ====================
        names_and_identifiers = match_heading("Names and Identifiers", record_section)
        if names_and_identifiers:
            names_and_identifiers_section = names_and_identifiers.get("Section")

            computed_descriptors = match_heading(
                "Computed Descriptors", names_and_identifiers_section
            )
            if computed_descriptors:
                computed_descriptors_section = computed_descriptors.get("Section")
                IUPAC_name = parse_computed_descriptors(
                    "IUPAC name", computed_descriptors_section
                )
                InChI = parse_computed_descriptors(
                    "InChI", computed_descriptors_section
                )
                SMILES = parse_computed_descriptors(
                    "SMILES", computed_descriptors_section
                )

            other_identifiers = match_heading(
                "Other Identifiers", names_and_identifiers_section
            )
            if other_identifiers:
                other_identifiers_section = other_identifiers.get("Section")
                CASRN = parse_computed_descriptors("CAS", other_identifiers_section)

        # ==================== Parse Chemical and Physical Properties ====================
        chemical_and_physical_properties = match_heading(
            "Chemical and Physical Properties", record_section
        )
        if chemical_and_physical_properties:
            chemical_and_physical_properties_section = (
                chemical_and_physical_properties.get("Section")
            )
            experimental_properties = match_heading(
                "Experimental Properties",
                chemical_and_physical_properties_section,
            )
            if experimental_properties:
                experimental_properties_section = experimental_properties.get("Section")

                boiling_point_parsed_result = parse_experimental_properties(
                    "Boiling Point",
                    experimental_properties_section,
                    references,
                )
                if boiling_point_parsed_result:
                    experimental_property_data.extend(boiling_point_parsed_result)
                    available_properties.append("boiling_point")

                melting_point_parsed_result = parse_experimental_properties(
                    "Melting Point",
                    experimental_properties_section,
                    references,
                )
                if melting_point_parsed_result:
                    experimental_property_data.extend(melting_point_parsed_result)
                    available_properties.append("melting_point")

                flash_point_parsed_result = parse_experimental_properties(
                    "Flash Point",
                    experimental_properties_section,
                    references,
                )
                if flash_point_parsed_result:
                    experimental_property_data.extend(flash_point_parsed_result)
                    available_properties.append("flash_point")

                density_parsed_result = parse_experimental_properties(
                    "Density",
                    experimental_properties_section,
                    references,
                )
                if density_parsed_result:
                    experimental_property_data.extend(density_parsed_result)
                    available_properties.append("density")

                vapor_density_parsed_result = parse_experimental_properties(
                    "Vapor Density",
                    experimental_properties_section,
                    references,
                )
                if vapor_density_parsed_result:
                    experimental_property_data.extend(vapor_density_parsed_result)
                    available_properties.append("vapor_density")

                vapor_pressure_parsed_result = parse_experimental_properties(
                    "Vapor Pressure",
                    experimental_properties_section,
                    references,
                )
                if vapor_pressure_parsed_result:
                    experimental_property_data.extend(vapor_pressure_parsed_result)
                    available_properties.append("vapor_pressure")

                viscosity_parsed_result = parse_experimental_properties(
                    "Viscosity",
                    experimental_properties_section,
                    references,
                )
                if viscosity_parsed_result:
                    experimental_property_data.extend(viscosity_parsed_result)
                    available_properties.append("viscosity")

        if len(available_properties) > 0:
            crawled_result: CrawledData = {
                "CID": CID,
                "compound_name": compound_name,
                "IUPAC_name": IUPAC_name,
                "InChI": InChI,
                "SMILES": SMILES,
                "CASRN": CASRN,
                "properties": experimental_property_data,
                "available_properties": available_properties,
            }

            return crawled_result
    except Exception as e:
        write_log(f"ERROR__000__UNHANDLED_RESPONSE_TYPE: {e}")
