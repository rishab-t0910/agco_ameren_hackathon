from google.cloud import firestore
from dotenv import load_dotenv
import os
import datetime

class DatabaseHandler:

    def __init__(self):
        # Load environment
        load_dotenv()
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        # Check if the credentials environment variable is set
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        else:
            raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

        # Initialize firestore
        self.db = firestore.Client()

    def add_data(self, node_id, timestamp, noise, count):
        data = {
            'timestamp' : timestamp,
            'node_id' : node_id,
            'noise' : noise,
            'count' : count,
        }

        doc_id = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        self.db.collection(node_id).document(doc_id).set(data)

    def get_data(self, node_id, start, end):
        collection_ref = self.db.collection(node_id)
        query = collection_ref

        if start and end:
            query = query.where('timestamp', '>=', start).where('timestamp', '<=', end)
        elif start:
            query = query.where('timestamp', '>=', start)
        elif end:
            query = query.where('timestamp', '<=', end)

        docs = query.stream()

        # Collect the documents in a list
        data = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id  # Add the document ID to the data
            data.append(doc_dict)

        return data


