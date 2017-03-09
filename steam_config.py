"""Import configuration settings for Steam"""
import configparser as cfg_parser


class MyConfig():
    def __init__(self, filepath="../Private/config.ini"):
        config = cfg_parser.ConfigParser(interpolation=None)
        with open(filepath) as f:
            config.read_file(f)

        self.api_key = config['STEAM']['API_KEY']
        self.rev_robot = config["STEAM"]["DEFAULT_PWD"]
        self.rev_robot_u = config["STEAM"]["DEFAULT_USER"]
        self.db_connstr = config["STEAM"]["DATABASE_CONNECTION"]
        self.db_price_table=config["STEAM"]["PRICE_TABLE"]

if __name__ == "__main__":
    cfg_t = MyConfig("../Private/config.ini")
    print(len(cfg_t.api_key))
