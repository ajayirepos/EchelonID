import pandas as pd
from datetime import datetime
import os

os.makedirs("output", exist_ok=True)


users = pd.read_csv("users.csv")
roles = pd.read_csv("roles.csv")


log_path = "output/lifecycle_log.txt"
log = open(log_path, "a")

def log_action(action: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.write(f"[{timestamp}] {action}\n")
    print(action)


def joiner(user_id, name, dept, role):
    global users
    users.loc[len(users)] = [user_id, name, dept, role, "Active"]
    log_action(f"JOINER: Created account for {name} ({user_id}) in {dept} with role {role}")

def mover(user_id, new_role):
    global users
    user = users[users["user_id"] == user_id]
    if not user.empty:
        old_role = user.iloc[0]["role"]
        users.loc[users["user_id"] == user_id, "role"] = new_role
        log_action(f"MOVER: Updated {user_id} role from {old_role} -> {new_role}")
    else:
        log_action(f"MOVER: User {user_id} not found")


def leaver(user_id):
    global users
    if user_id in list(users["user_id"]):
        users.loc[users["user_id"] == user_id, 'status'] = "Terminated"
        log_action(f"LEAVER: Disabled access for {user_id}")
    else:
        log_action(f"LEAVER: User {user_id} not found")


joiner("U004", "John Taylor", "IT", "DevOps")
mover("U002", "Analyst")
leaver("U003")

users.to_csv("output/access_review_report.csv", index=False)
log_action("Exported access review report to output/access_review_report.csv")

log.close()