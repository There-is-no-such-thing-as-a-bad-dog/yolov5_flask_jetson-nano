import pymysql


def send(action):
    conn = pymysql.connect(host='localhost', user='test',
                           password='1234', db='dog')
    cursor = conn.cursor()

    sql = "insert into behavior (action) values (%s)"
    cursor.execute(sql, (action))

    conn.commit()
    conn.close()
    # print(action + "has inserted successful")
