# -----------------------------------------------------------------------------
# Project:        myOTP-Service
# File:           Makefile
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
# ============================================================
# myOTP-Service – Makefile
# Installs:
#   /opt/otp-service/*
#   /etc/otp-service/*
#   /etc/nginx/sites-available/otp-service.conf
#   /etc/nginx/snippets/otp-common.conf
#   /etc/systemd/system/otp-service.service
#
# Autor: Ghostcoder
# ============================================================

PREFIX       := /
OPT_DIR      := $(PREFIX)opt/otp-service
ETC_DIR      := $(PREFIX)etc/otp-service
NGINX_AVAIL  := $(PREFIX)etc/nginx/sites-available
NGINX_ENAB   := $(PREFIX)etc/nginx/sites-enabled
NGINX_SNIP   := $(PREFIX)etc/nginx/snippets
SYSTEMD_DIR  := $(PREFIX)etc/systemd/system

INSTALL_BIN  := install -m 755
INSTALL_ETC  := install -m 600

# ------------------------------------------------------------
all:
	@echo "Use: make install | uninstall | tree | show"

# ------------------------------------------------------------
install:
	@echo "📦 Installing myOTP-Service..."

	@mkdir -p "$(OPT_DIR)"
	@mkdir -p "$(ETC_DIR)"
	@mkdir -p "$(NGINX_AVAIL)"
	@mkdir -p "$(NGINX_ENAB)"
	@mkdir -p "$(NGINX_SNIP)"
	@mkdir -p "$(SYSTEMD_DIR)"

	@cp -r opt/otp-service/* "$(OPT_DIR)/"
	@$(INSTALL_ETC) etc/otp-service/*.conf "$(ETC_DIR)/"

	@$(INSTALL_ETC) etc/nginx/sites-available/otp-service.conf "$(NGINX_AVAIL)/"
	@ln -sf ../sites-available/otp-service.conf "$(NGINX_ENAB)/otp-service.conf"
	@$(INSTALL_ETC) etc/nginx/snippets/otp-common.conf "$(NGINX_SNIP)/"

	@$(INSTALL_ETC) etc/systemd/system/otp-service.service "$(SYSTEMD_DIR)/"

	@echo "✔ Installation complete!"

# ------------------------------------------------------------
uninstall:
	@echo "🗑 Removing myOTP-Service..."

	@rm -rf "$(OPT_DIR)"
	@rm -rf "$(ETC_DIR)"

	@rm -f  "$(NGINX_AVAIL)/otp-service.conf"
	@rm -f  "$(NGINX_ENAB)/otp-service.conf"
	@rm -f  "$(NGINX_SNIP)/otp-common.conf"

	@rm -f  "$(SYSTEMD_DIR)/otp-service.service"

	@echo "✔ Uninstalled."

# ------------------------------------------------------------
show:
	@echo "."
	@echo "├── etc"
	@echo "│   ├── nginx"
	@echo "│   │   ├── sites-available/otp-service.conf"
	@echo "│   │   ├── sites-enabled/otp-service.conf -> ../sites-available/otp-service.conf"
	@echo "│   │   └── snippets/otp-common.conf"
	@echo "│   └── otp-service"
	@echo "│       ├── db.conf"
	@echo "│       └── otp.conf"
	@echo "├── opt/otp-service"
	@echo "│   ├── app.py"
	@echo "│   ├── models.py"
	@echo "│   ├── db.py"
	@echo "│   ├── config_loader.py"
	@echo "│   ├── otp-adduser.py"
	@echo "│   ├── static/*.css"
	@echo "│   ├── static/logo/*.jpeg"
	@echo "│   └── venv/"
	@echo "└── systemd/system/otp-service.service"

# ------------------------------------------------------------
tree:
	@echo "$(PREFIX)"
	@echo "├── etc"
	@echo "│   ├── otp-service"
	@echo "│   │   ├── db.conf"
	@echo "│   │   └── otp.conf"
	@echo "│   └── nginx"
	@echo "│       ├── sites-available"
	@echo "│       │   └── otp-service.conf"
	@echo "│       ├── sites-enabled"
	@echo "│       │   └── otp-service.conf -> ../sites-available/otp-service.conf"
	@echo "│       └── snippets/otp-common.conf"
	@echo "├── opt/otp-service"
	@echo "│       ├── app.py"
	@echo "│       ├── models.py"
	@echo "│       ├── db.py"
	@echo "│       ├── config_loader.py"
	@echo "│       ├── otp-adduser.py"
	@echo "│       ├── static/*.css"
	@echo "│       ├── static/logo/*.jpeg"
	@echo "│       └── venv/"
	@echo "└── systemd/system/otp-service.service"

# ------------------------------------------------------------
test:
	@make -n install

.PHONY: all install uninstall show tree test

