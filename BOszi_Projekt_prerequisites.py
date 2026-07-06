import sys
import subprocess

# Define your required packages here
REQUIRED_PACKAGES = ["numpy", "pandas", "yfinance", "scipy", "matplotlib", "datetime", "requests", "scikit-learn"]

def check_and_install():
    print("Checking prerequisites...")
    missing_packages = []

    # 1. Check what is missing
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    # 2. If packages are missing, install them
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing them now...")
        try:
            # sys.executable ensures it installs to the exact Python environment currently running
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("All packages installed successfully!")
        except Exception as e:
            print(f"Automatic installation failed: {e}")
            print(f"Please manually run: pip install {' '.join(missing_packages)}")
    else:
        print("All prerequisites are satisfied!")

# Run the function
check_and_install()
