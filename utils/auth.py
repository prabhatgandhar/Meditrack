import firebase_admin
from firebase_admin import credentials, auth
from pathlib import Path

# Initialize Firebase only once
if not firebase_admin._apps:
    cred_path = Path(__file__).parent.parent / "serviceAccountKey.json"
    cred = credentials.Certificate(str(cred_path))
    firebase_app = firebase_admin.initialize_app(cred)
else:
    firebase_app = firebase_admin.get_app()

def create_user(email: str, password: str, name: str) -> str:
    """Create a new Firebase user and return their UID"""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        return user.uid
    except Exception as e:
        raise Exception(f"Failed to create user: {str(e)}")

def verify_token(id_token: str) -> dict:
    """Verify Firebase ID token"""
    try:
        return auth.verify_id_token(id_token)
    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")
