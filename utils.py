import pymongo
from datetime import datetime,date
import dotenv
import os

def get_db_client():
    
    dotenv.load_dotenv(dotenv.find_dotenv())

    host = os.environ.get("MONGODB_HOST")
    port = int(os.environ.get("MONGODB_PORT"))
    username = os.environ.get("MONGODB_USERNAME")
    password = os.environ.get("MONGODB_PASSWORD")
    
    client = pymongo.MongoClient(
        host=host, 
        port=port,
        username=username,
        password=password
    )
    db_handle = client['school_db']
    return db_handle, client

def read_db_data(*, collection_handle, query:dict={}, fields:dict):
    '''
    collection_handle: the collection handle
    query: the mongodb query string
    fields: the data to return. {} means everything in the document

    returns a list of documents matching the query
    '''
    results = collection_handle.find(query, fields)
    return list(results)

class Student:
    def __init__(self, collection, **kwargs):
        self.db_collection = collection
        self.school_id = kwargs.get("school_id", self.get_latest_id())
        self.first_name = kwargs.get("first_name", None)
        self.last_name = kwargs.get("last_name", None)
        self.birthday = kwargs.get("birthday", None)
        self.age = self.compute_age()
        self.email = kwargs.get("email", None)
        self.classes = kwargs.get("classes", [])
        self.profile_picture = kwargs.get("profile_picture", "default.png")
        self.gender = kwargs.get("gender", None)
        self.phone = kwargs.get("phone", None)
        self.address = kwargs.get("address", None)
        self.projects = kwargs.get("projects", None)

    @staticmethod
    def get(collection, student_id):
        student_data = collection.find_one({'school_id': student_id})
        if student_data is None:
            return None
        return Student(collection, **student_data)

    def update(self, update_fields:dict):
        if ("birthday" in update_fields) and isinstance(update_fields["birthday"], date):
            # change date to datetime
            update_fields["birthday"] = datetime(update_fields['birthday'].year, update_fields['birthday'].month, update_fields['birthday'].day)
            update_fields["age"] = self.compute_age(new_birthday=update_fields["birthday"])

        result = self.db_collection.update_one(
            {'school_id': self.school_id},
            {'$set': update_fields}
        )
        if result.matched_count == 0:
            print("None found for specified Student ID.")
        if result.modified_count == 0:
            print("No update done.")
        else:
            print("Update successful.")
        return result.modified_count

    def save(self):
        student_data = {
          "school_id": self.school_id,
          "first_name": self.first_name,
          "last_name": self.last_name,
          "birthday": self.birthday,
          "age": self.age,
          "email": self.email,
          "classes": self.classes,
          "profile_picture": self.profile_picture,
          "gender": self.gender,
          "phone": self.phone,
          "address": self.address,
          "projects": self.projects,
        }
        self.db_collection.insert_one(student_data)

    def delete(self):
        result = self.db_collection.delete_one({'school_id': self.school_id})
        if result.deleted_count == 0:
            print("Delete UNsuccessful.")
        else:
            print("Delete successful.")
        return result.deleted_count
    def get_latest_id(self):
        # create index for faster query
        self.db_collection.create_index([("school_id", 1)])
        # find the topmost (-1 is descending)
        school_id = self.db_collection.find().sort("_id", -1).limit(1)
        # get the topmost
        latest_school_id = school_id[0]["school_id"]
        # increment
        new_latest_school_id = latest_school_id + 1

        return new_latest_school_id

    def compute_age(self, new_birthday=None):
        if self.birthday in ["", None]:
            return None
        # because the compute_age uses the self.birthday
        # if we want to update using the update, with new fields
        # this function computes the old birthday, instead of the new birthday in the update_fields
        # thats why we added a new_birthday parameter
        if new_birthday:
            self.birthday = new_birthday
        current_date = datetime.now().date()
        age = current_date.year - self.birthday.year

        # Adjust age if the birth date hasn't occurred yet this year
        if current_date.month < self.birthday.month or (current_date.month == self.birthday.month and current_date.day < self.birthday.day):
            age -= 1

        return age
