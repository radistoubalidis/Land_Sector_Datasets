import os
from osgeo import gdal

def BILtoTIF(inBilPath,outTifPath):
    inBil = gdal.Open(inBilPath)
    driver = gdal.GetDriverByName('GTiff')
    outTif = driver.CreateCopy(outTifPath, inBil, 0)

    inBil = None
    outTif = None

def restructureTIF(in_tif, out_tif):
    options = gdal.WarpOptions(
        creationOptions=["COMPRESS=DEFLATE","PREDICTOR=2","ZLEVEL=9"],
        dstSRS="EPSG:4326",
        format="GTiff",
        multithread=True,
        xRes=0.005, yRes=0.005,
        resampleAlg="near",
        )
    gdal.Warp(destNameOrDestDS=out_tif, srcDSOrSrcDSTab=in_tif, options=options)

if __name__ == "__main__":
    in_src = os.path.join("HWSD_RASTER","hwsd.bil")
    out_src = os.path.join("HWSD_VECTOR","HarmonizedWorldSoilDatabase_RAW.tif")
    BILtoTIF(in_src,out_src)
    if os.path.isfile(out_src):
        restructuredTifPath = os.path.join("HWSD_VECTOR","HarmonizedWorldSoilDatabase_RESTRUCTURED.tif")
        restructureTIF(in_tif=out_src, out_tif=restructuredTifPath)
