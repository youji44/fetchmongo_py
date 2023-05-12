import pymongo
from pymongo import MongoClient

# List of MongoDB server connection details
servers = [
    {
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': ''
    }
    # Add more servers as needed
]

# Open CSV file for output
fh = open('output.csv', 'w', encoding='utf-8')
fh.write('DBName,Size,PackageCount\n')

for server in servers:
    # Connect to MongoDB server
    mongo_client = MongoClient(
        host=server['host'],
        port=server['port'],
        username=server['username'],
        password=server['password']
    )

    # Get server information
    for k, v in mongo_client.server_info().items():
        print("Key: {} , Value: {}".format(k, v))

    # Get database names
    database_names = mongo_client.list_database_names()

    # print('DBName,Size,PackageCount')

    # Calculate and print total database size for each database
    for db_name in database_names:
        pack_count = mongo_client[db_name]['system.js'].count_documents({})
        db = mongo_client[db_name]
        stats = db.command('dbStats')
        total_size = stats['dataSize'] + stats['indexSize']
        print(f"{server['host']} | {db_name}, {total_size} bytes, {pack_count}")
        fh.write(db_name+','+str(total_size)+','+str(pack_count)+'\n')

    # Disconnect from MongoDB server
    mongo_client.close()

fh.close()


