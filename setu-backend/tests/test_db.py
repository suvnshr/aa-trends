from aadb import AADB
import pymongo

# Date for sample AA doc
SAMPLE_DOC_DATE = "01-01-2017"

# Sample aaa doc for testing
SAMPLE_AA_DOC = {
    "date": SAMPLE_DOC_DATE,
    "aas_data": {
        "Anumati": {"na_count": 59, "live_count": 53, "testing_count": 0},
        "CAMS": {"na_count": 59, "live_count": 53, "testing_count": 0},
        "CRIF": {"na_count": 81, "live_count": 29, "testing_count": 2},
        "Digio": {"na_count": 106, "live_count": 3, "testing_count": 3},
        "Finvu": {"na_count": 58, "live_count": 52, "testing_count": 2},
        "INK": {"na_count": 80, "live_count": 28, "testing_count": 4},
        "NADL": {"na_count": 61, "live_count": 46, "testing_count": 5},
        "Onemoney": {"na_count": 37, "live_count": 73, "testing_count": 2},
        "PhonePe": {"na_count": 91, "live_count": 10, "testing_count": 11},
        "Protean SurakshAA": {"na_count": 74, "live_count": 35, "testing_count": 3},
        "Setu AA": {"na_count": 100, "live_count": 10, "testing_count": 2},
        "Saafe": {"na_count": 71, "live_count": 39, "testing_count": 2},
        "TallyEdge": {"na_count": 91, "live_count": 18, "testing_count": 3},
        "Yodlee": {"na_count": 102, "live_count": 7, "testing_count": 3},
    },
}

# Connect to setu db
def connect_db():

    client = pymongo.MongoClient(AADB.DB_URL)
    return client[AADB.DB_NAME][AADB.COLLECTION_NAME]

# Test db connect operation
def test_db_connect():

    db = AADB()
    
    # get the collection instance
    collection = db.connect_to_collection()
    
    test_result = False
    
    try:
        collection.find()
        
        # If the above fetch works
        # ...then  `test_result` will be true
        test_result = True
    except:
        pass
    
    # Close connection
    db.close_connection()
    
    # Whether the fetch worked after connecting to DB? 
    assert test_result == True
    

# Test db save operation
def test_db_save():

    db = AADB()

    # save a sample AA doc to db
    result =  db.save_aa_doc(SAMPLE_AA_DOC)

    # delete the sample AA doc
    db.delete_record_for_date(SAMPLE_DOC_DATE)

    # Close connection
    db.close_connection()
    
    # Whether the db save operation was successfull?
    assert result == True


# Test db's fetch operation docs length
def test_db_fetch_length():

    # Make a separate connection
    raw_connection = connect_db()

    db = AADB()

    # Save 2 sample docs
    db.save_aa_doc(SAMPLE_AA_DOC)
    db.save_aa_doc(SAMPLE_AA_DOC)

    # fetch docs from the class method
    result_docs = db.fetch_aa_docs()
    
    # fetch docs from the separate connection
    test_docs = raw_connection.find()

    # Whether the separate connection returned the same results
    # ...as the class method.
    test_result = len(list(test_docs)) == len(list(result_docs))

    # Cleaning up, deleting the saved records
    db.delete_record_for_date(SAMPLE_DOC_DATE)

    # Close connection
    db.close_connection()

    assert test_result == True


# Test DB's delete operation
def test_delete():

    db = AADB()

    # Clean up the db
    db.delete_record_for_date(SAMPLE_DOC_DATE)

    # Fetch docs before adding and deleting a sample doc
    prev_del_docs = db.fetch_aa_docs()

    # Save a sample doc
    db.save_aa_doc(SAMPLE_AA_DOC)
    
    # Delete the previous saved record
    db.delete_record_for_date(SAMPLE_DOC_DATE)

    # Fetch docs after deleting sample docs
    after_del_docs = db.fetch_aa_docs()

    # Whether the length of fetched docs is
    # ...same before and after adding and deleting a sample doc?
    test_result =  len(list(prev_del_docs)) == len(list(after_del_docs))

    # Close connection
    db.close_connection()
    
    assert test_result == True

# Test DB's connection close operation
def test_close_connection():
    
    db = AADB()
    # Call fetch to populate the client property with pymongo instance
    db.fetch_aa_docs()
    
    client = db.client
    
    # Close the client
    client.close()
        
    test_result = False
    
    try: 
        # If we try to run `.server_info()` on client 
        # ...instance once the connection is closed, then it should throw an Exception
        client.server_info()
    except Exception as e:
        # the connection is closed successfully
        test_result = True
        pass    

    # Whether the connection has closed sucessfully?
    assert test_result == True