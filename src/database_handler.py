from google.cloud import firestore
from dotenv import load_dotenv
import os
import datetime

class DatabaseHandler:
    def __init__(self):
        # Load environment
        load_dotenv("../.env")
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        # Check if the credentials environment variable is set
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        else:
            raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

        # Initialize firestore
        database_id = "occupi-streaming"
        self.db = firestore.Client(database=database_id)

    def add_data(self, node_id, timestamp, noise, count):
        data = {
            'timestamp' : datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S'),
            'node_id' : node_id,
            'noise' : noise,
            'count' : count,
        }

        doc_id = timestamp
        self.db.collection(str(node_id)).document(doc_id).set(data)

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
            data.append(doc_dict)

        return data
    
    def get_most_recent_count(self, node_id):
        collection_ref = self.db.collection(node_id)

        query = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        docs = query.stream()

        for doc in docs:
            doc_dict = doc.to_dict()
            return doc_dict.get('count')  # Return the count value from the most recent document

        return None 
    
    def get_forecast(self, node_id, time, window=6):
        collection_past = self.db.collection(node_id)
        collection_forecast = self.db.collection(node_id + "_forecast")

        data = []

        # Get past 
        start_time = time - datetime.timedelta(hours=window)
        query = collection_past.where('timestamp', '>=', start_time)
        for doc in query.stream():
            data.append(doc.to_dict())

        # Get future
        end_time = time + datetime.timedelta(hours=window)
        query = collection_forecast.where('timestamp', '>=', start_time).where('timestamp', '<=', end_time)
        for doc in query.stream():
            data.append(doc.to_dict())

        return data
    
    def set_forecast(self, node_id, forecasts):
        collection_ref = self.db.collection(node_id + "_forecast")

        docs = collection_ref.stream()
        for doc in docs:
            doc.reference.delete()

        # Add new forecast documents
        for forecast in forecasts:
            doc_id = str(forecast.get('timestamp'))
            self.db.collection(str(node_id)).document(doc_id).set(forecast)

