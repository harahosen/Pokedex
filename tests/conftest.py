import sys
import os

# Path to the "app" folder — treat it as Python root during tests
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))

if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)
