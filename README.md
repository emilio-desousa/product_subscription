Product Subscription

Machine Learning Project: Product Subscription by Emilio De Sousa & Damien Mellot


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

In order to run the script, following steps could be performed 
( only csv format is supported for now, contact us if you neeed ):
- Please put you data to predict and the file to train in the folder **data/raw**
- For the Train file, please name it *data.csv" or change the value of **FILENAME_BANK** in `base.py`
- For the social context data file, please name it "socio_eco.csv" or change the value of **FILENAME_SOCIO_ECO** in `base.py`
- After that run the following commands:

```
$ poetry shell 
$ deposit_subscription --filename_to_predict  <filename_to_predict>
```

### Find predictions

After running the script, you will be able to find the prediction results in a **csv** file in the **data/processed** folder. 
- **0** is for **No**
- **1** is for **Yes**

*Care, you can overwrite it, please move it into another folder if you want to make another prediction*
