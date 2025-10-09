
import pandas as pd
import geopandas as gpd
from census import Census
import pygris
import os

from . import census as mc
from . import datacache as dc
from . import tiger


def get_nyc_counties(region="metro"):
    """Get the FIPS codes for NYC and its inner suburbs"""
        

    city = {
        ('36', '005'): 'Bronx County',
        ('36', '047'): 'Kings County',
        ('36', '061'): 'New York County',
        ('36', '085'): 'Richmond County',
        ('36', '081'): 'Queens County'
    }
    ny_inner = {
        ('36', '119'): 'Westchester County',
        ('36', '059'): 'Nassau County',
    }
    ny_outer = {
        ('36', '027'): 'Dutchess County',
        ('36', '071'): 'Orange County',
        ('36', '079'): 'Putnam County',
        ('36', '087'): 'Rockland County',
        ('36', '103'): 'Suffolk County',
    }
    nj = {
        ('34', '003'): 'Bergen County',
        ('34', '013'): 'Essex County',
        ('34', '017'): 'Hudson County',
    }

    ct = {
        ('09', '001'): 'Fairfield County',
    }

    metro = city | ny_inner | ny_outer | nj | ct

    inner = city | ny_inner | nj | ct
    suburbs = ny_inner | ny_outer | nj | ct
    if region == "city":
        return city
    if region == "inner":
        return inner
    if region == "suburbs":
        return suburbs
    return metro


def get_tracts(c, table, year=2023, region="inner", cache=True):
    """Get census tracts for NYC and inner suburbs for an acs5 table"""

    filename = f"nyc_tracts_{table}-{region}-{year}.geojson"
    path = dc.local_path(filename)
    filename = os.path.join(path, filename)

    if os.path.exists(filename) and cache:
        return dc.read_file(filename, gdf=True)


    fields = mc.table_vars(table)
    vars = list(fields.keys())

    county_fips = get_nyc_counties(region=region).keys()

    print(county_fips)

    results = []
    for state, counties in county_fips:
        r = c.acs5.state_county_tract(vars, state, counties, Census.ALL)
        results.extend(r)

    df = pd.DataFrame(results)
    df.rename(columns=fields, inplace=True)

    # drop rows with no data
    df.dropna(inplace=True)


    # make nicer column names and re-order
    df["county_name"] = df.apply(mc.county_mapper(), axis=1)
    df["statefp"] = df.state
    df["state"] = df.statefp.apply(mc.lookup_state)
    df["countyfp"] = df["county"]
    df["county"] = df.county_name
    df.drop(columns=["county_name"], inplace=True)
   

    boros = {
        '005': 'Bronx',
        '047': 'Brooklyn',
        '061': 'Manhattan',
        '085': 'Staten Island',
        '081': 'Queens',
    }

    df['borough'] = df['countyfp'].map(boros).fillna('-')




    state_fips = df.statefp.unique().tolist()



    # merge tiger tracts
    tracts = pd.concat([pygris.tracts(state=s, year=year, cache=True) for s in state_fips])
    tracts["geography"] = tracts["GEOIDFQ"]
    df = df.merge(tracts[["geography", "geometry"]], on="geography", )
    df = gpd.GeoDataFrame(df, geometry="geometry")
    df = tiger.shoreline(df, year=year)
    
    if cache:
        print("Writing to cache:", filename)
        dc.write_cache(df, filename)
    return df
