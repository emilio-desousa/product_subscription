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

RANDOM_STATE = 42

FILENAME_BANK = "data.csv"
FILENAME_SOCIO_ECO = "socio_eco.csv"


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
COL_RAW_CONTACT = "CONTACT"
COL_RAW_DURATION_CONTACT = "DURATION_CONTACT"
COL_RAW_NB_CONTACT = "NB_CONTACT"
COL_RAW_NB_DAY_LAST_CONTACT = "NB_DAY_LAST_CONTACT"
COL_RAW_NB_CONTACT_LAST_CAMPAIGN = "NB_CONTACT_LAST_CAMPAIGN"
COL_RAW_RESULT_LAST_CAMPAIGN = "RESULT_LAST_CAMPAIGN"
COL_RAW_SUBSCRIPTION = "SUBSCRIPTION"

COL_MONTH = "MONTH"
COL_WEEKDAY = "WEEKDAY"


TYPE_FOR_CATEGORY = "category"
COLS_TO_CAT_CONVERT = {
    COL_RAW_JOB: TYPE_FOR_CATEGORY,
    COL_RAW_CONTACT: TYPE_FOR_CATEGORY,
    COL_RAW_EDUCATION: TYPE_FOR_CATEGORY,
    COL_RAW_STATUS: TYPE_FOR_CATEGORY,
    COL_RAW_RESULT_LAST_CAMPAIGN: TYPE_FOR_CATEGORY,
}
COLS_TO_FREQ_ENCODE = [COL_RAW_CONTACT, COL_RAW_EDUCATION, COL_RAW_STATUS]
COLS_TO_ONEHOT = [COL_RAW_JOB]
COL_QUARTER = "QUARTER"
COL_SOCIO_DATE = "DATE_SOCIO"
COL_DATE_WITH_ONE = "DATE_1"

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


AGE_RETIRED = 65
DICT_TO_CREATE_COLS = [
    {
        "inf": None,
        "sup": 0,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "column_dist": "is_first_campaign",
    },
    {
        "inf": 0,
        "sup": 4,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "column_dist": "nb_contact_last_campaign_inf_4",
    },
    {
        "inf": 4,
        "sup": 8,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "column_dist": "nb_contact_last_campaign_inf_8",
    },
    {
        "inf": 8,
        "sup": 12,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "column_dist": "nb_contact_last_campaign_inf_12",
    },
    {
        "inf": 12,
        "sup": None,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "column_dist": "nb_contact_last_campaign_sup_12",
    },
]

FINAL_COLUMNS = [
    COL_RAW_AGE,
    COL_RAW_HAS_DEFAULT,
    COL_RAW_BALANCE,
    COL_RAW_HAS_HOUSING_LOAN,
    COL_RAW_HAS_PERSO_LOAN,
    COL_RAW_DURATION_CONTACT,
    COL_RAW_NB_CONTACT,
    COL_RAW_NB_DAY_LAST_CONTACT,
    COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
    COL_RAW_EMPL_VAR_RATE,
    COL_RAW_IDX_CSMR_PRICE,
    COL_RAW_IDX_CSMR_CONFIDENCE,
    COL_MONTH,
    COL_WEEKDAY,
    "is_first_campaign",
    "nb_contact_last_campaign_inf_4",
    "nb_contact_last_campaign_inf_8",
    "nb_contact_last_campaign_inf_12",
    "nb_contact_last_campaign_sup_12",
    COL_RAW_STATUS,
    COL_RAW_EDUCATION,
    COL_RAW_CONTACT,
    "is_last_campaign_success",
    "is_last_campaign_fail",
    "Admin",
    "Chomeur",
    "Col bleu",
    "Employe de menage",
    "Entrepreneur",
    "Etudiant",
    "Independant",
    "Manager",
    "Retraite",
    "Services",
    "Technicien",
    "Autre",
]