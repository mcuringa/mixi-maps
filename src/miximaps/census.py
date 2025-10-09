import pandas as pd
import geopandas as gpd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import us
import geonamescache
import warnings
import appdirs


from . import datacache as dc



def nice_label(var):
    var = var.replace("Estimate!!", "")
    var = var.lower()
    var = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', re.sub(r'[^a-zA-Z0-9]+', '_', var))

    if var.startswith("total_"):
        var = var[6:]

    var = "_".join(var.split(" "))
    if var.endswith(":"):
        var = var[:-1]
    return var

def table_vars(table, year=2023):
    """Look up a census ACS 5 data table from meta data.
        Parameters
        ----------
        table : str
            The census table ID, e.g. B01001
        year : int, optional
            The year of the ACS data, by default 2023
        Returns
        -------
        dict
            A dictionary of variable codes and nice labels.


        Example
        -------
        from miximaps import census as mc
        table = "B25044"
        fields = mc.table_vars(table)
         = 
    
    """
    url = f"https://api.census.gov/data/{year}/acs/acs5/groups/{table}.json"
    data = data = dc.read_file(url)
    vars = data["variables"]
    keys = [k for k in vars.keys() if not k.startswith(table) or k.endswith("E")]
    vars = {k: nice_label(vars[k]["label"]) for k in keys if k in vars}

    return vars

def lookup_state(statefp):
    if statefp == "11":
        return "DC"

    state = us.states.lookup(statefp)
    if state is not None:
        return state.abbr

    return statefp


def county_mapper(statefp="state", countyfp="county"):

    gc = geonamescache.GeonamesCache()
    counties = gc.get_us_counties()
    county_mapper = dict([(c["fips"], c["name"]) for c in counties])
    def m(r):
        fips = r[statefp] + r[countyfp]
        return county_mapper.get(fips, f"Unknown ({fips})")
    return m
        

# def search(term, results=20):
#     tables = get_tables()
#     tables = tables[tables.concept.notnull()]
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(tables.concept)

#     query_vec = vectorizer.transform([term])
#     tables["match"] = cosine_similarity(query_vec, tfidf_matrix).flatten()
#     tables.sort_values(by='match', ascending=False, inplace=True)
#     tables = tables.head(results).copy()
#     results = tables.style.set_properties(subset=['concept'], **{'white-space': 'pre-wrap', 'word-wrap': 'break-word'})
#     results.format({'match': '{:.2%}', 'concept': lambda x: x.title()})
#     return results
