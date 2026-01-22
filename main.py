#!/usr/bin/env python3
"""
Bruite Force - Educational Web Security Testing Tool

Main entry point for the application.
This is the recommended way to run the tool.

⚠️ EDUCATIONAL USE ONLY ⚠️
This tool is designed for educational purposes and authorized security testing only.
"""

import sys
import os

# Add the package to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bruite_force.cli import main

if __name__ == "__main__":
    main()
