import requests
from pymongo import MongoClient
import time
import bcrypt
import json

# Configuration
API_URL = "http://localhost:30002/signup"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "UserDB"
COLLECTION_NAME = "users"
FILE_PATH = "/home/godfather/MERN_Labs/activity1/.evaluationScripts/data.json"
EVALUATE_FILE = "/home/godfather/MERN_Labs/activity1/.evaluationScripts/evaluate.json"

# Load test data from JSON file
with open(FILE_PATH, 'r') as file:
    test_data = json.load(file)

# Initial test results data structure for 6 test cases
dataSkel_list = []
for i in range(1, 7):
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
    responses = []
    for entry in test_data:
        responses.append(send_signup_request(entry))
    
    # Wait for a short period to ensure all signup operations complete
    time.sleep(2)
    
    # Test 1: Verify that an entry with an empty password (test_data[0]) is rejected.
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

    # Test 2: Verify that an entry with an empty email (test_data[1]) is rejected.
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

    # Test 3: Verify that an entry with an empty username (test_data[2]) is rejected.
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
    
    # Test 4: Verify that a valid user (test_data[3]) is stored and the password is hashed.
    if count_users_with_email(test_data[3]["email"]) == 1:
        user = query_user_in_db(test_data[3]["email"])
        stored_password = user.get("password", "")
        try:
            # Check if the stored password is a valid bcrypt hash of the original password
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

    # Test 5: Verify that duplicate user creation for username (test_data[4]) is handled (only one record exists).
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

    # Test 6: Verify that duplicate user creation for email (test_data[5]) is handled (only one record exists).
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
            json.dump({"data": dataSkel_list}, eval_file, indent=4)
    except Exception as e:
        print("An error occurred while writing to evaluate.json:", e)

if __name__ == "__main__":
    main()
