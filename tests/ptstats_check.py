import requests
import json


def fetch_pypistats_recent(package: str):
    url = f"https://pypistats.org/api/packages/{package}/recent"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        print("Raw text response:")
        print(response.text)


fetch_pypistats_recent("opencc-purepy")
