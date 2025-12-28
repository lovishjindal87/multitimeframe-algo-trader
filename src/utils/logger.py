"""
Logging utilities for the trading system.
"""

import logging
import os
from datetime import datetime
from typing import Optional
import sys

# Add project root to path for config access
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.config import LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (defaults to config LOG_LEVEL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    
    logger.setLevel(level or LOG_LEVEL)
    return logger


def log_trade_to_csv(filepath: str, timestamp: float, symbol: str, side: str, 
                     price: float, quantity: float, entry_price: Optional[float] = None,
                     exit_price: Optional[float] = None, pnl: Optional[float] = None,
                     metadata: Optional[dict] = None):
    """
    Log a trade to CSV file.
    
    Args:
        filepath: Path to CSV file
        timestamp: Trade timestamp
        symbol: Trading symbol
        side: Trade side (BUY/SELL)
        price: Execution price
        quantity: Trade quantity
        entry_price: Entry price
        exit_price: Exit price
        pnl: Profit and loss
        metadata: Additional metadata
    """
    import csv
    
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    
    file_exists = os.path.exists(filepath)
    file_empty = file_exists and os.path.getsize(filepath) == 0
    needs_header = not file_exists or file_empty
    
    if file_exists and not file_empty:
        try:
            with open(filepath, 'r') as f_check:
                first_line = f_check.readline().strip()
                expected_header = 'timestamp,symbol,side,price,quantity,entry_price,exit_price,pnl,metadata'
                if first_line != expected_header:
                    needs_header = True
        except Exception:
            needs_header = True
    
    with open(filepath, 'a', newline='') as f:
        fieldnames = [
            'timestamp', 'symbol', 'side', 'price', 'quantity',
            'entry_price', 'exit_price', 'pnl', 'metadata'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if needs_header:
            writer.writeheader()
        
        row = {
            'timestamp': timestamp,
            'symbol': symbol,
            'side': side,
            'price': price,
            'quantity': quantity,
            'entry_price': entry_price or '',
            'exit_price': exit_price or '',
            'pnl': pnl or '',
            'metadata': str(metadata) if metadata else ''
        }
        
        writer.writerow(row)

