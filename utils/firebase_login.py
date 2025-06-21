import requests

def firebase_login(email, password, api_key):
    print(f"🚨 Trying to log in: {email}")  # For debug tracking

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Firebase login success")
        return response.json()  # Includes localId (UID), email, etc.
    else:
        print(f"❌ Firebase login failed: {response.text}")
        raise Exception(response.json().get("error", {}).get("message", "Login failed."))

