# Dataset and dataset processor tracking procedure
> **Dataset processing**
- I have created a .bil to .tif python converter in [`bilTotif.py`](https://github.com/radistoubalidis/Land_Sector_Datasets/blob/integrate_dvc/Data/Soil/bilToTif.py "bilTotif.py") for the `Harmonized World Soil Database` . It uses `gdal` to :
 - Convert `.bil` dataset file from [original source](http://webarchive.iiasa.ac.at/Research/LUC/External-World-soil-database/HTML/HWSD_Data.html?sb=4 "source") to `.tif` format and save it without additional restructure options (`convert` function).
 - Restructure the raw `.tif` dataset to specific options defined in `restructure` function and store it in the same directory with the raw one.
- This `.tif` processor can be scaled by following an OOP approach and modifying its code to be compatible with more datasets (I used the `Harmonized World Soil Database` as a test case)

> **DVC Pipeline**
- I wrapped the dataset converter inside a dvc pipeline that runs the python script and providing two arguments which are the paths for the raw and restructured `.tif` dataset. (See [`dvc.yaml`](https://github.com/radistoubalidis/Land_Sector_Datasets/blob/integrate_dvc/dvc.yaml)) .
- The DVC pipeline besides providing versioning and configuration to upload the output `tiffs` in a remote storage that is set up is going to be of big help in the case we want to run the converter for multiple scripts.

> **Github Action : Health Check**
- I wrote an action that executes the above mentioned pipeline and then uploads the output `tiffs` to my personal gdrive. I achieved this by creating a github secret in order to automatically push the outputs inside the action (I followed the instructions from the [dvc docs](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-a-custom-google-cloud-project-recommended "here") page)
- This action is triggered only when in someone's commit [`bilTotif.py`](https://github.com/radistoubalidis/Land_Sector_Datasets/blob/integrate_dvc/Data/Soil/bilToTif.py "bilTotif.py") is changed.
- This constraint is going to help provide an automated dataset tracker:
  - i.e when someone wants to use a dataset and process it with custom options ,this action's output is going to ensure that the recent changes did not affect the dataset's integrity thus providing a `health-check`
