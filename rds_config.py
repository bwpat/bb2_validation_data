
bb2_host = "bb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com"
bb2_username = "admin_bb2"
bb2_password = "3pX45n9MIGCm"
bb2_dbname = "bigblue-2"

#mysql -hbb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com -uadmin_bb2 -p3pX45n9MIGCm

# conn = pymysql.connect(host="bb2-dev.cluster-chyay8gb54w8.us-west-1.rds.amazonaws.com", user="admin_bb2", passwd="3pX45n9MIGCm", db="bigblue-2", connect_timeout=5,
#                 cursorclass=pymysql.cursors.DictCursor)

sqls = {
    "getDbCreds": """select cb.* from  accounts a join client_databases cb on cb.id=a.db_connection where cb.abbv <> ''; """,
    "dist": """select distinct
        map.distributor_seller_account as account_no,
        p.phone as phone,
        if(map.customer_id is not null,map.customer_id,if(map.distributor_purchaser_id is NULL,1041779,map.distributor_purchaser_id)) as customer_id
        from
        customer_distributor_map map
        join master_distributor m on m.master_abv=map.master_abv
        join distributor_phones p on p.master_distributor_id=m.id;""",
        # where
        # map.distributor_seller_account in (%s) and p.phone in (%s);""",

    "product": """select
        distinct
        map.upc_code as upc_code,
        p.phone as phone,
        map.distributor_product_id as product_id
        from
        product_distributor_map map
        join master_distributor m on m.master_abv=map.master_abv
        join distributor_phones p on p.master_distributor_id=m.id;""",
        # where p.phone = %s;""",

    "cust": """select distinct
        map.distributor_seller_account as account_no, p.phone
        from
        customer_distributor_map map
        join master_distributor m on m.master_abv=map.master_abv
        join distributor_phones p on p.master_distributor_id=m.id;""",
        # where p.phone = %s """,
    # "custValidationSql2": """ and map.distributor_seller_account in (%s);"""
    "replace": """replace INTO lambda_validation_data(row_key,row_data)
        VALUES(%s, %s)"""
}
