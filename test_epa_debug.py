from services.epa import EPAClient
import requests

def test_search():
    client = EPAClient()
    
    # Test cases
    queries = [
        # City, State test
        {"city_name": "San Francisco", "state_abbr": "CA"},
        # Name + State test
        {"facility_name": "CHEVRON", "state_abbr": "CA"},
    ]
    
    for params in queries:
        print(f"--- Query: {params} ---")
        try:
            # We need to manually construct this since the method signature is fixed
            # Just hacking the client usage for debug
            response = requests.get(client.BASE_URL, params={**params, "output": "JSON"}, timeout=10)
            data = response.json()
            results = data.get("Results", {}).get("FRSFacilities", [])
            print(f"Found {len(results)} results")
            if results:
                print(f"Sample: {results[0]['FacilityName']} - {results[0]['LocationAddress']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
