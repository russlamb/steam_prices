import sqlalchemy as sa, psycopg2 as psy, pandas as pd, numpy as np, datetime as dt
import steam_config as stc
import odo
from os.path import expanduser


def test_load():
    engine = sa.create_engine(
        stc.MyConfig().db_connstr,
        isolation_level="READ COMMITTED"
    )
    conn=engine.connect()
    res = conn.execute("select 1 as x")
    df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))
    print("{} - Start".format(dt.datetime.now()))
    df.to_sql('dummy_data',engine,if_exists="replace", chunksize=5000)
    print("{} - End".format(dt.datetime.now()))



default_connection=stc.MyConfig().db_connstr

def load_prices_to_db(filename):
    odo.odo(filename, stc.MyConfig().db_price_table, dshape='var * {price_date: ?datetime, price_value: ?float64, card_value: ?string, app_name: ?string, app_id:?string}')


class PostgreLoad():
    def __init__(self, connection_string=default_connection):
        self.engine = sa.create_engine( connection_string, isolation_level="READ COMMITTED")
        self.conn = self.engine.connect()

    def save_dataframe(self, df, table, if_exists="append"):
        df.to_sql(table, self.engine, if_exists=if_exists, chunksize=1000)

    def clear_table(self, table):
        res = self.conn.execute("delete from {}".format(table))
        print(res.rowcount)

    def load_price_df(self):
        df = pd.read_sql("select * from steam_prices")


if __name__=="__main__":
    #test_load()
    #PostgreLoad().clear_table("dummy_data")
    #test_load()
    #load_prices_to_db("../data/prices.csv")
    file=expanduser("~/data/prices_new.csv")
    load_prices_to_db(file)