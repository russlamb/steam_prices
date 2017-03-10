"""Import configuration settings for Steam"""
import configparser as cfg_parser, getpass, os


class MyConfig():
    def __init__(self, filepath="../Private/config.ini"):
        
        if not os.path.exists(filepath):
            print("file path {} not found".format(os.path.abspath(filepath)))
            self.api_key=getpass.getpass("STEAM API KEY:")
            self.rev_robot_u=getpass.getpass("STEAM USER:")
            self.rev_robot=getpass.getpass("STEAM PASS:")
            self.db_connstr =getpass.getpass("DB CONN STR:")
        else:
            print("steam_config path {}".format(os.path.abspath(filepath)))
            config = cfg_parser.ConfigParser(interpolation=None)
            with open(filepath) as f:
                config.read_file(f)
    
            self.api_key = config['STEAM']['API_KEY']
            self.rev_robot = config["STEAM"]["DEFAULT_PWD"]
            self.rev_robot_u = config["STEAM"]["DEFAULT_USER"]
            self.db_connstr = config["STEAM"]["DATABASE_CONNECTION"]

if __name__ == "__main__":
    cfg_t = MyConfig("../Private/config.ini")
    print(len(cfg_t.api_key))
