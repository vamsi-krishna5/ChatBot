import pandas as pd
import ibm_db

def DatabaseAPI(book_id, mobile, pick_up, destination):
    dsn_hostname = "dashdb-txn-sbox-yp-lon02-04.services.eu-gb.bluemix.net"
    dsn_uid = "srn99133"
    dsn_pwd = "ggk@bm549cwr3pxg"
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "BLUDB"
    dsn_port = "50000"
    dsn_protocol = "TCPIP"

    dsn = ("DRIVER={0};" "DATABASE={1};" "HOSTNAME={2};" "PORT={3};" "PROTOCOL={4};" "UID={5};" "PWD={6};").format(
        dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

    connection=ibm_db.connect(dsn,"","")

    query="insert into booking_details (BOOK_ID,MOBILE,PICK_UP,DESTINATION) values ('{}','{}','{}','{}');".format(book_id,mobile,pick_up,destination)
    statement=ibm_db.exec_immediate(connection,query)

    ibm_db.close(connection)
    return


def CancelAPI(book_id):
    dsn_hostname = "dashdb-txn-sbox-yp-lon02-04.services.eu-gb.bluemix.net"
    dsn_uid = "srn99133"
    dsn_pwd = "ggk@bm549cwr3pxg"
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "BLUDB"
    dsn_port = "50000"
    dsn_protocol = "TCPIP"

    dsn = ("DRIVER={0};" "DATABASE={1};" "HOSTNAME={2};" "PORT={3};" "PROTOCOL={4};" "UID={5};" "PWD={6};").format(
        dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

    connection=ibm_db.connect(dsn,"","")

    query="delete from BOOKING_DETAILS where BOOK_ID={};".format(book_id)
    statement=ibm_db.exec_immediate(connection,query)

    ibm_db.close(connection)
    return


def DetailsAPI(book_id):
    dsn_hostname = "dashdb-txn-sbox-yp-lon02-04.services.eu-gb.bluemix.net"
    dsn_uid = "srn99133"
    dsn_pwd = "ggk@bm549cwr3pxg"
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "BLUDB"
    dsn_port = "50000"
    dsn_protocol = "TCPIP"

    dsn = ("DRIVER={0};" "DATABASE={1};" "HOSTNAME={2};" "PORT={3};" "PROTOCOL={4};" "UID={5};" "PWD={6};").format(
        dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

    connection=ibm_db.connect(dsn,"","")

    query="select * from booking_details where BOOK_ID={};".format(book_id)
    statement=ibm_db.exec_immediate(connection,query)
    result=ibm_db.fetch_both(statement)

    ibm_db.close(connection)
    return result

if __name__=="__main__":
    #DatabaseAPI(94851,'7989078662','Maharashtra','Bombay')
    result=DetailsAPI(94851)
    print(result)