import json
from http.server import BaseHTTPRequestHandler

from hashing import generate_hash



class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = {
            "project": "BlockVerify",
            "status": "running",
            "message": "Blockchain-Based Tamper-Proof Record Verification API",
            "algorithm": "SHA-256"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            record_id = data.get("record_id")
            record_data = data.get("record_data")

            if not record_id or not record_data:
                self.send_error(400, "record_id and record_data are required")
                return

            record_hash = generate_hash(record_data)

            response = {
                "project": "BlockVerify",
                "record_id": record_id,
                "record_hash": record_hash,
                "algorithm": "SHA-256",
                "status": "Hash generated successfully"
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

        except Exception as error:
            self.send_error(500, str(error))