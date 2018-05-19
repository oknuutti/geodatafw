import numpy as np

import geopyspark as gps
import rasterio
from pyspark import SparkContext
from shapely.geometry import box


def get_raster_layer(sc, path):
    jp2s = ["B02.jp2", "B03.jp2", "B04.jp2"]
    arrs = []
    for jp2 in jp2s:
        with rasterio.open(path+jp2) as f:
            arrs.append(f.read(1))

    data = np.array(arrs, dtype=arrs[0].dtype)

    # Create an Extent instance from rasterio's bounds
    extent = gps.Extent(*f.bounds)

    # The EPSG code can also be obtained from the information read in via rasterio
    projected_extent = gps.ProjectedExtent(extent=extent, epsg=int(f.crs.to_dict()['init'][5:]))

    # We can create a Tile instance from our multiband, raster array and the nodata value from rasterio
    tile = gps.Tile.from_numpy_array(numpy_array=data, no_data_value=f.nodata)

    # Now that we have our ProjectedExtent and Tile, we can create our RDD from them
    rdd = sc.parallelize([(projected_extent, tile)])

    # While there is a time component to the data, this was ignored for this tutorial and
    # instead the focus is just on the spatial information. Thus, we have a LayerType of SPATIAL.
    raster_layer = gps.RasterLayer.from_numpy_rdd(layer_type=gps.LayerType.SPATIAL, numpy_rdd=rdd)

    return raster_layer


def main(data_path, area_of_interest, outfile):
    # Create the SparkContext
    conf = gps.geopyspark_conf(appName="geodatafw", master="local[*]")
    sc = SparkContext(conf=conf)

    # Create raster_layer object from Sentinel 2 data
    raster_layer = get_raster_layer(sc, data_path)

    # Tile the rasters within the layer and reproject them to Web Mercator.
    tiled_layer = raster_layer.tile_to_layout(layout=gps.GlobalLayout(), target_crs=3857)

    # Mask the tiles within the layer with the area of interest
    masked = tiled_layer.mask(geometries=area_of_interest)

    # We will now pyramid the masked TiledRasterLayer so that we can use it in a TMS server later.
    # pyramided_mask = masked.pyramid()

    # Save each layer of the pyramid locally so that it can be accessed at a later time.
    #for pyramid in pyramided_mask.levels.values():
    gps.write(uri='file://%s'%outfile,
              layer_name='munsmo',
              tiled_raster_layer=masked)


if __name__ == '__main__':
    # path to sentinel 2 data with file prefix
    path = "../data/S2A_MSIL1C_20180509T101031_N0206_R022_T34VEQ_20180509T135043.SAFE/GRANULE/L1C_T34VEQ_A015034_20180509T101027/IMG_DATA/T34VEQ_20180509T101031_"

    # near my forest plot at Mustasaari
    area_of_interest = box(63.049715, 21.636323, 63.048448, 21.638664)
    main(path, area_of_interest, '../out/munsmo_20180509')
