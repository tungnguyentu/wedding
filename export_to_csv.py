import csv
from pymongo import MongoClient

def export_to_csv():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wedding']
    collection = db['rsvp']

    cursor = collection.find({})
    with open('rsvp_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id','name', 'rsvp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for document in cursor:
            writer.writerow({'user_id': document['user_id'],'name': document['name'], 'rsvp': document['rsvp']})

if __name__ == '__main__':
    export_to_csv()
