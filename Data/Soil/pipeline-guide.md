
#  Dataset and dataset processor tracking procedure
<h2 id="main_goal">Main Goal</h2>
The goal here is to make the Land Sector Datasets repository more interactive. By that, we mean establish some automated procedures that:

- Implement a general dataset processor that can support processing for multiple raw datasets from this repository. This general processor has to be able to convert the raw original datasets into `flint-ready` formats
- Track the processing steps and store the `flint-ready` datasets in remote storage ,ideally [here](https://datasets.mojaglobal.workers.dev/0:/) (that's what we use [DVC](#dvc) for).
- Provide a `health-check` on the processed  datasets when someone makes changes to the processing steps (that's what we use GithubActions and [CML](#cml) for).
	- By `health-check` we mean a GithubAction that executes the modified dataset processor , stores the processed datasets online and checks that they are `flint-ready`

<h3 id="other_goals"> Other goals </h3>

- Another goal is to reduce the required dependencies to process the raw datasets. In the Land Sector repository some datasets depend on arcpy which is difficult for GithubAction runners to handle. The goal here is to refactor the arcpy code so we only depend on gdal ,which is easier for GithubAction runners to handle.

These deliverables are going to help compare differences between different versions of the datasets that were generated from different versions of the dataset processors and automate a small part of the maintenance of moja-global's [online dataset repository](https://datasets.mojaglobal.workers.dev/0:/) .

#### Reminder
As a use case to test my deliverables I used the Harmonized World Soil Database to create an example, but as said the goal is to implement a robust processor that supports multiple datasets in different formats.

<h2 id="processor">Harmonized World Soil Database Processor</h2>

- I have created a `.bil` to `.tif` python converter in [`bilTotif.py`](https://github.com/radistoubalidis/Land_Sector_Datasets/blob/integrate_dvc/Data/Soil/bilToTif.py "bilTotif.py") for the `Harmonized World Soil Database` . It uses `gdal` to :

- Convert `.bil` dataset file from [original source](http://webarchive.iiasa.ac.at/Research/LUC/External-World-soil-database/HTML/HWSD_Data.html?sb=4 "source") to `GeoTiff` format and save it without additional restructure options (`convert` function).

- Restructure the raw `.tif` dataset to specific options defined in the `restructure` function and store it in the same directory with the raw one.

- This `.tif` processor can be scaled by following an OOP approach and modifying its code to be compatible with more datasets (I used the `Harmonized World Soil Database` as a test case)


<h2 id="dvc">DVC</h2>

[Data Version Control](https://dvc.org/) is an open-source data and experiment management tool that offers a wide variety of features. Some of each features are:

- track and save data and machine learning models the same way you capture code (e.g git for datasets)

- Create and switch between different versions of datasets and models (or in out case simulations) .

- Automate workflows using pipelines and dependency graphs


<h2 id="cml">CML</h2>

[CML](https://cml.dev/) is an open-source library for implementing continuous integration & delivery (CI/CD) in machine learning projects.Some of each fatures are:

- Auto-generated reports with metrics and plots in each Git Pull Request.

- It can be used in CI scripts to manage different versions of simulations, track who run a simulation or modified data and when.

- It can be used along with DVC to configure cloud runners to run simulations and generate automated reports.

<h2 id="pipeline"> DVC Pipeline</h2>

- I wrapped the dataset converter inside a dvc pipeline that runs the python script and providing two arguments which are the paths for the raw and restructured `.tif` dataset. (See [`dvc.yaml`](https://github.com/radistoubalidis/Land_Sector_Datasets/blob/integrate_dvc/dvc.yaml)) .

- The DVC pipeline besides providing versioning and configuration to upload the output `tiffs` in a remote storage that is set up is going to be of big help in the case we want to run the converter for multiple scripts.
- More on dvc data pipeline [here](https://dvc.org/doc/start/data-management/pipelines) 
- In our case for now the pipeline stages consist of:
	- `prepare_HarmonizedWorldSoilDatabase` which executes the [dataset processor](#processor)


<h2 id="dvc_setup"> DVC Local Setup</h2>

- You can install DVC in your python environment by following this [guide](https://dvc.org/doc/install "guide")
- Once you have installed DVC on you local environment you can open your local Land_Sector repository in your text editor and by default the DVC pipeline is already configured (**but not the remote storage repository**)
- To check if DVC was properly installed and configured in your local Land Sector repository  type this command and its output should be like this.
```shell
$ dvc stage list
prepare_HarmonizedWorldSoilDatabase Outputs HWSD_VECTOR/HarmonizedWorldSoilDatabase_RAW.tif, HWSD_VECTOR/Harmonized…
```

- In order for the pipeline to work properly you need to setup remote storage to push the pipeline outputs after its execution. You can use this [guide](https://dvc.org/doc/command-reference/remote "guide") to setup you remote storage (I used google drive).

- To check if your remote storage was configured properly type (gdrive is going to be replaced by the remote storage provider you chose):

```shell
$ dvc remote list
your_remote_name gdrive://<remote_storage_id>
```

- Also you can test that the pipeline runs properly by typing.

```shell
$ dvc repro
```

<h2 id="credentials">DVC GDRIVE CREDENTIALS</h2>

- The last step is to setup dvc so it can push the pipeline outputs inside the CI script (health-check).In order, for dvc to be able to push the pipeline outputs inside the CI script you need to setup a Google service account.

- You can follow this [guide](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-service-accounts "guide").

<sub>This is the most complicated step if you need any help contact me in slack (Radis Toumpalidis) or post a comment in my [PR](https://github.com/radistoubalidis/Land_Sector_Datasets/pull/3 "PR").</sub>

<h2 id="action">Github Action : Health Check</h2>

- I wrote an action that executes the above mentioned pipeline and then uploads the output `tiffs` to my personal gdrive. I achieved this by creating a github secret in order to automatically push the outputs inside the action (I followed the instructions from the [dvc docs](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-a-custom-google-cloud-project-recommended "here") page)

- This action is triggered only when in someone's commit [`bilTotif.py`](https://github.com/radistoubalidis/Land_Sector_Datasets/blob/integrate_dvc/Data/Soil/bilToTif.py "bilTotif.py") is changed.

- This constraint is going to help provide an automated dataset tracker:

- i.e when someone wants to use a dataset and process it with custom options ,this action's output is going to ensure that the recent changes did not affect the dataset's integrity thus providing a `health-check`#  Dataset and dataset processor tracking procedure

