"""Kismet server info abstraction."""
from .base_interface import BaseInterface
from .snapshots import Snapshots
import json
import sqlite3
from .utility import Utility


class Kismet(Snapshots):
    """This object extracts kismet server info from the first SYSTEM 
    snapshot in the database.  All values reference the Kismet
    server which generated this log.

    Args:
        file_location (str): Path to Kismet log file.

    Attributes:
        kismet_version (str): Kismet version
        kismet_git (str): Kismet git commit string
        kismet_uuid (str): UUID of server
        kismet_name (str): User-supplied name of server
        kismet_location (str): User-supplied server location
        kismet_description (str): User-supplied server description
        kismet_user (str): Username server was running under
    """
    
    def __init__(self, filepath):
        super(Kismet, self).__init__(filepath)

        sql = "SELECT json FROM snapshots WHERE snaptype = 'SYSTEM' LIMIT 1"
        db = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_COLNAMES)
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        result = row["json"]
        db.close()

        system_j = json.loads(result)

        self.kismet_version = system_j['kismet.system.version']
        self.kismet_git = system_j['kismet.system.git']
        self.kismet_uuid = system_j['kismet.system.server_uuid']
        self.kismet_name = system_j['kismet.system.server_name']
        self.kismet_location = system_j['kismet.system.server_location']
        self.kismet_description = system_j['kismet.system.server_description']
        self.kismet_user = system_j['kismet.system.user']

