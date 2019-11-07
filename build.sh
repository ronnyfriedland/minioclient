#!/bin/sh

pyinstaller --clean --onefile --workpath .tmp --specpath .tmp minioclient.py

rm -rf .tmp