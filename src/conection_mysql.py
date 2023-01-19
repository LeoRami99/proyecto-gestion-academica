from pymysql import connect
from dotenv import load_dotenv
from os import environ


def obtener_conexion():
    load_dotenv()
    host = environ.get('HOST')
    user = environ.get('USUARIO')
    password = environ.get('PASSWORD')
    database = environ.get('DATABASE')
    try:
        conn = connect(host=host, user=user, password=password, database=database)
        # conn = connect(host = os.getenv('HOST'), user = os.getenv('USER'), password = os.getenv('PASSWORD'), database = os.getenv('DATABASE'))
        return conn
    except Exception as e:
        print(e)
        return None