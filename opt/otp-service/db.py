# -----------------------------------------------------------------------------
# Project:        myOTP-Service
# File:           db.py
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
