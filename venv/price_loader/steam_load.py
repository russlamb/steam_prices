import steam.webauth as wa, datetime as dt, numpy as np, pandas as pd, steam


import price_loader.steam_config as steam_config

#import postgre_connect as poc



def get_steam_session(u, p):
    user = wa.WebAuth(u, p)

    try:
        user.login()
    except wa.CaptchaRequired:
        capcha_val = input("Input captcha from {}".format(user.captcha_url))
        # ask a human to solve captcha
        user.login(captcha=capcha_val)
    except wa.EmailCodeRequired:
        email_code_val = input("Input email code: ")
        user.login(email_code=email_code_val)
    except wa.TwoFactorCodeRequired:
        guard_code = input("Steam Guard Code: ")
        user.login(twofactor_code=guard_code)

    return user


def get_inventory_json(webauthuser, username=None):
    """gets user inventory json"""
    s_id = steam.steamid.SteamID(webauthuser.steam_id)

    if username is not None:
        community_url = "http://steamcommunity.com/id/{}/".format(username)
        s_id = steam.steamid.SteamID().from_url(community_url)

    url = "http://steamcommunity.com/inventory/{}/753/6?l=english&count=5000".format(s_id)

    response = webauthuser.session.get(url)
    return response.json()


def get_inventory_list(webauthuser, username=None):
    inv_json = get_inventory_json(webauthuser, username)

    game_list = [i["market_hash_name"] for i in inv_json["descriptions"]]
    return game_list


def get_owned_games_json(webauthuser, api_key, username=None):
    """gets json of games owned by a user"""
    url = r"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    s_id = steam.steamid.SteamID(webauthuser.steam_id)

    if username is not None:
        community_url = "http://steamcommunity.com/id/{}/".format(username)
        s_id = steam.steamid.SteamID().from_url(community_url)

    payload = {
        "key": api_key,
        "steamid": s_id,
        "format": "json",
        "include_appinfo": 1
    }

    response = webauthuser.session.get(url, params=payload)

    results = response.json()
    return results


def get_owned_game_list(webauthuser, api_key, username=None):
    """gets list of games owned by a user """
    game_json = get_owned_games_json(webauthuser, api_key, username)
    game_dict = game_json["response"]["games"]
    app_list = dict()

    for i in game_dict:
        app_list[i["appid"]] = i["name"]

    return app_list


def get_all_card_games_json(webauthuser):
    """gets json of steam items"""
    url = "http://steamcommunity.com/market/appfilters/753"
    response = webauthuser.session.get(url)
    return response.json()


def get_all_card_games(webauthuser):
    """returnns a dictionary of application ids and game names (for games that have cards?)"""
    resp = get_all_card_games_json(webauthuser)
    searchme = resp["facets"]["753_Game"]["tags"]
    app_list = dict()
    for i in searchme:
        appid = int(i.split("_")[1])
        game_name = searchme[i]["localized_name"]

        app_list[appid] = game_name

    return app_list


def get_card_price_json(session, card_name):
    """Returns a dictionary of lists.  prices are in results["prices"].  lists are formatted [date, price, amount]"""
    url = "http://steamcommunity.com/market/pricehistory/"
    payload = {
        "country": "US",
        "currency": "1",
        "appid": "753",
        "market_hash_name": card_name
    }

    response = session.get(url, params=payload)
    results = response.json()
    return results


def parse_date(date_str):
    return dt.datetime.strptime(date_str[:-4], '%b %d %Y %H')


def get_price_data(webauthuser, card_name):
    """get date time pair with price"""
    price_history = get_card_price_json(webauthuser.session, card_name)
    prices = {parse_date(row[0]): row[1] for row in price_history["prices"]}
    return prices


def get_price_dataframe(prices):
    df = pd.DataFrame.from_dict(prices, orient="index")
    df = df.rename(columns={0: "price"})
    return df.sort_index()


def get_filtered_prices(df, max_date=None, min_date=None):
    df[np.abs(df["price"] - df["price"].mean()) <= (3 * df["price"].std())]

    if max_date is not None:
        df = df.loc[df.index <= max_date]

    if min_date is not None:
        df = df.loc[df.index >= min_date]

    return df


def create_price_pickle(username=None, filename="all_prices.pkl"):
    s = SteamLoad()
    p_list = s.inventory_prices(username)
    print("Starting pickle... {}".format(dt.datetime.now()))
    p_list.to_pickle(filename)
    print("Pickle complete ... {}".format(dt.datetime.now()))


def load_price_pickle(filename="all_prices.pkl"):
    print("Reading pickle... {}".format(dt.datetime.now()))
    read_pickl = pd.read_pickle("all_prices.pkl")
    print("Done")
    return read_pickl


class SteamLoad():
    def __init__(self, config_file=None):
        
        
        if config_file is None:
            print("no steam config file")
            stcfg = steam_config.MyConfig()
        else:
            print("reading file {}".format(config_file))
            stcfg=steam_config.MyConfig(config_file)
            
        u = stcfg.rev_robot_u
        p = stcfg.rev_robot
        api_key = stcfg.api_key

        self.u = u
        self.p = p
        self.api_key = api_key
        self.user = get_steam_session(u, p)
        self.session = self.user.session

    def card_history_json(self, card_name):
        return get_card_price_json(self.session, card_name)

    def card_prices(self, card_name):
        return get_price_data(self.user, card_name)

    def card_dataframe(self, card_name):
        return get_price_dataframe(self.card_prices(card_name))

    def card_price_filtered(self, card_name):
        return get_filtered_prices(self.card_dataframe(card_name))

    def owned_games(self, username=None):
        """gets list of owned games"""
        return get_owned_game_list(self.user, self.api_key, username)

    def get_all_cards(self):
        """Gets list of steam games"""
        return get_all_card_games(self.user)

    def get_inventory(self, username=None):
        return get_inventory_list(self.user, username)

    def load_prices_from_csv(self):
        pd.read_csv("prices.csv")
        
    


if __name__ == "__main__":


    # price_df=load_price_pickle()

    # print(price_df[price_df["card_name"]=="269670-Daydream (Trading Card)"])
    s=SteamLoad()
    #s.save_prices_to_csv("jahbreeze")
    s.load_prices_from_csv()