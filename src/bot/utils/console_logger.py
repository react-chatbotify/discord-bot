"""
Logger configuration module for console output.

Initializes and configures a console logger using values from the
logging config. Sets the log level, output format, and ensures no
duplicate handlers are attached.
"""

import logging

from bot.config.logging import logging_config

# creates logger
console_logger = logging.getLogger(logging_config.logger_prefix)

# sets log level to info
log_level_num = getattr(logging, logging_config.logger_level, logging.INFO)
console_logger.setLevel(log_level_num)

# formats logger output
handler = logging.StreamHandler()
formatter = logging.Formatter(logging_config.logger_format)
handler.setFormatter(formatter)
if not console_logger.hasHandlers():
    console_logger.addHandler(handler)

console_logger.info("✅ Logger is successfully configured.")
