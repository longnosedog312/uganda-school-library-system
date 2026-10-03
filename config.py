"""
Configuration settings for Uganda School Library Management System
"""

# Database Configuration
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'library_system'
DB_USER = 'postgres'
DB_PASSWORD = 'password'

# Application Settings
APP_TITLE = 'Uganda School Library Management System'
SCHOOL_NAME = 'Secondary School Name'
SCHOOL_EMAIL = 'school@example.com'
SCHOOL_PHONE = '+256 XXX XXX XXX'

# Library Settings
BORROW_LIMIT = 5  # Max books per student
BORROW_DURATION = 14  # Days
FINE_PER_DAY = 500  # UGX
MAX_FINE = 10000  # UGX

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FONT_FAMILY = 'Helvetica'
FONT_SIZE = 10

# Colors
PRIMARY_COLOR = '#2c3e50'
SECONDARY_COLOR = '#3498db'
SUCCESS_COLOR = '#27ae60'
DANGER_COLOR = '#e74c3c'
WARNING_COLOR = '#f39c12'
BG_COLOR = '#ecf0f1'
TEXT_COLOR = '#2c3e50'
