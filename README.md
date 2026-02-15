# Deep Research API

An internal API for enriching company data with facilities (source is the EPA), assets (source is UCC), and headquarters information.

## Features

- **EPA Facility Search**:
  - Extremely fast local lookup using **DuckDB** and Parquet (5M+ records).
  - Automatic fallback to EPA ECHO API if local data is missing.
- **Asset Intelligence**: Mock integration with UCC filing data (extensible to real providers like Middesk).
- **HQ Lookup**: Automated headquarters address discovery.
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
   The EPA dataset is too large for Git. You need the `national_single.csv` file from the EPA website.
   ```bash
   # Convert CSV to Parquet for performance
   python3 convert_data.py
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

## Deployment via Docker

Build and run the container with your secure token:

```bash
docker build -t deep-research-api .
docker run -p 8000:8000 -e INTERNAL_API_TOKEN="Innoveer!23" deep-research-api
```
