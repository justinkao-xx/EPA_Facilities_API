# Deep Research API

A powerful internal API for enriching company data with environmental compliance (EPA) information.

## Features

- **EPA Facility Search**:
  - Extremely fast local lookup using **DuckDB** and Parquet (5M+ records).
  - Automated data download and setup.
- **Secure**: API Key authentication for internal use.
- **Production Ready**: Dockerized and ready for deployment.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/justinkao-xx/Deep-Research-API.git
   cd Deep-Research-API
   ```

2. **Set up Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Prepare Data**:
   Download and process the EPA dataset (runs once):
   ```bash
   python download_data.py
   ```

## Usage

### Running Locally

```bash
# Set your internal token
export INTERNAL_API_TOKEN="my-secret-password"

# Start the server
uvicorn main:app --reload
```

### API Endpoint

**POST** `/enrich`

**Headers**:
- `X-API-Key`: `<INTERNAL_API_TOKEN>`

**Body**:
```json
{
  "company_name": "Tesla",
  "website": "tesla.com"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/enrich" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: my-secret-password" \
     -d '{"company_name": "Tesla", "website": "tesla.com"}'
```

**Response**:
```json
{
  "epa_facilities": [
    {
      "registry_id": 110058852331,
      "name": "TESLA MOTORS INC",
      "address": "1501 PAGE MILL RD",
      "city": "PALO ALTO",
      "state": "CA",
      "zip_code": "94304",
      "latitude": 37.42308,
      "longitude": -122.146608
    }
  ]
}
```

## Deployment via Docker

Build and run the container (data downloads automatically during build):

```bash
docker build -t deep-research-api .
docker run -p 8000:8000 -e INTERNAL_API_TOKEN="Innoveer!23" deep-research-api
```
