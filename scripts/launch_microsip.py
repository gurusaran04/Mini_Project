import os
import glob
import subprocess

downloads_path = r"C:\Users\Gurusaran\Downloads"
search_pattern = os.path.join(downloads_path, "*MicroSIP*")

found_files = glob.glob(search_pattern)

print("Found MicroSIP files:")
for f in found_files:
    print(f" - {f}")

# Try to launch the first executable found
exe_files = [f for f in found_files if f.endswith(".exe")]
if exe_files:
    target_exe = exe_files[0]
    print(f"\n🚀 Launching: {target_exe}")
    os.startfile(target_exe)
else:
    print("\n⚠️ No .exe file found. Searching entire downloads directory...")
