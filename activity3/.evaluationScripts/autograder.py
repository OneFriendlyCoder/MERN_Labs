import requests
from pymongo import MongoClient
import time
import bcrypt
import json

# Configuration
SIGNUP_URL = "http://localhost:30002/signup"
LOGIN_URL = "http://localhost:30002/login"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "UserDB"
COLLECTION_NAME = "users"
FILE_PATH = "/home/godfather/MERN_Labs/activity3/.evaluationScripts/data.json"
EVALUATE_FILE = "/home/godfather/MERN_Labs/activity3/.evaluationScripts/evaluate.json"

# Load test data from JSON file
with open(FILE_PATH, 'r') as file:
    test_data = json.load(file)

# Adjusted to 6 test cases: 5 for signup tests and 1 for login JWT structure
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
        response = requests.post(SIGNUP_URL, json=data)
        return response
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending signup request:", e)
        return None

def send_login_request(data):
    try:
        response = requests.post(LOGIN_URL, json=data)
        return response
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending login request:", e)
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
    # --------------------
    # Signup Tests
    # --------------------
    # Test case 1: Missing email (non-empty field check)
    r0 = send_signup_request(test_data[0])
    # Test case 2: Invalid email format
    r1 = send_signup_request(test_data[1])
    # Test case 3: Valid registration for a new user (for subsequent login tests)
    r2 = send_signup_request(test_data[2])
    # Test case 4: Duplicate registration with correct password (simulate login success)
    r3 = send_signup_request(test_data[3])
    # Test case 5: Duplicate registration with wrong password (simulate login failure)
    r4 = send_signup_request(test_data[4])
    
    time.sleep(1)  # Give the database a moment to update

    # --------------------
    # Test 1: Check that a signup attempt with a missing email is rejected.
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

    # --------------------
    # Test 6: Check for a proper JWT response from the /login endpoint.
    # Use the valid registration's credentials (from test_data[2]).
    login_data = {
        "email": test_data[2]["email"],
        "password": test_data[2]["password"]
    }
    login_response = send_login_request(login_data)
    if login_response is None:
        dataSkel_list[5] = {
            "testid": 6,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test case 6 failed"
        }
    else:
        try:
            login_result = login_response.json()
            # print(login_result)
            # Check that login_result has token, message and user (with correct username and email)
            if (login_result.get("token") and login_result.get("message") and login_result.get("user") and
                login_result["user"].get("username") == test_data[2]["username"] and
                login_result["user"].get("email") == test_data[2]["email"]):
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
        except Exception as e:
            print("Error while processing login response:", e)
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
