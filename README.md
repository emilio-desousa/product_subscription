# Yotta - Product Subscription

Project Nº1: Machine Learning Subject Nº3: Product Subscription by Emilio De Sousa & Damien Mellot


## Getting started

### Requirements 
Following tools must be install to setup this project:
* `python >= 3.8`
* `poetry >= 1.1`

### Setup environment
Following command lines could be used to setup the project.
```
By SSH
$ git clone git@gitlab.com:yotta-academy/mle-bootcamp/projects/ml-project/fall-2020/productsubscription_eds_dm.git
or By https
$ git clone https://gitlab.com/yotta-academy/mle-bootcamp/projects/ml-project/fall-2020/productsubscription_eds_dm.git
$ cd productsubscription_eds_dm/
$ poetry install  # Install virtual environment with packages from pyproject.toml file
``` 

### Run script

In order to run the script, following steps could be performed:
Please put you data to predict in the folder **data/raw**
```
$ poetry shell 
$ deposit_subscription --filename_to_predict  <filename_to_test>
```

### Find predictions

After running the script, you will be able to find the prediction results in a **csv** file in the **data/processed** folder.
