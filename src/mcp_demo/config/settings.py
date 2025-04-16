from typing import List

# Server Configuration
SERVER_NAME = "Demo"
SERVER_VERSION = "1.0.0"

# Security Settings
BLOCKED_HOSTS: List[str] = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '10.',
    '172.16.',
    '192.168.'
]

# API Settings
YAHOO_FINANCE_BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"
DEFAULT_HTTP_TIMEOUT = 30 