#!/usr/bin/env bash

python3 -m venv venv
python_path=venv/bin/python3

${python_path} -m pip install --upgrade pyinstaller
${python_path} -m pip install --upgrade pywin32
${python_path} -m pip install --upgrade python-telegram-bot
${python_path} -m pip install --upgrade PyAutoGUI
${python_path} -m pip install --upgrade PyScreeze
${python_path} -m pip install --upgrade pywinauto
${python_path} -m pip install --upgrade opencv-python
${python_path} -m pip install --upgrade pywin32-ctypes
${python_path} -m pip install --upgrade python-dateutil
${python_path} -m pip install --upgrade openpyxl
${python_path} -m pip install --upgrade xlrd
${python_path} -m pip install --upgrade xlwt
${python_path} -m pip install --upgrade pytesseract