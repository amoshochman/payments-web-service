import re

from constants import INPUT_AMOUNT, INPUT_AMOUNT_RECEIVED, INPUT_CURRENCY_FROM, OUTPUT_AMOUNT, OUTPUT_AMOUNT_WITH_FEES, \
    OUTPUT_AMOUNT_RECEIVED, OUTPUT_REFERENCE, INPUT_REFERENCE, OUTPUT_QUALITY_CHECK, INPUT_EMAIL, INPUT_STUDENT_ID, \
    OUTPUT_OVER_PAYMENT, \
    OUTPUT_UNDER_PAYMENT, AMOUNT_THRESHOLD, DUPLICATED_PAYMENT, INVALID_EMAIL, DECIMALS_NUM, FEES, REMANENT_FEE, \
    AMOUNT_TRESHOLD_VAL


def get_quality_check(student_ids_set, email, student_id, amount):
    quality_check = []
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        quality_check.append(INVALID_EMAIL)
    if student_id in student_ids_set:
        quality_check.append(DUPLICATED_PAYMENT)
    if AMOUNT_TRESHOLD_VAL < amount:
        quality_check.append(AMOUNT_THRESHOLD)
    return ', '.join(quality_check)


def get_amount_with_fees(amount):
    fee = None
    for cur_amount, cur_fee in FEES.items():
        if amount <= cur_amount:
            fee = cur_fee
            break
    if not fee:
        fee = REMANENT_FEE
    return amount + amount * fee / 100


def get_amounts(original_amount, original_amount_received, currency, rates):
    rate = rates[currency]
    amount = original_amount / rate
    amount_with_fees = get_amount_with_fees(amount)
    amount_received = original_amount_received / rate
    decimals = DECIMALS_NUM
    return (round(elem, decimals) for elem in (amount, amount_with_fees, amount_received))


def get_output_payment(input_payment, rates, student_ids_set):
    output_payment = {}
    amount, amount_with_fees, amount_received = get_amounts(input_payment[INPUT_AMOUNT],
                                                            input_payment[INPUT_AMOUNT_RECEIVED],
                                                            input_payment[INPUT_CURRENCY_FROM].upper(), rates)
    output_payment[OUTPUT_AMOUNT] = amount
    output_payment[OUTPUT_AMOUNT_WITH_FEES] = amount_with_fees
    output_payment[OUTPUT_AMOUNT_RECEIVED] = amount_received
    output_payment[OUTPUT_REFERENCE] = input_payment[INPUT_REFERENCE]
    output_payment[OUTPUT_QUALITY_CHECK] = get_quality_check(student_ids_set, input_payment[INPUT_EMAIL],
                                                             input_payment[INPUT_STUDENT_ID],
                                                             output_payment[OUTPUT_AMOUNT_WITH_FEES])
    output_payment[OUTPUT_OVER_PAYMENT] = amount_with_fees < amount_received
    output_payment[OUTPUT_UNDER_PAYMENT] = amount_received < amount_with_fees
    return output_payment


def are_payment_numbers_valid(payment):
    return True if type(payment[INPUT_AMOUNT]) == int or float and type(
        payment[INPUT_AMOUNT_RECEIVED]) == int or float else False
