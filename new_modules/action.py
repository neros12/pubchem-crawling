from utils import http_request, match_heading, parse_computed_descriptors


CID = 1
compound_name = None
IUPAC_name = None
InChI = None
SMILES = None
CASRN = None
experimental_properties = []
available_properties = []

data = http_request(
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/712/JSON"
)

if data:
    record = data["Record"]

    compound_name = record.get("RecordTitle")
    record_section = record.get("Section")

    # Parse Names and Identifiers
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
            InChI = parse_computed_descriptors("InChI", computed_descriptors_section)
            SMILES = parse_computed_descriptors("SMILES", computed_descriptors_section)

        other_identifiers = match_heading(
            "Other Identifiers", names_and_identifiers_section
        )
        if other_identifiers:
            other_identifiers_section = other_identifiers.get("Section")
            CASRN = parse_computed_descriptors("CAS", other_identifiers_section)

        # Parse Chemical and Physical Properties
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

                pass
