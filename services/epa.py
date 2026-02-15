import requests
import duckdb
import os
from typing import List, Dict, Any, Optional

class EPAClient:
    """
    Client for interacting with EPA data via local Parquet file (using DuckDB) 
    or the EPA ECHO API as a fallback.
    API Documentation: https://echo.epa.gov/tools/web-services
    """
    BASE_URL = "https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities"
    PARQUET_PATH = "epa_facilities.parquet"

    def __init__(self):
        self.con = None
        if os.path.exists(self.PARQUET_PATH):
            try:
                self.con = duckdb.connect(database=':memory:') # In-memory db, reading parquet file
                # Register the parquet file as a view for easier querying if needed, 
                # or just query directly. Using direct query in methods for simplicity.
                print(f"EPAClient: Loaded local data from {self.PARQUET_PATH}")
            except Exception as e:
                print(f"EPAClient: Failed to load local data: {e}")

    def search_facilities(self, company_name: str, state: Optional[str] = None, mock_fallback: bool = True) -> List[Dict[str, Any]]:
        """
        Search for facilities.
        Priority 1: Local Parquet File (via DuckDB)
        Priority 2: EPA API
        Priority 3: Mock Data (if enabled)
        """
        # 1. Try Local Search
        if self.con:
            try:
                print(f"Searching local data for {company_name}...")
                # Construct query
                # We use ILIKE for case-insensitive partial match
                # Assuming standard columns found in national_single.csv: 
                # PRIMARY_NAME, LOCATION_ADDRESS, CITY_NAME, STATE_CODE, POSTAL_CODE
                
                query = f"""
                    SELECT 
                        REGISTRY_ID, PRIMARY_NAME, LOCATION_ADDRESS, 
                        CITY_NAME, STATE_CODE, POSTAL_CODE, LATITUDE83, LONGITUDE83
                    FROM '{self.PARQUET_PATH}'
                    WHERE PRIMARY_NAME ILIKE ?
                """
                params = [f"%{company_name}%"]
                
                if state:
                    query += " AND STATE_CODE = ?"
                    params.append(state)
                
                query += " LIMIT 20"
                
                results = self.con.execute(query, params).fetchall()
                
                if results:
                    print(f"Found {len(results)} matches in local data.")
                    normalized = []
                    for row in results:
                        # Row structure based on select order
                        normalized.append({
                            "registry_id": row[0],
                            "name": row[1],
                            "address": row[2],
                            "city": row[3],
                            "state": row[4],
                            "zip_code": row[5],
                            "latitude": row[6],
                            "longitude": row[7],
                        })
                    return normalized
                else:
                    print("No matches in local data.")

            except Exception as e:
                print(f"Error querying local data: {e}")
                # Fallthrough to API

        # 2. Try EPA API
        # Testing with FRS parameters
        params = {
            "facility_name": company_name,
            "output": "JSON"
        }
        
        if state:
            params["state_abbr"] = state

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            
            try:
                data = response.json()
            except Exception:
                print(f"Failed to parse JSON. Raw response: {response.text}")
                if mock_fallback:
                    return self._get_mock_data(company_name, state)
                return []
            
            results = data.get("Results", {})
            facilities = results.get("FRSFacilities", [])
            
            if not facilities:
                if mock_fallback:
                    return self._get_mock_data(company_name, state)
                return []
                
            # Normalize the output
            normalized_facilities = []
            for fac in facilities:
                normalized_facilities.append({
                    "registry_id": fac.get("RegistryId"),
                    "name": fac.get("FacilityName"),
                    "address": fac.get("LocationAddress"),
                    "city": fac.get("CityName"),
                    "state": fac.get("StateAbbr"),
                    "zip_code": fac.get("ZipCode"),
                    "latitude": fac.get("Latitude83"),
                    "longitude": fac.get("Longitude83"),
                })
                
            return normalized_facilities

        except Exception as e:
            print(f"Error fetching EPA data (using mock): {e}")
            if mock_fallback:
                return self._get_mock_data(company_name, state)
            return []

    def _get_mock_data(self, company_name: str, state: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns mock facility data for demonstration."""
        # Use a default state if none provided, for the mock data
        safe_state = state if state else "TX"
        
        return [{
            "registry_id": "110000491823",
            "name": f"{company_name.upper()} GIGAFACTORY",
            "address": "1 TESLA ROAD",
            "city": "AUSTIN",
            "state": safe_state,
            "zip_code": "78725",
            "latitude": 30.22,
            "longitude": -97.62,
        }]

if __name__ == "__main__":
    # Quick test
    client = EPAClient()
    results = client.search_facilities("Tesla")
    print(f"Found {len(results)} facilities for Tesla")
    if results:
        print(results[0])
