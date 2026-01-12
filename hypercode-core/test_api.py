import requests
import json

url = "http://127.0.0.1:8000/compile"
payload = {
  "nodes": [
    { "id": "init-q", "type": "init", "data": { "label": "q = QReg(2)" } },
    { "id": "init-c", "type": "init", "data": { "label": "c = CReg(2)" } },
    { "id": "h-node", "type": "gate", "data": { "label": "H", "gateType": "H", "target": "q[0]" } },
    { "id": "measure-0", "type": "measure", "data": { "label": "Measure q[0]", "qubit": "q[0]", "target": "c[0]" } }
  ],
  "edges": []
}

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
