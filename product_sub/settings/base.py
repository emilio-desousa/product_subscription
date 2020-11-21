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
FILENAME_DATA_TEST = "data_test.csv"


FILENAME_BANK_TRAIN = "data_train.csv"
FILENAME_SOCIO_ECO_TRAIN = "socio_eco.csv"
FILENAME_DATA_TEST = "data_test.csv"


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

COL_IS_FIRST_CAMPAIGN = "is_first_campaign"

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


DICT_CONTINUOUS_TO_CATEGORICAL = [
    {
        "inf": None,
        "sup": 0,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "val": 0,
    },
    {
        "inf": 0,
        "sup": 4,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "val": 1,
    },
    {
        "inf": 4,
        "sup": 8,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "val": 2,
    },
    {
        "inf": 8,
        "sup": 12,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "val": 3,
    },
    {
        "inf": 12,
        "sup": None,
        "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN,
        "val": 4,
    },
    {
        "inf": None,
        "sup": -1,
        "column_source": COL_RAW_NB_DAY_LAST_CONTACT,
        "val": 0,
    },
    {
        "inf": 0,
        "sup": 50,
        "column_source": COL_RAW_NB_DAY_LAST_CONTACT,
        "val": 1,
    },
    {
        "inf": 50,
        "sup": 200,
        "column_source": COL_RAW_NB_DAY_LAST_CONTACT,
        "val": 2,
    },
    {
        "inf": 200,
        "sup": 400,
        "column_source": COL_RAW_NB_DAY_LAST_CONTACT,
        "val": 3,
    },
    {
        "inf": 400,
        "sup": None,
        "column_source": COL_RAW_NB_DAY_LAST_CONTACT,
        "val": 4,
    },
]
dict_with_duration_to_categorize = [
    {
        "inf": 0,
        "sup": 100,
        "column_source": COL_RAW_DURATION_CONTACT,
        "column_dist": "short_duration_contact",
    },
    {
        "inf": 100,
        "sup": 500,
        "column_source": COL_RAW_DURATION_CONTACT,
        "column_dist": "middle_duration_contact",
    },
    {
        "inf": 500,
        "sup": 1000,
        "column_source": COL_RAW_DURATION_CONTACT,
        "column_dist": "long_duration_contact",
    },
    {
        "inf": 1000,
        "sup": None,
        "column_source": COL_RAW_DURATION_CONTACT,
        "column_dist": "so_long_contact",
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
    # "nb_contact_last_campaign_inf_4",
    # "nb_contact_last_campaign_inf_8",
    # "nb_contact_last_campaign_inf_12",
    # "nb_contact_last_campaign_sup_12",
    # "short_duration_contact",
    # "middle_duration_contact",
    # "long_duration_contact",
    # "so_long_contact",
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