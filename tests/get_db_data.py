import pyodbc

server = 'LAPTOP-0DD1LKN9\SQLEXPRESS'
database = 'SwagLabs'
query = 'SELECT username, userpassword, assertion FROM Users'

def get_query_data(server, database, query):
    db = pyodbc.connect('Driver={SQL Server};Server=%s;Database=%s;Trusted_Connection=yes;' % (server, database))
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

login_form_parameters = get_query_data(server, database, query)
