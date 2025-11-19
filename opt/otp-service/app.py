from fastapi import FastAPI, Form, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pyotp, qrcode, os, configparser
from passlib.hash import bcrypt
from models import create_user, get_user, set_otp_secret, update_last_login

# --- App Setup ---
app = FastAPI(title="My OTP Service")
security = HTTPBasic()

BASE_DIR = "/opt/otp-service"
QR_DIR = f"{BASE_DIR}/static/qrcodes"
CONFIG_PATH = "/etc/otp-service/otp.conf"
os.makedirs(QR_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")

# --- Config Loader ---
def load_domain_config(hostname: str):
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH)

    issuer = cfg["General"].get("issuer_default", "OTP-Service Default")
    css = cfg["General"].get("css_default", "/static/default.css")

    if "Domains" in cfg and hostname in cfg["Domains"]:
        val = cfg["Domains"][hostname]
        parts = [p.strip() for p in val.split("|")]
        if len(parts) >= 1:
            issuer = parts[0]
        if len(parts) >= 2:
            css = f"/static/{parts[1]}"
    return issuer, css

# --- Auth & Admin Checks ---
def require_auth(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username)
    if not user or not bcrypt.verify(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def require_admin(user=Depends(require_auth)):
    if not user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin rights required")
    update_last_login(user["username"])
    return user

# --- OTP Endpoints ---
@app.get("/generate/{username}")
def generate_otp(username: str, request: Request, user=Depends(require_auth)):
    db_user = get_user(username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    issuer, css_path = load_domain_config(request.headers.get("host", ""))

    secret = db_user["otp_secret"] or pyotp.random_base32()
    if not db_user["otp_secret"]:
        set_otp_secret(username, secret)

    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)
    img_path = f"{QR_DIR}/{username}.png"
    qrcode.make(otp_uri).save(img_path)

    return {
        "username": username,
        "issuer": issuer,
        "secret": secret,
        "otp_uri": otp_uri,
        "qrcode_url": f"/qrcode/{username}",
        "theme_css": css_path
    }

@app.get("/qrcode/{username}")
def get_qrcode(username: str, user=Depends(require_auth)):
    img_path = f"{QR_DIR}/{username}.png"
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="QR code not found")
    return FileResponse(img_path)

@app.get("/verify/{username}/{code}")
def verify_otp(username: str, code: str):
    db_user = get_user(username)
    if not db_user or not db_user["otp_secret"]:
        raise HTTPException(status_code=404, detail="User not found or OTP not set")
    totp = pyotp.TOTP(db_user["otp_secret"])
    return {"valid": totp.verify(code)}

# --- Admin Manager Page ---
@app.get("/manager", response_class=HTMLResponse)
def manager_page(request: Request, user=Depends(require_admin)):
    issuer, css_path = load_domain_config(request.headers.get("host", ""))
    html = f"""
    <html>
    <head>
        <title>{issuer} - Manager</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>{issuer} - Admin Manager</h1>
        <p>Welcome, {user['username']}</p>
        <ul>
            <li><a href="/manager/register">Register New User</a></li>
            <li><a href="/static/qrcodes/">View All QR Codes</a></li>
        </ul>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# --- Admin Register User Form ---
@app.get("/manager/register", response_class=HTMLResponse)
def register_form(request: Request, user=Depends(require_admin)):
    issuer, css_path = load_domain_config(request.headers.get("host", ""))
    html = f"""
    <html>
    <head>
        <title>{issuer} - Register User</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>{issuer} - Register New User</h1>
        <form method="post">
            <label>Username: <input type="text" name="username"/></label><br/>
            <label>Password: <input type="password" name="password"/></label><br/>
            <input type="submit" value="Create User"/>
        </form>
        <a href="/manager">Back to Manager</a>
    </body>
    </html>
    """
    return HTMLResponse(html)

@app.post("/manager/register", response_class=HTMLResponse)
def register_user_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user=Depends(require_admin)
):
    existing_user = get_user(username)
    if existing_user:
        return HTMLResponse(f"<h3>User {username} already exists!</h3><a href='/manager/register'>Back</a>")

    create_user(username, password, is_admin=False)
    return HTMLResponse(f"<h3>User {username} created!</h3><a href='/manager'>Back to Manager</a>")

