from database import connect_db, get_collection

db = connect_db()
print db
coll = get_collection(db, "user")
print coll