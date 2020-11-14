"""Basic settings of the project.
Contains all configurations for the projectself.
Should NOT contain any secrets.
>>> import settings
>>> settings.DATA_DIR
"""
import os

# By default the data is stored in this repository's "data/" folder.
# You can change it in your own settings file.
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

DATA_DIR = os.path.join(REPO_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
INTERIM_DIR = os.path.join(DATA_DIR, "interim")


SEP = ";"

COL_RAW_JOB = "JOB_TYPE"
COL_RAW_STATUS = "STATUS"
COL_RAW_DATE = "DATE"
COL_RAW_AGE = "AGE"
COL_RAW_EDUCATION = "EDUCATION"
COL_RAW_HAS_DEFAULT = "HAS_DEFAULT"
COL_RAW_BALANCE = "BALANCE"
COL_RAW_HAS_HOUSING_LOAN = "HAS_HOUSING_LOAN"
COL_RAW_HAS_PERSO_LOAN = "HAS_PERSO_LOAN"
COL_RAW_CONTAT = "CONTACT"
COL_RAW_DURATION_CONTACT = "DURATION_CONTACT"
COL_RAW_NB_CONTACT = "NB_CONTACT"
COL_RAW_NB_DAY_LAST_CONTACT = "NB_DAY_LAST_CONTACT"
COL_RAW_NB_CONTACT_LAST_CAMPAIGN = "NB_CONTACT_LAST_CAMPAIGN"
COL_RAW_RESULT_LAST_CAMPAIGN = "RESULAT_LAST_CAMPAIGN"
COL_RAW_SUBSCRIPTION = "SUBSCRIPTION"

COL_QUARTER = "QUARTER"
COL_SOCIO_DATE = "DATE_SOCIO"

COL_RAW_EMPL_VAR_RATE = "EMPLOYMENT_VARIATION_RATE"
COL_RAW_IDX_CSMR_PRICE = "IDX_CONSUMER_PRICE"
COL_RAW_IDX_CSMR_CONFIDENCE = "IDX_CONSUMER_CONFIDENCE"

ARRAY_WITH_COUPLE_TO_FILL_JOB = [["Tertiaire", "Manager"], ["Primaire", "Col bleu"]]
ARRAY_WITH_COUPLE_TO_FILL_EDU = [
    ["Manager", "Tertiaire"],
    ["Admin", "Secondaire"],
    ["Services", "Secondaire"],
]

BOOLEAN_ENCODING = {"Yes": 1, "No": 0}

COL_YEAR_MONTH = "YEAR/MONTH"