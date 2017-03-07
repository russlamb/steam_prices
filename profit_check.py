import pandas as pd, json, datetime as dt, numpy as np, matplotlib.pyplot as plt, math
import decimal as dec


def parse_date(date_str):
    # trim plus
    date_str = date_str[:-4]
    result = dt.datetime.strptime(date_str, "%b %d %Y %H")
    return result


def generate_trades_mean(price, number_of_trades):
    return mean_balance(price, number_of_trades)


def generate_trades_dummy(price, number_of_trades):
    return [price] * number_of_trades


def parse_prices(price_dict_raw, how_gen_trade="mean"):
    """prices are of form: [timestamp, price, number of trades].  Parse into [timestamp,price] x numer of trades"""
    d_prices = dict()
    for row in price_dict_raw["prices"]:

        price_date = parse_date(row[0])
        price = round(float(row[1]), 2)

        number_of_trades = int(row[2])

        # if how_gen_trade=="mean":
        # generate possible trade values based on mean
        #    generated_trades = generate_trades_mean(price, number_of_trades)
        # else:
        #    generated_trades = generate_trades_dummy(price, number_of_trades)

        generated_trades = generate_trades_mean(price, number_of_trades)

        # add rows to the dictionary for each time a trade occurred
        for i in range(0, len(generated_trades)):
            # add a microsecond to each date to differentiate each trade
            micro_t = dt.timedelta(microseconds=1 * i)
            price_key = price_date + micro_t
            d_prices[price_key] = generated_trades[i]

    return d_prices


def list_mean(l):
    if len(l) == 0:
        return 0
    return sum(l) / float(len(l))


def mean_balance(mean, n):
    total = 0
    numbers = []

    if n == 1:
        return [mean]

    # round floating point at 14th decimal
    mean_d = dec.Decimal(mean).quantize(dec.Decimal('.00000000000001'), rounding=dec.ROUND_HALF_UP)

    mean_round_down = mean_d.quantize(dec.Decimal('.01'), rounding=dec.ROUND_DOWN)
    mean_round_up = mean_d.quantize(dec.Decimal('.01'), rounding=dec.ROUND_UP)
    if mean_d == mean_round_down or mean_d == mean_round_up:
        return [mean] * n
    # print("mean {} meanup {} meandown {}".format(mean_d,mean_round_up, mean_round_down))
    for i in range(0, n):

        mu = list_mean(numbers)

        if len(numbers) < 1:
            new_num = mean_round_down \
                if abs(mean_round_down - mean_d) < abs(mean_round_up - mean_d) \
                else mean_round_up
        elif mu < mean:
            new_num = mean_round_up
        else:
            new_num = mean_round_down

        numbers.append(float(new_num))
        total += new_num

        # print(list_mean(numbers))
    return numbers


def price_histogram_data(price_history_input, date_start=None):
    his = dict()
    date_filter = date_start
    if date_filter is None:
        date_filter = dt.datetime.min

    for i in sorted(price_history_input.keys()):
        val = price_history_input[i]
        if i > date_filter:

            if val in his:
                his[val] += 1
            else:
                his[val] = 1
    return his


class PriceHistory():
    def __init__(self, price_json):
        self.price_dict = price_json
        self.price_history = parse_prices(self.price_dict)


    def get_histogram(self, start_date=None):
        return price_histogram_data(self.price_history, start_date)

    def get_histogram_24hr(self, start_date=None):
        start_date = dt.datetime.today() if start_date is None else start_date
        past_24_hrs = start_date - dt.timedelta(hours=24)
        return price_histogram_data(self.price_history, past_24_hrs)

    def get_histogram_time_period(self, end_date=dt.datetime.now(), prior_period=dt.timedelta(weeks=1)):
        prior_date = end_date - prior_period
        return price_histogram_data(self.price_history, prior_date)

    def get_price_probability(self, end_date=dt.datetime.now(), prior_period=dt.timedelta(weeks=1)):
        price_dist = self.get_histogram_time_period(end_date=end_date, prior_period=prior_period)
        price_prob = dict()
        total_vals = sum([i for i in price_dist.values()])
        for i in price_dist:
            price_prob[i] = price_dist[i] / total_vals * 100

        return price_prob


    def get_price_dataframe(self, end_date=dt.datetime.now(), days=14):
        df=pd.DataFrame.from_dict(self.price_history,orient="index")

        return df.sort_index()

    def get_price_histogram_dataframe(self, end_date=dt.datetime.now(), days=14):
        prior_period = dt.timedelta(days=days)
        price_dist = self.get_histogram_time_period(end_date=end_date, prior_period=prior_period)
        df = pd.DataFrame.from_dict(price_dist, orient="index")
        df.columns = ["trades"]
        total_vals = sum([i for i in price_dist.values()])
        for i in price_dist:
            df.loc[i, "probability"] = price_dist[i] / total_vals * 100

        return df.sort_index()

    def print_probability_and_numbers(self, days=14):
        htp = (self.get_histogram_time_period(prior_period=dt.timedelta(days=days)))
        gpp = (self.get_price_probability(prior_period=dt.timedelta(days=days)))

        for i in sorted(htp):
            print("{0}: {1} - {2:0.2f}%".format(i, htp[i], gpp[i]))


if __name__ == "__main__":
    import steam_load as sl

    s = sl.SteamLoad()
    cardname = "269670-Daydream (Trading Card)"
    h = s.card_history_json(cardname)

    # p = PriceHistory(h).print_probability_and_numbers(7)
    df = PriceHistory(h).get_price_histogram_dataframe(days=7)
    df["card_name"] = cardname
    print(df)
