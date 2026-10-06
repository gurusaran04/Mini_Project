import os

obsolete_files = [
    r"D:\Mini_Project\setup-custom-domain.bat",
    r"D:\Mini_Project\start-python-server.bat",
    r"D:\Mini_Project\start-server.bat"
]

for f in obsolete_files:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"[CLEANUP SUCCESS] Removed obsolete root file: {f}")
        except Exception as e:
            print(f"[CLEANUP ERROR] {e}")

print("[CLEANUP COMPLETE] Workspace cleaned of obsolete root files.")
