import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from contextvars import ContextVar

import urllib3

from loguru import logger

# Counter to track account number
_account_counter = 0

# Context variable to store account number per task
account_number_ctx: ContextVar[int] = ContextVar('account_number', default=0)


def get_account_number() -> int:
    """Increment and return the account number"""
    global _account_counter
    _account_counter += 1
    account_number_ctx.set(_account_counter)
    return _account_counter


def patch(record):
    """Add account number to record"""
    record["extra"]["account_num"] = account_number_ctx.get() or ""
    return True


def format_account_message(record):
    """Custom format function to inject account number"""
    account_num = account_number_ctx.get()
    if account_num > 0:
        record["extra"]["account_num"] = account_num
    else:
        record["extra"]["account_num"] = ""
    return "[{time:HH:mm:ss | DD-MM-YYYY}] [Crazyscholar @ IRYS] [{level}] | Account  {extra[account_num]} - {message}\n{exception}"


def configuration():
    urllib3.disable_warnings()
    logger.remove()

    # Tắt log của primp và web3
    logging.getLogger("primp").setLevel(logging.WARNING)
    logging.getLogger("web3").setLevel(logging.WARNING)

    console_format = (
        "<cyan>[{time:HH:mm:ss | DD-MM-YYYY}]</cyan> "
        "<magenta>[Crazyscholar @ IRYS ]</magenta> "
        "<level>[{level}]</level> | "
        "<blue>Account  {extra[account_num]}</blue> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        colorize=True,
        format=console_format,
        level="INFO",
        filter=patch
    )
    
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 month",
        format=format_account_message,
        level="INFO",
        filter=patch
    )


def setup_multiprocess_logging(is_main: bool = False):
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    if is_main:
        log_file = f"logs/main_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    else:
        log_file = f"logs/process_{os.getpid()}.log"

    logger.add(
        log_file,
        rotation="10 MB",
        retention="1 month",
        format=format_account_message,
        level="INFO",
        filter=patch
    )


def setup_logs(is_main: bool = False):
    urllib3.disable_warnings()
    
    # Tắt log của primp và web3
    logging.getLogger("primp").setLevel(logging.WARNING)
    logging.getLogger("web3").setLevel(logging.WARNING)
    
    logger.remove()
    
    console_format = (
        "<cyan>[{time:HH:mm:ss | DD-MM-YYYY}]</cyan> "
        "<magenta>[Crazyscholar @ IRYS ]</magenta> "
        "<level>[{level}]</level> | "
        "<blue>Account  {extra[account_num]}</blue> - "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        colorize=True,
        format=console_format,
        level="INFO",
        filter=patch
    )
    
    setup_multiprocess_logging(is_main)
