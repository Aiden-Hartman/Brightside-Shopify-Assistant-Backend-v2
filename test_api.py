import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_health():
    url = f"{BASE_URL}/health"
    print(f"\nTesting GET {url}")
    try:
        resp = requests.get(url)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.json()}")
        assert resp.status_code == 200 and resp.json().get("status") == "ok"
        print("[PASS] /health endpoint works!")
        return True
    except Exception as e:
        print(f"[FAIL] /health endpoint: {e}")
        return False

def test_recommendation():
    url = f"{BASE_URL}/recommend"
    headers = {"Content-Type": "application/json"}
    data = {
        "query": "protein supplement",
        "limit": 3
    }
    print(f"\nTesting POST {url}")
    try:
        resp = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {json.dumps(resp.json(), indent=2)}")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        print("[PASS] /recommend endpoint works!")
        return True
    except Exception as e:
        print(f"[FAIL] /recommend endpoint: {e}")
        return False

def test_chat():
    url = f"{BASE_URL}/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "message": "What helps with sleep?",
        "client_id": "test_client",
        "session_id": "test_session",
        "chat_history": [
            {
                "role": "user",
                "content": "Hello",
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }
    print(f"\nTesting POST {url}")
    try:
        resp = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {json.dumps(resp.json(), indent=2)}")
        assert resp.status_code == 200
        assert resp.json().get("role") == "assistant"
        print("[PASS] /api/chat endpoint works!")
        return True
    except Exception as e:
        print(f"[FAIL] /api/chat endpoint: {e}")
        return False

def main():
    print("\n--- API Endpoint Smoke Test ---")
    results = {
        "health": test_health(),
        "recommend": test_recommendation(),
        "chat": test_chat(),
    }
    print("\n--- Test Summary ---")
    for k, v in results.items():
        print(f"{k}: {'✓' if v else '✗'}")
    if not all(results.values()):
        print("\nSome endpoints failed. Please check the logs above.")
    else:
        print("\nAll endpoints passed!")

if __name__ == "__main__":
    main()
