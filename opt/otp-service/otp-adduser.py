"""
Script for creating a user for the OTP service
Uses the DB credentials from /etc/otp-service/db.conf
"""

import configparser
import sys
import mysql.connector
from getpass import getpass
from passlib.hash import bcrypt
import pyotp
import qrcode
import os

DB_CONF = "/etc/otp-service/db.conf"
QR_DIR = "/opt/otp-service/static/qrcodes"

def load_db_config():
    config = configparser.ConfigParser()
    config.read(DB_CONF)
    return {
        'host': config.get('database', 'host', fallback='localhost'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <username>")
        sys.exit(1)

    username = sys.argv[1]

    password = getpass(f"Password for {username}: ")[:72]  # Bcrypt max 72 bytes
    password_hash = bcrypt.hash(password)

    # Generate OTP secret
    secret = pyotp.random_base32()

    # Connect DB
    db_config = load_db_config()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create user in DB
    cursor.execute("""
        INSERT INTO users (username, password_hash, otp_secret)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE password_hash=%s, otp_secret=%s
    """, (username, password_hash, secret, password_hash, secret))
    conn.commit()
    cursor.close()
    conn.close()

    # Generate QR-Code
    os.makedirs(QR_DIR, exist_ok=True)
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="MyOTPService"
    )
    img_path = os.path.join(QR_DIR, f"{username}.png")
    qrcode.make(otp_uri).save(img_path)

    print(f"User '{username}' successfully created.")
    print(f"Secret: {secret}")
    print(f"QR-Code saved under: {img_path}")
    print(f"OTP URI: {otp_uri}")

if __name__ == "__main__":
    main()
