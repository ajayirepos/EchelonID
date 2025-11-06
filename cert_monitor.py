# PKI Certificate Lifecycle Simulation
# Demonstrates monitoring and management of certificate expiry for IGA demo

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os

# make sure output folder exists
os.makedirs("output", exist_ok=True)

users = ["Jane Doe", "Mark Smith", "John Taylor"]

cert_report_lines = []
for user in users:
    # generate a short-lived demo cert
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, user)])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=15))
        .sign(key, hashes.SHA256())
    )

expiry = cert.not_valid_after_utc.replace(tzinfo=None)
days_left = (expiry - datetime.utcnow()).days
line = f"{user},{expiry.date()},{days_left}"

print(line)
cert_report_lines.append(line)

# write audit report
with open("output/expired_certs_report.csv", "w") as f:
    f.write("user,expiry_date,days_left\n")
    for line in cert_report_lines:
        f.write(line + "\n")

print("PKI report written to output/expired_certs_report.csv")
