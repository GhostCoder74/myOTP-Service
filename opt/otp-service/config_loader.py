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

