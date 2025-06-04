from pymongo import MongoClient


uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
  
try:
    

    client.admin.command("ping")
    print("Connected successfully")

    for db_name in client.list_database_names():
        print(db_name)

    

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

finally:
    client.close()
    
    
    