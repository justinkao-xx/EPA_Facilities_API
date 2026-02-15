#!/bin/bash
# 1. Test without token (Should Fail)
echo "Testing without token (Expect 401/403):"
curl -s -o /dev/null -w "%{http_code}\n" -X POST "http://localhost:8000/enrich" \
     -H "Content-Type: application/json" \
     -d '{"company_name": "Tesla", "website": "tesla.com"}'

# 2. Test with token (Should Succeed)
echo "Testing with token (Expect 200):"
curl -s -X POST "http://localhost:8000/enrich" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: my-secret-password" \
     -d '{"company_name": "TESLA", "website": "tesla.com"}' | python3 -m json.tool
