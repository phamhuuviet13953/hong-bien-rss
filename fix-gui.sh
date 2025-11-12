#!/bin/bash
# Script fix GUI dependencies - Hong Bien RSS Tool

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Hong Bien RSS Tool - Fix GUI${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}This script will fix GUI dependencies issue${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed!${NC}"
    exit 1
fi

echo -e "${GREEN}[OK] Python installed${NC}"
python3 --version
echo ""

# Check/Create venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[INFO] Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}[OK] Virtual environment created${NC}"
    echo ""
fi

# Activate venv
echo -e "${BLUE}[INFO] Activating virtual environment...${NC}"
source venv/bin/activate

echo ""
echo -e "${BLUE}[INFO] Uninstalling old customtkinter...${NC}"
pip uninstall -y customtkinter || true

echo ""
echo -e "${BLUE}[INFO] Upgrading pip...${NC}"
python -m pip install --upgrade pip

echo ""
echo -e "${BLUE}[INFO] Installing dependencies with specific versions...${NC}"
pip install --upgrade --force-reinstall customtkinter==5.2.2
pip install --upgrade darkdetect Pillow

echo ""
echo -e "${BLUE}[INFO] Installing all requirements...${NC}"
pip install -r requirements.txt

echo ""
echo -e "${BLUE}[INFO] Removing old markers...${NC}"
rm -f venv/.gui_requirements_installed

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}[SUCCESS] GUI dependencies fixed!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "You can now run the GUI with: ${BLUE}./run-gui.sh${NC}"
echo -e "Or directly: ${BLUE}python gui.py${NC}"
echo ""
