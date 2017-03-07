import sqlalchemy as sa, psycopg2 as psy, pandas as pd, numpy as np, datetime as dt
import steam_config as stc

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
    test_load()
    PostgreLoad().clear_table("dummy_data")
    test_load()