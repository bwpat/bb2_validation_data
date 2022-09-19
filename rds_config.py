
bb2_host = "bb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com"
bb2_username = "admin_bb2"
bb2_password = "3pX45n9MIGCm"
bb2_dbname = "bigblue-2"

#mysql -hbb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com -uadmin_bb2 -p3pX45n9MIGCm

# conn = pymysql.connect(host="bb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com", user="admin_bb2", passwd="3pX45n9MIGCm", db="bigblue-2", connect_timeout=5,
#                 cursorclass=pymysql.cursors.DictCursor)

sqls = {
    "getDbCreds": """select cb.* from  accounts a join client_databases cb on cb.id=a.db_connection where cb.abbv <> ''; """,
    "dist": """select
            distinct
            phone
            from
            distributor_phones
            where
            phone is not null and phone<>'';""",

    "product": """select distinct
            map.distributor_seller_account as account_no
            from
            customer_distributor_map map
            join master_distributor m on m.master_abv=map.master_abv
            join distributor_phones p on p.master_distributor_id=m.id
            where p.phone = %s;""",
        # where p.phone = %s;""",

    "cust": """select
            distinct
            map.distributor_product_id as product_id
            from
            product_distributor_map map
            join master_distributor m on m.master_abv=map.master_abv
            join distributor_phones p on p.master_distributor_id=m.id
            where
distributor_product_id is not null and p.phone = %s;""",
        # where p.phone = %s """,
    # "custValidationSql2": """ and map.distributor_seller_account in (%s);"""
    "replace": """replace INTO lambda_validation_data(row_key,row_data)
        VALUES(%s, %s)"""
}
