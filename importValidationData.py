import json

import csv
import importlib
import pandas as pd
import numpy as np
import os
import hashlib
import decimal
import re
import redis
import logging

import pymysql
import rds_config

bb2_host = rds_config.bb2_host
bb2_username = rds_config.bb2_username
bb2_password = rds_config.bb2_password
bb2_dbname = rds_config.bb2_dbname


# mysql -hbb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com -uadmin_bb2 -p3pX45n9MIGCm


def importData():
    # TODO implement

    try:

        conn = pymysql.connect(host=bb2_host, user=bb2_username, passwd=bb2_password, db=bb2_dbname, connect_timeout=5,
                               cursorclass=pymysql.cursors.DictCursor)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    redisPass1 = 'f^@vLY^ao3gXlPl7'
    redisPass2 = 'tgOee0%^6GgqneO3'

    r = redis.Redis(host='clustercfg.bb2.fh5ygv.memorydb.us-west-1.amazonaws.com', port=6379, username='bb2-lambda',
                    password='f^@vLY^ao3gXlPl7', db=0)

    # clustercfg.bb2.fh5ygv.memorydb.us-west-1.amazonaws.com:6379

    pipe = r.pipeline()
    # print(event['Records'])
    # print(event['Records'])

    # cur = conn.cursor(pymysql.cursors.DictCursor)
    cur = conn.cursor()

    # print(cur)

    cur.execute(rds_config.sqls['getDbCreds'])

    dbList = cur.fetchall()

    # print(dbList)

    for dbCreds in dbList:

        try:
            dbConn = pymysql.connect(host=dbCreds["host"], user=dbCreds["db_user"], passwd=dbCreds["db_pass"],
                                     db=dbCreds["db_name"], connect_timeout=5,
                                     cursorclass=pymysql.cursors.DictCursor)
            # print(dbConn)
        except pymysql.MySQLError as e:
            # logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            # logger.error(e)
            print(e)
            print(dbCreds)

        currentConn = dbConn.cursor()

        for i in rds_config.sqls:
            dataToInsert = {}
            print(i)
            if i == 'getDbCreds':
                print("skipping " + i)
                continue

            currentConn.execute(rds_config.sqls[i])

            results = currentConn.fetchall();
            # print(results)
            for row in results:
                # print("key vals: " )
                # print(dbCreds["abbv"])
                # print(i)
                # print(row)
                key = i + ":<>:" + dbCreds["abbv"] + ":<>:" + (getKey(i, row))

                # if key not in dataToInsert:
                #     dataToInsert[key] = []

                # dataToInsert[key].append(getVal(i, row))
                pipe.set(key, json.dumps(getVal(i, row)))
                # print(r.get(key))

            print(dbCreds["abbv"] + " " + i + " done")
            pipe.execute()


        # print(dataToInsert)

    return {
        'statusCode': 200,
        'body': json.dumps('validation tables done')
    }


def getKey(type, row):
    # print("key type: " + type)

    key = row["phone"]

    if type == "dist":
        key = row["account_no"] + ":<>:" + row["phone"]

    # if there is no match for type, return phone
    return key


def getVal(type, row):
    # print("val type: " + type)
    switcher = {
        "dist": "customer_id",
        "product": "product_id",
        # "cust": row["account_no"],
    }
    # print("val swutcher selected: "+ switcher.get(type))

    # if there is no match for type, return account_no
    return row[switcher.get(type, "account_no")]



importData()