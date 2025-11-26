# -----------------------------------------------------------------------------
# Project:        myOTP-Service
# File:           models.py
# Author:         Christian Klose
# Email:          ghostcoder@gmx.de
# GitHub:         https://github.com/GhostCoder74/Set-Project-Headers (GhostCoder74)
# Copyright (c) 2025 Christian Klose
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of myOTP-Service.
# Do not remove this header.
# Header added by https://github.com/GhostCoder74/Set-Project-Headers
# -----------------------------------------------------------------------------
from passlib.hash import bcrypt
from db import get_connection

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    password_hash = bcrypt.hash(password)
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    cur.close()
    conn.close()

def get_user(username):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def set_otp_secret(username, secret):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET otp_secret=%s WHERE username=%s", (secret, username))
    conn.commit()
    cur.close()
    conn.close()

def update_last_login(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_login = NOW() WHERE username=%s", (username,))
    conn.commit()
    conn.close()
