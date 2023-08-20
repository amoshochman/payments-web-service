# expected fields in Bookings retrieved from server
INPUT_REFERENCE = 'reference'
INPUT_AMOUNT = 'amount'
INPUT_AMOUNT_RECEIVED = 'amount_received'
INPUT_CURRENCY_FROM = 'currency_from'
INPUT_STUDENT_ID = 'student_id'
INPUT_EMAIL = 'email'

# fields to return in response
OUTPUT_REFERENCE = 'reference'
OUTPUT_AMOUNT = 'amount'
OUTPUT_AMOUNT_WITH_FEES = 'amountWithFees'
OUTPUT_AMOUNT_RECEIVED = 'amountReceived'
OUTPUT_QUALITY_CHECK = 'qualityCheck'
OUTPUT_OVER_PAYMENT = 'overPayment'
OUTPUT_UNDER_PAYMENT = 'underPayment'

# quality checks possible values
AMOUNT_THRESHOLD = "AmountThreshold"
DUPLICATED_PAYMENT = "DuplicatedPayment"
INVALID_EMAIL = "InvalidEmail"

# message errors
BOOKINGS_ERROR_MSG = "there was an error while reading bookings data"
RATES_ERROR_MSG = "there was an error while reading rates data"

# file names
MOCK_SERVER_FILENAME_BASE = 'mock_server.json'
EXPECTED_CLIENT_FILENAME_BASE = 'expected_client.json'
MOCK_RATES_FILENAME = 'mock_rates.json'
TESTS_DATA_FOLDER_NAME = "tests_data"
CONFIG_FILE_NAME = 'config-example.ini'

# relevant sections in files
BOOKINGS_JSON_SECTION = 'bookings'
RATES_JSON_SECTION = 'rates'
RATES_FILE_NAME = "rates.json"

# logs
LOG_FILEMODE = 'w'
LOG_FORMAT = '%(name)s - %(levelname)s - %(message)s'
LOG_FILE_NAME = 'app.log'

# logs
LOG_LEVEL_ERROR = 'logging.ERROR'
LOG_LEVEL_WARNING = 'logging.WARNING'
LOG_LEVEL_INFO = 'logging.INFO'
LOG_LEVEL_DEBUG = 'logging.DEBUG'

# config
BOOKINGS_URL_STRING = 'BOOKINGS_URL'
RATES_URL_STRING = 'RATES_URL'
APIS_STRING = 'APIS'
BOOKINGS_URL_SUFFIX = ":9292/api/bookings"
BOOKINGS_URL_PREFIX = "http://"
SERVER_HOST_STRING_CONFIG = 'server_host'
APIS_SECTION = 'APIS'
LEVEL = 'level'
LOG_SECTION = 'LOG'

# miscelaneous
DECIMALS_NUM = 2
FEES = {1000: 5, 10000: 3}
REMANENT_FEE = 2
AMOUNT_TRESHOLD_VAL = 1000000

