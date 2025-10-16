
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

    if cache:
        filename = f"nyc_tracts_{table}-{region}-{year}.geojson"
    else:
        filename = None

    county_fips = get_nyc_counties(region=region).keys()
    df = mc.get_tracts(c, table, county_fips,year=year,filename=filename)

    boros = {
        '005': 'Bronx',
        '047': 'Brooklyn',
        '061': 'Manhattan',
        '085': 'Staten Island',
        '081': 'Queens',
    }

    df['borough'] = df['countyfp'].map(boros).fillna('-')

    return df
