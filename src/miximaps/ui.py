import folium
import xyzservices.providers as xyz


def base_map(gdf=None, center=None, zoom=10, provider=xyz.CartoDB.Positron, name=""):
    """
    Create a base map using Folium.

    Parameters:
    - gdf: `GeoDataFrame` to use for the center of the map
    - center: [latitude, longitude] for the center of the map
    - zoom: Initial zoom level of the map, scale is 1-18 (zoomed out --> zoomed in)
    - provider: Map tile provider from `xyzservices` (e.g., xyz.CartoDB.Positron, xyz.CartoDB.DarkMatter, etc.)
    - name: Name of the map (will show up if Layer Control is added)

    Returns:
    - folium.Map object
    """
    # if no center is provided, center it near the middle of the US
    if center == None and gdf is not None:
        minx, miny, maxx, maxy = gdf.total_bounds
        center = [(miny + maxy) / 2, (minx + maxx) / 2]
    elif center == None:
        center = [40.69018448848042, -73.98654521557344]  # AU Brooklyn

    attr = "maptools" if not provider.attribution else provider.attribution
    m = folium.Map(name=name, tiles=provider, attr=attr, location=center, zoom_start=zoom)
    return m


def make_labels(m, df, col, style={}):
    """
    Add the string of `col`
    to the center of each shape in `df`
    onto a folium map.
    
    Parameters:
    -----------
    m : folium.Map
        The map to add the labels to.
    df : GeoDataFrame
        The GeoDataFrame to get the labels and locations from.
    col : str
        The column in `df` to use for the labels.
    style : dict
        A dictionary of CSS styles to apply to the labels.

    Returns:
    --------
    folium.Map
        The map with the labels added.

    Example:
    --------

    m = boroughs_df.explore()
    label_style = {
        "font-size": "12pt",
        "font-weight": "bold",
        "color": "black",
        "background-color": "white",
        "border": "2px solid black",
        "border-radius": "5px",
        "padding": "2px"
    }
    m = make_labels(m, boroughs_df, 'boro_name', style=label_style)
    m
    
    """
    style_str = ";".join([f"{k}:{v}" for k, v in style.items()])

    def label(row):
        point = row.geometry.centroid
        html = f"""<div style="{style_str}">{row[col]}</div>"""
        folium.Marker(
            location=(point.y, point.x),
            icon=folium.DivIcon(html=html)).add_to(m)
    df.apply(label, axis=1)
    return m
