# -*- coding: utf-8 -*-
"""
Mirror of src/services/eda_engine.py for backend/services package compatibility.
"""
import sys
import os

try:
    from src.services.eda_engine import *
except ImportError:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from src.services.eda_engine import *
