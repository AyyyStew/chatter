import json
from pydantic import BaseModel, fields
from tinydb import TinyDB, Query, table
from security.auth import User
from datetime import datetime

class Message(BaseModel):
	chatroomID: str
	message: str
	timestamp: datetime
	user: User

	def getJSONSafeMapping(self):
		# this is here to eliminate datetime serialization issues
		# pydantic probably has a solution but i couldn't find it
		return json.loads(self.json())


def get_db_table_instance(table):
    db = TinyDB(f"./databases/chatter.json")
    table = db.table(table)
    return table


def store_message(user: User, message: str, chatroomID: str):
	chatroomTable = get_db_table_instance(f"{chatroomID}")
	record : Message = Message(chatroomID=chatroomID, message=message, timestamp=datetime.now(), user=user)

	chatroomTable.insert(record.getJSONSafeMapping())