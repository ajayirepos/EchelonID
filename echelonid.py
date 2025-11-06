import pandas as pd
from datetime import datetime
import os
import json
import argparse

# make sure output folder exists
os.makedirs("output", exist_ok=True)

# load users and roles
users = pd.read_csv("users.csv")
roles = pd.read_csv("roles.csv")

# load policies if present
policies = []
if os.path.exists("access_policies.json"):
    with open("access_policies.json") as f:
        data = json.load(f)
        policies = data.get("policies", [])

log_path = "output/lifecycle_log.txt"
log = open(log_path, "a")


def log_action(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    log.write(line)
    print(msg)


def joiner(user_id, name, dept, role):
    """create a new active user"""
    global users
    users.loc[len(users)] = [user_id, name, dept, role, "Active"]
    log_action(f"JOINER: Created account for {name} ({user_id}) in {dept} with role {role}")


def mover(user_id, new_role):
    """update user role"""
    global users
    user = users[users["user_id"] == user_id]
    if not user.empty:
        old_role = user.iloc[0]["role"]
        users.loc[users["user_id"] == user_id, "role"] = new_role
        log_action(f"MOVER: Updated {user_id} from {old_role} -> {new_role}")
    else:
        log_action(f"MOVER: User {user_id} not found")


def leaver(user_id):
    """terminate user account"""
    global users
    if user_id in list(users["user_id"]):
        users.loc[users["user_id"] == user_id, "status"] = "Terminated"
        log_action(f"LEAVER: Disabled access for {user_id}")
    else:
        log_action(f"LEAVER: User {user_id} not found")


def export_access_review():
    """export current users for access review"""
    users.to_csv("output/access_review_report.csv", index=False)
    log_action("Exported access review report to output/access_review_report.csv")


def export_policy_alignment():
    """match active users to policies by department + role"""
    rows = []
    for _, u in users.iterrows():
        if u["status"] != "Active":
            continue
        dept = u["department"]
        role = u["role"]

        expected = []
        for p in policies:
            if p.get("department") == dept and p.get("role") == role:
                expected.extend(p.get("entitlements", []))

        rows.append(
            {
                "user_id": u["user_id"],
                "full_name": u["full_name"],
                "department": dept,
                "role": role,
                "expected_entitlements": "|".join(expected)
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv("output/policy_alignment_report.csv", index=False)
    log_action("Exported policy alignment report to output/policy_alignment_report.csv")


def enforce_role_based_access():
    """
    If a user is Terminated, remove their entitlements (simulate deprovisioning).
    Creates output/deprovisioned_users.csv
    """
    deprovisioned = []
    for _, u in users.iterrows():
        if u["status"] == "Terminated":
            deprovisioned.append({
                "user_id": u["user_id"],
                "full_name": u["full_name"],
                "department": u["department"],
                "role": u["role"],
                "status": u["status"],
                "action": "All entitlements revoked"
            })
            log_action(f"DEPROVISION: Removed access for {u['full_name']} ({u['user_id']})")

    if deprovisioned:
        df = pd.DataFrame(deprovisioned)
        df.to_csv("output/deprovisioned_users.csv", index=False)
        log_action("Exported deprovisioned users to output/deprovisioned_users.csv")
    else:
        log_action("No terminated users to deprovision.")


def run_lifecycle():
    """simulate a daily identity run"""
    joiner("U004", "John Taylor", "IT", "DevOps")
    mover("U002", "Analyst")
    leaver("U003")
    export_access_review()
    enforce_role_based_access()


def run_policy():
    if policies:
        export_policy_alignment()
    else:
        log_action("No access_policies.json found, skipping policy alignment")


def run_audit_summary():
    """combine metadata into one audit JSON"""
    summary = {
        "total_users": len(users),
        "active_users": int((users["status"] == "Active").sum()),
        "terminated_users": int((users["status"] == "Terminated").sum()),
        "generated_reports": [f for f in os.listdir("output") if f.endswith(".csv") or f.endswith(".json")],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("output/audit_summary.json", "w") as f:
        json.dump(summary, f, indent=4)
    log_action("Exported audit summary to output/audit_summary.json")


def simulate_s3_export():
    """
    Simulates exporting audit files to an AWS S3 bucket by copying them to cloud_export/
    """
    export_dir = "cloud_export"
    os.makedirs(export_dir, exist_ok=True)
    for f in os.listdir("output"):
        if f.endswith(".csv") or f.endswith(".json"):
            src = os.path.join("output", f)
            dst = os.path.join(export_dir, f)
            with open(src, "rb") as s, open(dst, "wb") as d:
                d.write(s.read())
    log_action("Simulated S3 export of all audit artifacts to cloud_export/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EchelonID IGA demo with advanced features")
    parser.add_argument("--lifecycle", action="store_true", help="run joiner/mover/leaver + deprovisioning")
    parser.add_argument("--policy", action="store_true", help="run policy alignment against access_policies.json")
    parser.add_argument("--audit", action="store_true", help="generate audit_summary.json")
    parser.add_argument("--s3", action="store_true", help="simulate S3/cloud export")
    args = parser.parse_args()

    # default: run everything
    if not any([args.lifecycle, args.policy, args.audit, args.s3]):
        run_lifecycle()
        run_policy()
        run_audit_summary()
        simulate_s3_export()
    else:
        if args.lifecycle:
            run_lifecycle()
        if args.policy:
            run_policy()
        if args.audit:
            run_audit_summary()
        if args.s3:
            simulate_s3_export()

    log.close()
