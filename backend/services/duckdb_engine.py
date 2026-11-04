# -*- coding: utf-8 -*-
"""
Proxy to src.services.duckdb_engine for backwards compatibility with
backend/services/duckdb_engine.py specification.
"""
from src.services.duckdb_engine import (
    get_connection,
    get_filtered_fact_data,
    get_cascading_options,
    get_dynamic_ml_metrics,
    build_filter_clause
)

__all__ = [
    "get_connection",
    "get_filtered_fact_data",
    "get_cascading_options",
    "get_dynamic_ml_metrics",
    "build_filter_clause"
]

