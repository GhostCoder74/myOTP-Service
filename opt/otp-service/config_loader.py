# -----------------------------------------------------------------------------
# Project:        myOTP-Service
# File:           config_loader.py
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
import configparser
import socket

def load_issuer():
    config = configparser.ConfigParser()
    config.read('/etc/otp-service/otp.conf')

    hostname = socket.gethostname()
    fqdn = socket.getfqdn()

    # Domains aus Config prüfen
    if config.has_section('Domains'):
        for domain, issuer in config.items('Domains'):
            if fqdn.endswith(domain) or hostname.endswith(domain):
                return issuer

    # Fallback
    return config.get('General', 'default_issuer', fallback="OTP-Service")

