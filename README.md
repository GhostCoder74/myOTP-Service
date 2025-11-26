# myOTP-Service – Lightweight One-Time-Passcode Web Service

<p align="center">
  <img src="opt/otp-service/static/logo/myOTP-Service-Logo.jpeg" alt="myOTP-Service logo" width="280">
</p>

The **myOTP-Service** is a lightweight and extensible web-based One-Time-Passcode (OTP) system.  
It provides user registration, QR-code generation, OTP validation, and database-backed user management.

The service is designed to run behind **Nginx** and can be managed using a **systemd service unit**.  
All configuration files, database parameters, and runtime environment files are cleanly separated.

---

# ✨ Features

- Web-based OTP registration workflow
- QR-code generation via templates
- SQLite / MySQL backend (configurable)
- Easy user management via CLI tool `otp-adduser.py`
- Flask-based web backend (`app.py`)
- Nginx integration with reusable `snippets/otp-common.conf`
- Production-ready systemd service file
- Fully isolated Python virtual environment (venv)
- Customizable CSS themes

---

# ✅ Supports Authenticators

This service supports all common TOTP-based authenticators.
The following apps have been tested and verified:

- itwarden – fully compatible (TOTP)
- oogle Authenticator – fully compatible
- icrosoft Authenticator – fully compatible

Any other TOTP-compatible authentication app should work as well.

---

# 📁 Directory Structure

After installation, the system files are located in:
```bash
/opt/otp-service/
├── app.py
├── config_loader.py
├── db.py
├── models.py
├── otp-adduser.py
├── requirements.txt
├── static
│   ├── default.css
│   ├── example1.css
│   ├── example2.css
│   ├── example3.css
│   ├── example4.css
│   ├── example5.css
│   └── qrcodes
├── templates
│   └── register.html
└── venv

```

# Configuration:
```bash
/etc/otp-service/
├── otp.conf
└── db.conf
```
# Nginx:
```bash
/etc/nginx/
├── sites-available
│   └── otp-service.conf
├── sites-enabled
│   └── otp-service.conf -> ../sites-available/otp-service.conf
└── snippets
    └── otp-common.conf
```

# Systemd unit:
```bash
/etc/systemd/system/
└── otp-service.service
```

---

# 📦 Installation

### Standard installation
```bash
sudo make install
```
### Force installation (overwrite all files)
```bash
sudo make install FORCE=1
```
### Dry-run (simulate installation, no changes applied)
```bash
make install DRY_RUN=1
```

### Dry-run + force (simulate overwrites)
```bash
make install DRY_RUN=1 FORCE=1
```

# 🛠 Systemd Management
```bash
sudo systemctl start otp-service
sudo systemctl enable otp-service
sudo systemctl restart otp-service
sudo systemctl status otp-service
```

# 🌐 Nginx Setup
## After installation, test the configuration:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

# 👤 User Management
## Add a new OTP user:
```bash
sudo /opt/otp-service/venv/bin/python /opt/otp-service/otp-adduser.py --username alice

# 🗄 Database
## Import the default database:
``` bash
sudo mysql < sql.dump
# (or SQLite depending on configuration)
```
## 📝License

### Licensed under GPL-3.0-or-later

See: [LICENSE](https://www.gnu.org/licenses/#GPL)
