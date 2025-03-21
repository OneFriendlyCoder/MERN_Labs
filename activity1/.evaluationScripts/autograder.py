import requests
from pymongo import MongoClient
import time
import bcrypt
import random
import string
import json

# Configuration
API_URL = "http://localhost:30002/signup"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "UserDB"  
COLLECTION_NAME = "users"
FILE_PATH = "/home/.evaluationScripts/data.json"
EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

# Load test data from JSON file
with open(FILE_PATH, 'r') as file:
    test_data = json.load(file)

dataSkel_list = []
for i in range(1, 7):  # Adjusted to 6 test cases for clarity if needed
    obj = {
        "testid": i,
        "status": "fail",
        "score": 0,
        "maximum marks": 1,
        "message": f"Test case {i} failed"
    }
    dataSkel_list.append(obj)

def send_signup_request(data):
    try:
        response = requests.post(API_URL, json=data)
        return response
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending request:", e)
        return None

def query_user_in_db(email):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        user = db[COLLECTION_NAME].find_one({"email": email})
        client.close()
        return user
    except Exception as e:
        print("An error occurred while querying the DB:", e)
        return None

def count_users_with_email(email):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        count = db[COLLECTION_NAME].count_documents({"email": email})
        client.close()
        return count
    except Exception as e:
        print("An error occurred while counting entries:", e)
        return None

def count_users_with_username(username):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        count = db[COLLECTION_NAME].count_documents({"username": username})
        client.close()
        return count
    except Exception as e:
        print("An error occurred while counting entries:", e)
        return None
    
def main():
    # Send signup requests for each test data entry
    r0 = send_signup_request(test_data[0])
    r1 = send_signup_request(test_data[1])
    r2 = send_signup_request(test_data[2])
    r3 = send_signup_request(test_data[3])
    r4 = send_signup_request(test_data[4])
    r5 = send_signup_request(test_data[5])    

    # Test 1: Check if the first entry (with empty password) was rejected.
    if count_users_with_email(test_data[0]["email"]) == 0:
        dataSkel_list[0] = {
            "testid": 1,
            "status": "pass",
            "score": 1,
            "maximum marks": 1,
            "message": "Test case 1 passed"
        }
    else:
        dataSkel_list[0] = {
            "testid": 1,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 1 failed"
        }        

    # Test 2: Check if the second entry (with empty email) was rejected.
    if count_users_with_username(test_data[1]["username"]) == 0:
        dataSkel_list[1] = {
            "testid": 2,
            "status": "pass",
            "score": 1,
            "maximum marks": 1,
            "message": "Test case 2 passed"
        }
    else:
        dataSkel_list[1] = {
            "testid": 2,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 2 failed"
        }

    # Test 3: Check if the third entry (with empty username) was rejected.
    if count_users_with_email(test_data[2]["email"]) == 0:
        dataSkel_list[2] = {
            "testid": 3,
            "status": "pass",
            "score": 1,
            "maximum marks": 1,
            "message": "Test case 3 passed"
        }
    else:
        dataSkel_list[2] = {
            "testid": 3,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 3 failed"
        }        
          
    # Test 4: For the fourth entry, verify that a valid user is stored and password is hashed.
    if count_users_with_email(test_data[3]["email"]) == 1: 
        user = query_user_in_db(test_data[3]["email"])
        stored_password = user.get("password", "")
        try:
            if bcrypt.checkpw(test_data[3]["password"].encode('utf-8'), stored_password.encode('utf-8')):
                dataSkel_list[3] = {
                    "testid": 4,
                    "status": "pass",
                    "score": 1,
                    "maximum marks": 1,
                    "message": "Test case 4 passed"
                }
            else:
                dataSkel_list[3] = {
                    "testid": 4,
                    "status": "fail",
                    "score": 0,
                    "maximum marks": 1,
                    "message": "Test case 4 failed"
                }
        except Exception as e:
            print("Error while checking password hash:", e)
            dataSkel_list[3] = {
                "testid": 4,
                "status": "fail",
                "score": 0,
                "maximum marks": 1,
                "message": "Test case 4 failed"
            }
    else:
        dataSkel_list[3] = {
            "testid": 4,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 4 failed"
        }

    # Test 5: Check if duplicate user creation (fifth entry) for username is handled.
    if count_users_with_username(test_data[4]["username"]) == 1: 
        dataSkel_list[4] = {
            "testid": 5,
            "status": "pass",
            "score": 1,
            "maximum marks": 1,
            "message": "Test case 5 passed"
        }
    else:
        dataSkel_list[4] = {
            "testid": 5,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 5 failed"
        }

    # Test 6: Check if duplicate user creation (sixth entry) for email is handled.
    if count_users_with_email(test_data[5]["email"]) == 1: 
        dataSkel_list[5] = {
            "testid": 6,
            "status": "pass",
            "score": 1,
            "maximum marks": 1,
            "message": "Test case 6 passed"
        }
    else:
        dataSkel_list[5] = {
            "testid": 6,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 6 failed"
        }

    # Write test results to evaluate.json file
    try:
        with open(EVALUATE_FILE, 'w') as eval_file:
            json.dump(dataSkel_list, eval_file, indent=4)
        print(f"Test results successfully written to {EVALUATE_FILE}")
    except Exception as e:
        print("An error occurred while writing to evaluate.json:", e)

if __name__ == "__main__":
    main()
