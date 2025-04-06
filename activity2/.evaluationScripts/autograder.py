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
FILE_PATH = "/home/.evaluationScripts/data.json"
EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

# Load test data from JSON file
with open(FILE_PATH, 'r') as file:
    test_data = json.load(file)

# Adjusted to 5 test cases (removing the last one)
dataSkel_list = []
for i in range(1, 6):
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
    r0 = send_signup_request(test_data[0])  # Test case 1: Missing email (empty email field)
    r1 = send_signup_request(test_data[1])  # Test case 2: Invalid email format
    r2 = send_signup_request(test_data[2])  # Test case 3: Valid registration for a new user
    r3 = send_signup_request(test_data[3])  # Test case 4: Duplicate registration with same credentials (correct password)
    r4 = send_signup_request(test_data[4])  # Test case 5: Duplicate registration with wrong password

    responses = [r0, r1, r2, r3, r4]
    
    # Check if the server is not running (i.e. all responses are None)
    if all(response is None for response in responses):
        print("Server is not running or not reachable. Failing all test cases.")
        for i in range(len(dataSkel_list)):
            dataSkel_list[i] = {
                "testid": i + 1,
                "status": "fail",
                "score": 0,
                "maximum marks": 1,
                "message": "Server not running or not reachable."
            }
        try:
            with open(EVALUATE_FILE, 'w') as eval_file:
                json.dump({"data": dataSkel_list}, eval_file, indent=4)
        except Exception as e:
            print("An error occurred while writing to evaluate.json:", e)
        return

    time.sleep(1)  # Give the database a moment to update

    # --------------------
    # Test 1: Check that a signup attempt with a missing email is rejected.
    # (Expect no DB entry for test_data[0])
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
        
    # --------------------
    # Test 2: Check that a signup attempt with an invalid email format is rejected.
    if count_users_with_email(test_data[1]["email"]) == 0:
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
        
    # --------------------
    # Test 3: Check that a valid new user is stored with a hashed password.
    if count_users_with_email(test_data[2]["email"]) == 1:
        user = query_user_in_db(test_data[2]["email"])
        stored_password = user.get("password", "")
        try:
            if bcrypt.checkpw(test_data[2]["password"].encode('utf-8'), stored_password.encode('utf-8')):
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
        except Exception as e:
            print("Error while checking password hash:", e)
            dataSkel_list[2] = {
                "testid": 3,
                "status": "fail",
                "score": 0,
                "maximum marks": 1,
                "message": "Test case 3 failed"
            }
    else:
        dataSkel_list[2] = {
            "testid": 3,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 3 failed"
        }
    
    # --------------------
    # Test 4: For a duplicate registration with the same credentials (correct password),
    # simulate a login by checking that the database still contains one entry and that the password matches.
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
            print("Error while checking duplicate password hash:", e)
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
    
    # --------------------
    # Test 5: For a duplicate registration with a wrong password,
    # the stored hash should not match the provided password (simulate a failed login attempt).
    if count_users_with_email(test_data[4]["email"]) == 1:
        user = query_user_in_db(test_data[4]["email"])
        stored_password = user.get("password", "")
        try:
            if not bcrypt.checkpw(test_data[4]["password"].encode('utf-8'), stored_password.encode('utf-8')):
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
        except Exception as e:
            print("Error while checking wrong password hash:", e)
            dataSkel_list[4] = {
                "testid": 5,
                "status": "fail",
                "score": 0,
                "maximum marks": 1,
                "message": "Test case 5 failed"
            }
    else:
        dataSkel_list[4] = {
            "testid": 5,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 5 failed"
        }

    # Write test results to evaluate.json file
    try:
        with open(EVALUATE_FILE, 'w') as eval_file:
            json.dump({"data": dataSkel_list}, eval_file, indent=4)
        print("Evaluation results written to evaluate.json")
    except Exception as e:
        print("An error occurred while writing to evaluate.json:", e)

if __name__ == "__main__":
    main()
