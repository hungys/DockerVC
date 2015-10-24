from azure.storage.queue import QueueService
from bson.objectid import ObjectId
from core.database import connect_db
import config
import json

def process_message(message):
    try:
        global db
        payload = json.loads(message)
        input_id = payload["input_id"]
        workunit_id = payload["workunit_id"]
        output_url = payload["output_url"]
        output_checksum = payload["output_checksum"]

        print "Workunit %s finished" % workunit_id

        finished_count = db.workunit.find({"input_id": input_id, "status": "finished", "output_checksum": output_checksum}).count()
        if finished_count > CONSENSUS_MIN:
            print "Input %s reached consensus" % input_id
            db.workunit.update({"input_id": input_id, "status": "finished", "output_checksum": output_checksum}, \
                {"$set": {"status": "accepted"}})
            db.workunit.update({"input_id": input_id, "status": "finished", "output_checksum": {"$ne": output_checksum}}, \
                {"$set": {"status": "rejected"}})
            db.input.update({"_id": ObjectId(input_id)}, {"$set": {"status": "finished", "output_url": output_url}})
    except:
        pass

if __name__ == "__main__":
    dbconn, db = connect_db()

    queue_service = QueueService(account_name=config.AZURE_STORAGE_NAME, account_key=config.AZURE_STORAGE_KEY)
    queue_service.create_queue(config.AZURE_QUEUE_NAME)

    while True:
        try:
            messages = queue_service.get_messages(config.AZURE_QUEUE_NAME)
            for message in messages:
                process_message(message.message_text)
                queue_service.delete_message(config.AZURE_QUEUE_NAME, message.message_id, message.pop_receipt)
        except KeyboardInterrupt:
            break