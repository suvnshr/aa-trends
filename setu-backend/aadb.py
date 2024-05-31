import pymongo
import os

from dotenv import load_dotenv

# Load envs
load_dotenv()


class AADB:
    
    """ 
    AADB provides methods to save, fetch and delete AA docs
    """
    
    # Db creds and identifiers
    DB_URL =  os.environ.get('DB_URL') 
    DB_NAME =  os.environ.get('DB_NAME')
    COLLECTION_NAME =  os.environ.get('COLLECTION_NAME')

    def __init__(self):
        self.client = None

    # Connect to a collection
    def connect_to_collection(self):
        # Connect to mongo
        self.client = pymongo.MongoClient(self.DB_URL)
        
        # return collection instance
        return self.client[self.DB_NAME][self.COLLECTION_NAME]
    
    # Close connection
    def close_connection(self):
        self.client.close()
    
    # Delete record for a specific date 
    def delete_record_for_date(self, date):
        collection = self.connect_to_collection()
        collection.delete_one({"date": date})
        self.close_connection()

    # Save an AA doc
    def save_aa_doc(self, aa_doc):
        try:

            # Connect to collecion
            collection = self.connect_to_collection()
            # Delete previous records(if any) for the same date
            self.delete_record_for_date(aa_doc["date"])
            # Insert the doc
            result = collection.insert_one(aa_doc)
            self.close_connection()
            return True
        except Exception as e:
            print("Error while saving doc", aa_doc, e)
            return False
        
    # Fetch AA docs
    def fetch_aa_docs(self):
        try:
            collection = self.connect_to_collection()
            
            # Fetch docs from db   
            docs = list(collection.find())
            
            for doc in docs:
                # Stringify the _id param because 
                # ...`ObjectID` cannot be jsonfied in the response
                doc['_id'] = str(doc['_id'])                
           
            self.close_connection()
            return docs
        
        except Exception as e:
            print("Error while fetching docs:", e)
            return False

