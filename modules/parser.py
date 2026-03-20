from typing import Dict, Any


def match_heading(value: str, data_list: list[Dict[str, Any]] | None):
    if data_list:
        for data in data_list:
            target = data.get("TOCHeading", "")
            if target == value:

                return data


def find_reference(ref_number: int, ref_list: list[Dict[str, Any]]) -> str | None:
    for ref in ref_list:
        target = ref.get("ReferenceNumber")
        if int(target) == ref_number:  # type: ignore

            return ref.get("SourceName")


def parse_computed_descriptors(name, sections) -> str | None:
    try:
        data = match_heading(name, sections)
        if data:
            return data["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
    except:
        pass


def parse_experimental_properties(name: str, sections, references):
    experimental_properties = []
    data = match_heading(name, sections)
    if data:
        properties: list[Dict[str, Any]] | None = data.get("Information")  # type: ignore
        if properties:
            for _property in properties:
                reference_number = _property["ReferenceNumber"]
                source = find_reference(reference_number, references)
                _property_value = _property["Value"]
                if "StringWithMarkup" in _property_value:
                    experiement_property = _property_value["StringWithMarkup"][0][
                        "String"
                    ]
                elif "StringWithMarkup" in _property_value:
                    experiement_property = str(
                        _property_value.get("Number", "")[0]
                    ) + str(_property_value.get("Unit", ""))
                else:
                    continue

                experimental_properties.append(
                    {
                        "property_name": name.lower().replace(" ", "_"),
                        "value": experiement_property,
                        "source": source,
                    }
                )

            return experimental_properties
