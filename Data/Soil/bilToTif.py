import os
import gdal
import sys
import logging

class BIL2TIF:
    def __init__(self, inBilPath, raw_tif, restructured_tif):
        self.inBilPath = inBilPath
        self.raw_tif = raw_tif
        self.restructured_tif = restructured_tif

    # Use gdal to convert .bil to .tif
    def convert(self):
        inBil = gdal.Open(self.inBilPath)
        driver = gdal.GetDriverByName('GTiff')
        outTif = driver.CreateCopy(self.raw_tif, inBil, 0)

        inBil = None
        outTif = None

    # Defines an gdal.WarpOptions object to define the restucture options and run gdal.Warp
    def restructure(self):
        options = gdal.WarpOptions(
            creationOptions=["COMPRESS=DEFLATE","PREDICTOR=2","ZLEVEL=9"],
            dstSRS="EPSG:4326",
            format="GTiff",
            multithread=True,
            xRes=0.005, yRes=0.005,
            resampleAlg="near",
            )
        gdal.Warp(destNameOrDestDS=self.restructured_tif, srcDSOrSrcDSTab=self.raw_tif, options=options)

if __name__ == "__main__":
    # parse args
    inBil = sys.argv[1]
    raw_tif = sys.argv[2]
    restructured_tif = sys.argv[3]
    converter = BIL2TIF(inBil, raw_tif, restructured_tif)
    logging.info("Converting Dataset..")
    converter.convert()
    logging.info("Restructuring tif according to gdal.WarpOptions object..")
    try:
        converter.restructure()
        logging.info("Dataset Restructured.")
    except:
        raise FileNotFoundError(".bil Dataset was not converted correctly.")
