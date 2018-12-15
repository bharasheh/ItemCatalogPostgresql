import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/ItemCatalog/")

from application import app as application
