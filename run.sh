#!/bin/bash
# Hong Bien RSS Tool - Start Script for Linux/Mac

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}🔧 Hong Bien RSS Tool${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo -e "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python version: $PYTHON_VERSION${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo -e "${BLUE}Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.requirements_installed
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo -e "${YELLOW}⚠️  Configuration not found${NC}"
    echo -e "${BLUE}Running setup...${NC}"
    python setup.py

    if [ ! -f "config.json" ]; then
        echo -e "${RED}❌ Setup was not completed${NC}"
        exit 1
    fi
fi

# Start the bot
echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}🚀 Starting Hong Bien RSS Bot...${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

python rss_telegram.py
