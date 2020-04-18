import urllib

class Config(object):
    # Build the MSSQL ULR for SqlAlchemy
    params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=Cobartram016\TRABDSP10;DATABASE=BDVIAJE2;UID=tra-sap;PWD=12345.TS;')
    mssql_url = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_DATABASE_URI = mssql_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False