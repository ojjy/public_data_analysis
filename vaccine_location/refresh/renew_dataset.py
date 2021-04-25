import pandas as pd
from sqlalchemy import create_engine
import pymysql
from apis.address import getlatlng_list_naver
from apis.get_key import get_apikey

def renew_data():
    df = pd.read_csv("../csv/vac210421.csv")
    check_error_addr(df)
    update_tables(df)
    write_csv()
    print("PASS")
    return "PASS"

# address error check at csv file
def check_error_addr(df):
    addr_list=[]
    for idx in range(len(df)):
        addr_list.append(df.loc[idx, "address"])
    addr_lon_list, addr_lat_list = getlatlng_list_naver(addr_list)
    print("Pass")
    return addr_list, addr_lon_list, addr_lat_list

# create table and update lat and lon
def update_tables(df):
    sql = """update vaccine_center  set longitude = %s, latitude = %s where index_num = %s"""
    dbcon = create_engine("mysql+pymysql://yejinjoc_test:yejinjoc_test@127.0.0.1/yejinjoc_testdb")
    conn = pymysql.connect(host='127.0.0.1', user='yejinjoc_test', password='yejinjoc_test', database='yejinjoc_testdb')
    cur = conn.cursor()
    df.to_sql(name='vaccine_center', con=dbcon, if_exists='replace')
    addr_list, addr_lon_list, addr_lat_list = check_error_addr(df)

    for idx, addr in enumerate(addr_list):
        # dbcon.execute(sql)
        # stmt = (
        #     update("vaccine_center").
        #     where("vaccine_center".index_num == idx).
        #     value(longitude=addr_lon_list[idx], latitude=addr_lat_list[idx])
        # )
        cur.execute(sql, (addr_lon_list[idx], addr_lat_list[idx], idx+1))
        conn.commit()

    cur.execute("select * from vaccine_center")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def write_csv():
    conn = pymysql.connect(host='127.0.0.1', user='yejinjoc_test', password='yejinjoc_test', database='yejinjoc_testdb')
    sql_query = pd.read_sql_query('''select * from vaccine_center''', conn)
    df = pd.DataFrame(sql_query)
    df.to_csv("../csv/test.csv", index=False)

if __name__ == "__main__":
    renew_data()
