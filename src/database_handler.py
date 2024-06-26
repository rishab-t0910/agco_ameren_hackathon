from google.cloud import firestore
from dotenv import load_dotenv
import os

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
        self.collection_name = 'streaming_data'

    def verify_schema(data):
        return False

    def add_data(self, data):
        self.db.collection(self.collection_name).add(data)

    def get_data(self, node_id, data):
        return None



