# this is a class file (not executable)

import numpy as np


def r(n):
    return np.round(n, 2)


def pmt(mortgage, down, apr, term):
    # if down payment is in % then convert it to decimal
    if down > 1:
        down = down / 100

    # if term is not in months then convert it to months
    if term < 36:
        term = term * 12

    # if apr is in % then convert it to decimal
    if apr > 1:
        apr = apr / 100

    apr_mo = apr / 12

    principal = mortgage * (1 - down)
    factor = (1 + apr_mo) ** term
    monthlypayment = principal * factor * apr_mo / (factor - 1)

    return np.round(monthlypayment)


def net_operating(price, rent=1400, hoa=200, down=5, rate=2.75, duration=30, tax_rate=0.68,
                  vacancy_rate=5, prop_mgmnt_rate=10, capex=5):
    """
    Calculates NOI
    :param price:
    :param rent:
    :param hoa:
    :param pmi:
    :param down:
    :param rate:
    :param duration:
    :param tax_rate:
    :param vacancy_rate:
    :param prop_mgmnt_rate:
    :param capex:
    :return:
    """

    mortgage_amt = r(pmt(price, down, rate, duration))
    pmi = r((pmi_pct(down) / 100) * price * (1 - down / 100) / 12)
    prop_mgmnt = r(rent * prop_mgmnt_rate / 100)
    prop_tax = r(price * (tax_rate / 100) / 12)
    prop_repairs = r(rent * 0.02)
    capex = r(rent * capex / 100)
    vacancy = r(rent * vacancy_rate / 100)

    # These sections are a list of all the expenses used and formulas for each
    noi_monthly = r(rent - prop_mgmnt - prop_tax - prop_repairs - vacancy - mortgage_amt - hoa - pmi)
    noi = r(noi_monthly * 12)

    downpayment = r(price * down / 100)
    roi = r((noi / downpayment) * 100)
    caprate = r((noi / price) * 100)

    # gestimate_caprate = gestimatecaprate(price=price)

    # Summing up expenses
    operating_data = {'mortgage': mortgage_amt, 'prop_tax': prop_tax, 'pmi': pmi, 'prop_mgmnt': prop_mgmnt, 'prop_tax': prop_tax,
            'repairs': prop_repairs, 'capex': capex, 'vacancy': vacancy, 'noi_monthly': noi_monthly, 'NOI': noi,
            'DownPayment': downpayment, 'ROI': roi, 'caprate': caprate}
    return operating_data


def pmi_pct(down):
    """Calculated PMI based on credit score > 760 and coverage ratio of 30%. returns PMI as a percentage."""
    LTV = 100 - down
    pmi_chart = {0.90: [95.01, 97], 0.54: [90.01, 95], 0.49: [85.01, 90], 0.37: [80, 85]}

    for k, v in pmi_chart.items():
        if v[0] < LTV <= v[1]:
            return k
    return 0


def gestimatecaprate(price, rent=1400, hoa=200, pmi=100, down=5, rate=2.75, duration=30, tax_rate=0.68,
                     vacancy_rate=5, prop_mgmnt_rate=10, capex=5):
    # if there is no price data exit
    if price < 120:
        return price

    # calculate caprate
    operating_data = net_operating(price, rent, hoa, pmi, down, rate, duration, tax_rate,
                                   vacancy_rate, prop_mgmnt_rate, capex)
    caprate = operating_data['caprate']

    # if the caprate is > 8% then price is ok
    if caprate > 8:
        return price

    # if caprate is < 8 then keep lowering price till caprate increases > 5%
    while True:
        if caprate > 5:
            return price
        price = price - 1000
        operating_data = net_operating(price, rent, hoa, pmi, down, rate, duration, tax_rate,
                                       vacancy_rate, prop_mgmnt_rate, capex)
        caprate = operating_data['caprate']
        # prevent runaway process
        if price < 120:
            return price
