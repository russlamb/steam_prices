import pandas as pd, matplotlib.pyplot as plt, json, datetime as dt
import steam_load as sl

def get_test_data():

    with open("download.json","r") as f:
        j=f.read()

    return j


def plot_price_history():
    test_data = json.loads(get_test_data())
    # print(test_data)
    plt.style.use('ggplot')
    # prices=steam_load.SteamLoad().card_prices("290890-Ratter")
    prices = sl.get_price_data(test_data)
    df = sl.get_price_dataframe(prices)
    df = sl.get_filtered_prices(df, min_date=dt.datetime(2015, 3, 6))

    print(df)
    plt.figure()
    df.plot()

def price_histogram_data():
    prices = sl.SteamLoad().card_prices("292410-RX-7")

    yval = dict()
    prices_raw = list(prices.values())
    for i in range(0, len(prices_raw)):
        price = prices_raw[i]
        if price in yval.keys():

            yval[price] = yval[price] + 1
        else:
            yval[price] = 0
    return yval


def plot_histogram(yval):


    #plt.plot(yval)
    #plt.hist(list(yval.values()), 50, normed=1, facecolor='g', alpha=0.75)
    df = pd.DataFrame.from_dict(yval,orient="index")

    return plt.bar(list(yval.keys()), list(yval.values()), 1.0, color='g')

if __name__=="__main__":
    #print(df)
    #plt.figure()
    x=plot_histogram(price_histogram_data())
    plt.figure()
    plt.show()