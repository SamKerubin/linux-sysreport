#!/usr/bin/env bash

echo "Running venv..."

python3 -m venv venv
source "venv/bin/activate"

echo "Installing dependencies..."

pip install -e .

read -r -n 1 -p "Do you want to install sysreport globally (at '/usr/local/bin') in the system? Y/n: " global
echo ""

if [[ "$global" == "y" || "$global" == "Y" ]]; then
  echo "Installing globally at '/usr/local/bin'..."

  if [[ ! -d "/usr/local/bin" ]]; then
    echo "Error: Couldnt find the install directory '/usr/local/bin'" >&2
    
    echo "Installing normally..."
    pyinstaller --onefile --name=sysreport --distpath=. src/sysreport/core.py
  else
    echo "Creating final binary..."
    pyinstaller --onefile --name=sysreport --distpath=/usr/local/bin src/sysreport/core.py
  fi

else
  echo "Creating final binary..."
  pyinstaller --onefile --name=sysreport --distpath=. src/sysreport/core.py
fi

echo "Removing venv..."

rm -rf venv/*

echo "Installation complete"

