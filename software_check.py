import subprocess
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_installed_software():
    """
    Returns a list of tuples: (software_name, version)
    This example uses Windows PowerShell command to get installed software.
    """
    software_list = []
    try:
        # Use PowerShell command to list installed software
        command = [
            'powershell', 
            '-Command', 
            'Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | '
            'Select-Object DisplayName, DisplayVersion'
        ]
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        output = result.stdout
        
        # Parse PowerShell output
        for line in output.splitlines():
            match = re.match(r'^(?P<name>.+?)\s+(?P<version>[\d\.]+)$', line.strip())
            if match:
                name = match.group('name').strip()
                version = match.group('version').strip()
                software_list.append((name, version))
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error when getting installed software: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return software_list

def check_outdated_software(installed_software):
    """
    Dummy function to simulate checking for outdated software.
    In real scenarios, you would query vendor sites or vulnerability databases.
    Returns a list of tuples: (software_name, installed_version, latest_version)
    """
    outdated = []
    try:
        for name, version in installed_software:
            # Dummy logic: assume software is outdated if version < 2.0
            try:
                major_version = int(version.split('.')[0])
                if major_version < 2:
                    outdated.append((name, version, "2.0+ (Latest Version)"))  # Replace with real data
            except ValueError:
                logging.warning(f"Unable to parse version for software: {name}, version: {version}")
    except Exception as e:
        logging.error(f"Error checking outdated software: {e}")
    
    return outdated

if __name__ == "__main__":
    installed = get_installed_software()
    if installed:
        print("Installed Software:")
        for software in installed:
            print(f" - {software[0]}: {software[1]}")
        
        outdated = check_outdated_software(installed)
        print("\nOutdated Software:")
        if outdated:
            for software in outdated:
                print(f" - {software[0]}: Installed {software[1]}, Latest {software[2]}")
        else:
            print("All software is up-to-date!")
    else:
        print("No software found or unable to retrieve installed software.")
