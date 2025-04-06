import requests
import re
import json

# === CONFIGURATION ===
BASE_URL = "http://localhost:30002"  # Adjust if your server runs on a different port
LOGIN_ENDPOINT = "/login"
DASHBOARD_ENDPOINT = "/protected/dashboard"
EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"  # Adjust path if needed

VALID_EMAIL = "ram@gmail.com"    # Replace with valid test credentials
VALID_PASSWORD = "ram@123"       # Replace with valid test credentials

# Data skeleton for evaluation results (2 test cases)
dataSkel_list = [
    {
        "testid": 1,
        "status": "fail",
        "score": 0,
        "maximum marks": 1,
        "message": "Test case 1 failed"
    },
    {
        "testid": 2,
        "status": "fail",
        "score": 0,
        "maximum marks": 1,
        "message": "Test case 2 failed"
    }
]

def login_and_get_credentials():
    """Send a POST request to /login and return the token and user info."""
    url = BASE_URL + LOGIN_ENDPOINT
    payload = {
        "email": VALID_EMAIL,
        "password": VALID_PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return None, None

        data = response.json()
        token = data.get("token")
        user = data.get("user")
        # Check for non-empty token, user, username, and email
        if not token or not user or not user.get("username") or not user.get("email"):
            return None, None

        return token, user
    except Exception as e:
        return None, None

def access_dashboard(token):
    """Send a GET request to the dashboard endpoint using the provided token."""
    url = BASE_URL + DASHBOARD_ENDPOINT
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        return response.text
    except Exception as e:
        return None

def extract_username_from_html(html):
    """
    Extracts the username from the dashboard HTML.
    This function uses a regular expression to find a pattern like:
      <h1>Welcome <username>!</h1>
    """
    match = re.search(r"Welcome\s+([^<]+)!", html)
    if match:
        return match.group(1).strip()
    return None

def main():
    # ---------- Test Case 1: Login Test ----------
    token, user = login_and_get_credentials()
    if token and user:
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
            "message": "Server not running or login failed"
        }
        # If login fails, there's no point checking the dashboard.
        with open(EVALUATE_FILE, 'w') as eval_file:
            json.dump({"data": dataSkel_list}, eval_file, indent=4)
        return

    # ---------- Test Case 2: Dashboard Test ----------
    login_username = user.get("username")
    dashboard_html = access_dashboard(token)
    if dashboard_html:
        dashboard_username = extract_username_from_html(dashboard_html)
        if dashboard_username == login_username:
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
                "message": "Dashboard username does not match login username"
            }
    else:
        dataSkel_list[1] = {
            "testid": 2,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Server not running or dashboard not accessible"
        }

    try:
        with open(EVALUATE_FILE, 'w') as eval_file:
            json.dump({"data": dataSkel_list}, eval_file, indent=4)
        print("Evaluation results written to evaluate.json")
    except Exception as e:
        print("An error occurred while writing to evaluate.json:", e)

if __name__ == "__main__":
    main()
