import pymysql.cursors


def column_values_at_least(db_data, column, gt=1):
    connection = pymysql.connect(host=db_data.get('host'),
                                 user=db_data.get('username'),
                                 password=db_data.get('password'),
                                 db=db_data.get('dbname'))

    try:
        with connection.cursor() as cursor:
            existance_query = 'SELECT count(1) from ({}) as t where {} is not null and {} <> ""'.format(db_data.get('query'), column, column)
            sql = existance_query
            cursor.execute(sql)
            results = cursor.fetchone()
            if results[0] >= gt:
                return True
            else:
                return False
    finally:
        connection.close()
