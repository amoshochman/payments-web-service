import configparser
import json
import logging
import os
import traceback

from flask import Flask

import requests

from constants import BOOKINGS_ERROR_MSG, RATES_ERROR_MSG, BOOKINGS_JSON_SECTION, RATES_JSON_SECTION, RATES_FILE_NAME, \
    INPUT_STUDENT_ID, LOG_FILEMODE, LOG_FORMAT, LOG_FILE_NAME, INPUT_REFERENCE, LOG_LEVEL_ERROR, LOG_LEVEL_WARNING, \
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, CONFIG_FILE_NAME, RATES_URL_STRING, APIS_STRING, BOOKINGS_URL_SUFFIX, \
    BOOKINGS_URL_PREFIX, SERVER_HOST_STRING_CONFIG, APIS_SECTION, LEVEL, LOG_SECTION
from utils import get_output_payment, are_payment_numbers_valid

app = Flask(__name__)
config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)

try:
    RATES = requests.get(config[APIS_STRING][RATES_URL_STRING]).json()[RATES_JSON_SECTION]
except Exception as e:
    logging.error(RATES_ERROR_MSG + ": " + str(e))
    f = open(RATES_FILE_NAME)
    RATES = json.load(f)[RATES_JSON_SECTION]

LOG_LEVEL_INFO = {LOG_LEVEL_DEBUG: logging.DEBUG,
                  LOG_LEVEL_INFO: logging.INFO,
                  LOG_LEVEL_WARNING: logging.WARNING,
                  LOG_LEVEL_ERROR: logging.ERROR,
                  }

logging.basicConfig(filename=LOG_FILE_NAME, filemode=LOG_FILEMODE, format=LOG_FORMAT,
                    level=LOG_LEVEL_INFO[config[LOG_SECTION][LEVEL]])


@app.route("/payments_with_quality_check")
def get_payments_with_quality_check():
    logging.info("entering function get_payments_with_quality_check")
    host = os.environ.get(SERVER_HOST_STRING_CONFIG) or config.get(APIS_SECTION, SERVER_HOST_STRING_CONFIG)
    bookings_url = BOOKINGS_URL_PREFIX + host + BOOKINGS_URL_SUFFIX
    try:
        input_payments = requests.get(bookings_url).json()[BOOKINGS_JSON_SECTION]
        assert type(input_payments) == list
        logging.info("bookings successfully retrieved")
    except Exception as e:
        logging.error(BOOKINGS_ERROR_MSG + ": " + str(e))
        return BOOKINGS_ERROR_MSG, 502

    student_ids_set = set()
    output_payments = []
    for input_payment in input_payments:
        if type(input_payment) != dict or not are_payment_numbers_valid(input_payment):
            logging.error("invalid payment type received, either it's not a dictionary or one of the types is invalid: " + str(input_payment))
            continue
        try:
            logging.debug("processing payment with reference: " + str(input_payment.get(INPUT_REFERENCE)))
            output_payment = get_output_payment(input_payment, RATES, student_ids_set)
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error("An exception has occurred: " + str(e) + ", payment is being skipped: " + str(input_payment))
        else:
            student_ids_set.add(input_payment[INPUT_STUDENT_ID])
            output_payments.append(output_payment)

    return output_payments, 200


if __name__ == "__main__":
    app.run(debug=True)
