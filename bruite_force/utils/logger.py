"""
Logging configuration module
"""

import logging
import os
from typing import Optional


def setup_logger(name: str = "bruite_force", 
                log_level: str = "INFO",
                log_file: Optional[str] = None,
                console_output: bool = True) -> logging.Logger:
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        console_output: Whether to output to console
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add file handler if log_file is specified
    if log_file:
        try:
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "bruite_force") -> logging.Logger:
    """Get existing logger or create a new one"""
    return logging.getLogger(name)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}"
                f"{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        return super().format(record)


def setup_colored_logger(name: str = "bruite_force", 
                        log_level: str = "INFO",
                        log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup logger with colored console output
    
    Args:
        name: Logger name
        log_level: Logging level
        log_file: Path to log file (optional)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Add file handler if log_file is specified
    if log_file:
        try:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    # Add colored console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger
