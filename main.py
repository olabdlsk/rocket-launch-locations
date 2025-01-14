# from matplotlib import pyplot as plt
import geopandas as gpd
import os
import pandas as pd

# define paths to shapefiles layers
layers_dir = os.path.join(os.getcwd(), "layers")
buildings_dir = os.path.join(layers_dir, "buildings")
area_dir = os.path.join(layers_dir, "area")
results_dir = os.path.join(layers_dir, "results")

area = os.path.join(area_dir, "granica_dolnoslaskie.shp")
area = gpd.read_file(area)

#coordination system setup (epsg 2180, unit - meters)
area = area.to_crs(2180)
all_buildings_path = os.path.join(results_dir, "all_buildings.shp")

#the layers are chunked, so here we have a piece of code which reads concatenated buildings if the file exists or concatenate them
if os.path.isfile(all_buildings_path):
    all_buildings = gpd.read_file(all_buildings_path, mask=area)
else:
    buildings_files = [os.path.join(buildings_dir, file) for file in os.listdir(buildings_dir) if file.endswith(".shp")]
    buildings = [gpd.read_file(file) for file in buildings_files]
    all_buildings = pd.concat(buildings)
    all_buildings.to_file(all_buildings_path)

#coordination system setup (epsg 2180, unit - meters)
all_buildings = all_buildings.to_crs(2180)

#change the geometry of buildings - add buffer (2000 meters)
all_buildings['geometry'] = all_buildings['geometry'].buffer(2000)

#aggregate buildings
dissolved = all_buildings.dissolve()

#area minus buildings buffers
#https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.difference.html#geopandas.GeoSeries.difference
results = area.difference(dissolved)

#save the shapefile
results.to_file(os.path.join(results_dir, "result.shp"))
