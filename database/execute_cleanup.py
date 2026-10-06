import os

approved_deletions = [
    r"D:\Mini_Project\setup-custom-domain.bat",
    r"D:\Mini_Project\start-python-server.bat",
    r"D:\Mini_Project\start-server.bat",
    r"D:\Mini_Project\docker-compose.yml",
    r"D:\Mini_Project\server\python_server.py",
    r"D:\Mini_Project\server\server.js",
    r"D:\Mini_Project\server\package.json",
    r"D:\Mini_Project\server\Dockerfile",
    r"D:\Mini_Project\scripts\launch_microsip.py",
    r"D:\Mini_Project\scripts\init_sqlite_db.py",
    r"D:\Mini_Project\scripts\deploy_vapi_assistant.py",
    r"D:\Mini_Project\scripts\setup_vapi_webhook.py",
    r"D:\Mini_Project\vapi\vapi_live_tunnel_config.json"
]

removed_count = 0
for f in approved_deletions:
    if os.path.exists(f):
        try:
            os.remove(f)
            removed_count += 1
            print(f"[TASK 1 CLEANUP] Removed: {f}")
        except Exception as e:
            print(f"[TASK 1 ERROR] {f}: {e}")

print(f"[TASK 1 SUCCESS] Completed deletion of {removed_count} approved obsolete files.")
