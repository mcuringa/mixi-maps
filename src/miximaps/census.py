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


from . import cache



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
    data = data = cache.read_file(url)
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
        





# def nice_name(var):
#     var = var.replace("Estimate!!", "")
#     var = var.lower()

#     var = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', re.sub(r'[^a-zA-Z0-9]+', '_', var))

#     if var.startswith("total_"):
#         var = var[6:]
    
#     var = "_".join(var.split(" "))
#     if var.endswith(":"):
#         var = var[:-1]
#     return var


# def col_name(var):
#     if "!!" in var:
#         var = var.split("!!")[-1]
#     return nice_name(var)

# def rename_columns(data, year=2023):

#     url = f"http://api.census.gov/data/{year}/acs/acs1/subject/variables.json"
#     resp = requests.get(url)
#     json = resp.json()

#     df = pd.DataFrame(json['variables']).T

#     df["var_name"] = df.label.apply(col_name)
#     df.var_name = df.var_name.str.replace("total_households_", "")
#     df.var_name = df.var_name.str.replace("percent_total_households_", "")
#     col_map = df["var_name"].to_dict()
#     col_map['[["GEO_ID"'] = 'GEOID'

#     results = data.rename(columns=col_map)
#     # get cols not in col_map
#     def check(c):
#         if c not in col_map.values() and "_" in c and not c.endswith("E"):
#             return True
#         if c.startswith("Unnamed"):
#             return True
    
#     drop_cols = [c for c in results.columns if check(c)]
#     results.drop(columns=drop_cols, inplace=True)

#     return results


# def get_variables():
#     global census_vars
#     if census_vars is None:
#         _init_vars()
#     return census_vars.copy()


# def get_tables():
#     global census_tables
#     if census_tables is None:
#         _init_vars()
#     return census_tables.sort_values(by="group").copy()



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


# def get_table(table, as_dict=True):
#     table = table.upper()
#     variables = get_variables()
#     results = census_vars[variables.group == table].copy()
#     results.sort_values(by="var", inplace=True)
#     if as_dict:
#         return results.set_index('var')['var_name'].to_dict()
#     return results