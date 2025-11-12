#!/bin/bash
# Hong Bien RSS Tool - GUI Launcher for Linux/Mac

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}🖥️  Hong Bien RSS Tool - GUI${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"

# Check/Create venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate venv
source venv/bin/activate

# Install/Update dependencies
if [ ! -f "venv/.gui_requirements_installed" ]; then
    echo -e "${BLUE}📦 Installing GUI dependencies...${NC}"
    pip install --upgrade pip
    pip install --upgrade --force-reinstall customtkinter==5.2.2
    pip install -r requirements.txt
    touch venv/.gui_requirements_installed
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies ready${NC}"
fi

# Launch GUI
echo -e "${BLUE}🚀 Launching GUI...${NC}"
echo ""

python gui.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}❌ An error occurred!${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}If you see customtkinter errors, try running:${NC}"
    echo -e "   ${BLUE}./fix-gui.sh${NC}"
    echo ""
    echo -e "This will reinstall GUI dependencies."
    echo ""
fi
