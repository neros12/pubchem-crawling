import requests

response = requests.get(
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/712/JSON?heading=Experimental%20Properties",
    verify=False,
)
data = response.json()
references = data["Record"]["Reference"]
experimental_data = data["Record"]["Section"][0]["Section"][0]["Section"]


pass
