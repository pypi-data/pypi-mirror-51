# activity stream utils

# pull_tiles_data(sql_query, dbutils)
# validate_as_data_quality(sql_query, dates, dbutils)


# activity stream utils: imports
from pyspark.sql import SparkSession
import socket
# local dependences
from .util import write_parquet_to_s3, read_parquet_from_s3, date_to_string
from .constants import S3_ROOT

# --------------- accessing activity stream data utils ---------------


spark = SparkSession.builder.getOrCreate()


def pull_tiles_data(sql_query, dbutils):
    """
    provide SQL query, will return spark df of results
    """

    def tiles_redshift_jdbcurl_fetch(dbutils=dbutils): # noqa
        socket.setdefaulttimeout(3)
        s = socket.socket()
        rs = 'databricks-tiles-redshift.data.mozaws.net:5432'
        hostname, port = rs.split(":")
        port = int(port)
        address = socket.gethostbyname(hostname)
        print(address)
        try:
            s.connect((address, port))
            print("connected")
        except Exception as e:
            print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
        finally:
            s.close()
        jdbcurl = ("jdbc:postgresql://{0}:{1}" +
                   "/tiles?user={2}" +
                   "&password={3}&ssl=true" +
                   "&sslMode=verify-ca"
                   ).format(hostname,
                            port,
                            dbutils.secrets.get('tiles-redshift', 'username'),
                            dbutils.secrets.get('tiles-redshift', 'password'))
        return jdbcurl

    TEMPDIR = "s3n://mozilla-databricks-telemetry-test/tiles-redshift/_temp"
    JDBC_URL = tiles_redshift_jdbcurl_fetch()

    df = spark.read.format("com.databricks.spark.redshift")\
                   .option("forward_spark_s3_credentials", True)\
                   .option("url", JDBC_URL).option("tempdir", TEMPDIR)\
                   .option("query", sql_query)\
                   .load()
    return df


def validate_as_data_quality(sql_query, dates, dbutils):
    """
    for a given query and range/list of dates, check if
    databricks can pull the data into parquet at all
    most likely outcomes are:
        1) data pulls correctly (the counts are correct)
        2) spark can't communicate with the redshift db
           at which point you just wait / switch clusters /
           try again.
        3) pull fails and there will be a long py4 message
    """
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    TEMP_DATA_DUMP = S3_ROOT + "activity-stream/temp-testing-dir.parquet"
    print("using {} as temporary directory".format(TEMP_DATA_DUMP))
    print("checking {} dates".format(str(dates)))
    for date in dates:
        if type(date) != str:
            date = date_to_string(date, format='%Y-%m-%d')
        q = sql_query.format(START_DT=date,
                             END_DT=date)
        print("\n\n\n")
        print("--------------------------------------------------")
        print(date)
        print("--------------------------------------------------")
        print("checking:")
        print(q)
        try:
            test_data = pull_tiles_data(q, dbutils)
            test_count = test_data.count()

            write_parquet_to_s3(test_data, TEMP_DATA_DUMP)
            confirm_data = read_parquet_from_s3(TEMP_DATA_DUMP)

            confirm_count = confirm_data.count()
            if test_count == confirm_count:
                print("{}: data pulled and counts confirmed".format(date))
            elif test_count != confirm_count:
                print("{}: counts don't match").format(date)
        except Exception as E:
            print("{}: has error".format(date))
            print(E)


# --------------- parsing activity stream data utils ---------------

def as_experiment_field(shield_ids):
    """
    parse the shield_id field in activity stream data and return standard telemetry
    experiments field
    """
    try:
        if shield_ids and shield_ids != 'n/a':
            experiments = shield_ids.split(';')
            experiments = [exp for exp in experiments if exp != '']
            exp_dict = {}
            for i in experiments:
                exp_dict[i.split(':')[0]] = i.split(':')[1]
            if exp_dict != {}:
                return exp_dict
    except:  # noqa
        return


def as_pref_setting(user_prefs, setting):
    """
    parse as user_pref field (in sessions)
    and return condition for single setting
        setting is int for setting (see as docs)
    note - returns null if:
        1) null value
        2) value is less then 1
        3) value can't be coerced into integer
    """
    if type(user_prefs) == int and user_prefs >= 0:
        if user_prefs & setting == 0:
            return False
        if user_prefs & setting > 0:
            return True


def as_health_default_homepage(value):
    """
    parse value (in as health pings) to see if homepage
    is set to default
    note - returns null if:
        1) null value
    """
    if value:
        value = str(value)
        if value in ['0', '4', '8', '12']:
            return True
        else:
            return False


def as_health_default_newtab(value):
    """
    parse value (in as health pings) to see if newtab
    is set to default
    note - returns null if:
        1) null value
    """
    if value:
        value = str(value)
        if value in ['0', '1', '2', '3']:
            return True
        else:
            return False
