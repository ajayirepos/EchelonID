# 🧩 EchelonID — Identity Governance Administration Demo
!![EchelonID Dashboard](./output/screenshot.png)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)
![License](https://img.shields.io/badge/Project-Type:IGA-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

A lightweight Saviynt-style Identity Governance project built in Python.
Implements joiner–mover–leaver automation, policy alignment, LDAP simulation,
PKI certificate lifecycle monitoring, and Flask dashboard visualization.

# EchelonID — Mini Identity Governance Demo

A small, runnable identity governance (IGA) project built to mirror an **Identity Governance Administration Engineer** job description. It shows:

- user lifecycle (joiner → mover → leaver)
- directory / LDAP interaction
- PKI certificate lifecycle awareness
- audit-friendly outputs

All of it runs locally on macOS in a Python virtual environment (VS Code).

---

##  What this project does

1. **Lifecycle automation**  
   - Script: `echelonid.py`  
   - Loads users/roles from CSV  
   - Runs joiner, mover, and leaver actions  
   - Exports an **access review report** to `output/access_review_report.csv`  
   - Logs actions to `output/lifecycle_log.txt`

2. **Directory / LDAP simulation**  
   - Script: `ldap_sim.py`  
   - Creates a mock LDAP directory using `ldap3`  
   - Binds and lists users (Finance, Engineering)  
   - Proves “configure and maintain identity directories and LDAP”

3. **PKI certificate lifecycle check**  
   - Script: `cert_monitor.py`  
   - Generates short-lived certs for demo users  
   - Calculates days to expiry  
   - Writes `output/expired_certs_report.csv`  
   - Proves “monitor and manage PKI certificate lifecycle”

4. **Governance/policy layer (optional)**  
   - File: `access_policies.json`  
   - Shows separation of identity data vs. governance rules (Saviynt/EIC style)

---

##  Project structure

```text
EchelonID/
├── README.md
├── users.csv
├── roles.csv
├── access_policies.json     # optional policy layer
├── echelonid.py             # lifecycle / access review
├── ldap_sim.py              # directory / LDAP demo
├── cert_monitor.py          # PKI lifecycle demo
├── output/                  # audit artifacts (CSV + logs)
└── venv/                    # local Python virtual environment
