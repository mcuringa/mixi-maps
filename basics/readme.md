Mixi Maps Basics
================
These notebooks offer a basic introduction to working with python libraries,
US Census, and NYC Open Data. The techniques here can be combined to create
more interesting and complex maps.

These are meant to be run in Jupyter Notebook -- either through Google Colab, or
locally. Our development team uses VS Code for development. If you want help
getting your own local environment set up (faster, more stable than Colab),
just bring your laptop to a map club meeting, or reach out on Discord.

Notebooks
---------
1. **[census-table_median-inc.ipynb](https://colab.research.google.com/drive/1RywLR4gvoGUbUAnsjaTqA2z2yGcO-BCF?usp=sharing)**
   This notebook shows how to use the miximaps package to load a basic US Census ACS 5 table
   for the tracts in the NYC metro area, and to create a choropleth map of median household income.
2. **[nyc-311-load-data.ipynb](nyc-311-load-data.ipynb)**
   A very simple notebook to load 311 data using `pandas` and to look at the most common complaints. 
3. **[myc-311-map.ipynb](nyc-311-map.ipynb)**
   A notebook to load 311 data using `pandas` and to create a point thematic map of the most common complaints. Export data for QGIS.
4. **[parking-complaints.ipynb](parking-complaints.ipynb)**
   Merges 311 with zip code geographies to create a choropleth of parking complaints.
5. **[distance-from-subway.ipynb](distance-from-subway.ipynb)**
   Ths notebook is a little bit more complicated. It loads our median income census data for NYC tracts and
   locations of public pools from NYC Open Data. It then merges the two datasets using a spatial join
   function from `GeoPandas` to find the closest pool to each tract. It then creates a scatter plot
   and calculates a Pearson R correlation to see if there is a relationship between median rent and distance to the nearest pool (there isn't).
6. **rent-change.ipynb**
   This takes a look at multiple years of census data to create a
   layered map, allowing a glimpse at how NYC rents have changed over
   the period of 2010-2024.



**_[Click here for data files to download](https://adelphiuniversity-my.sharepoint.com/personal/mcuringa_adelphi_edu/_layouts/15/guestaccess.aspx?share=Ev9gP83bK7tFtdBBa3SvbFEBy15l21AtoAOQ6TXSJIodSw&e=sfPGrk)_**


