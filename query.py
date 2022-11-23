from fcm import fcm_send
import pymysql
import json
import collections

''' select로 가장 최근 것을 가져와서 액션이 같다면 end time update, 다르다면 insert '''

abnormal_behavior = ['eat', 'bark', 'walk']


def update(action):
    conn = pymysql.connect(host='localhost', user='dog',
                           password='dog', db='dog')
    cursor = conn.cursor()

    sql = "select * from behavior order by end desc limit 1;"
    cursor.execute(sql)
    result = cursor.fetchall()

    if len(result) == 0:
        sql = "insert into behavior values (%s,NOW(),NOW())"
        cursor.execute(sql, (action))
    else:
        if result[0][0] == action:
            sql = "update behavior set end=NOW() where action=%s and start=%s"
            cursor.execute(sql, (action, result[0][1]))
        else:
            if action in abnormal_behavior:
                fcm_send(action)
            sql = "insert into behavior values (%s,NOW(),NOW())"
            cursor.execute(sql, (action))

    conn.commit()
    conn.close()


''' 데이터 시각화를 위한 쿼리문 '''


def select():
    conn = pymysql.connect(host='localhost', user='dog',
                           password='dog', db='dog')
    cursor = conn.cursor()

    sql = "select action, sum(end-start+1) from behavior group by action"
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        tmp = collections.OrderedDict()
        tmp['action'] = row[0]
        tmp['time'] = int(row[1])
        data.append(tmp)
    return json.dumps(data)
