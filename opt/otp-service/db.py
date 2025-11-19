import mysql.connector
import configparser

CONFIG_FILE = "/etc/otp-service/db.conf"

def get_connection():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    db = config["database"]

    return mysql.connector.connect(
        host=db.get("host", "localhost"),
        port=db.getint("port", 3306),
        user=db["user"],
        password=db["password"],
        database=db["database"]
    )
