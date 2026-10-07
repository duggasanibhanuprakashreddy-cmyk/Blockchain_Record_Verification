import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

# Ensure repository root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from hashing import generate_hash
from blockchain import Blockchain, Block
from storage import load_blockchain, save_blockchain


class handler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def _serve_file(self, filename, content_type):
        candidates = [
            os.path.join(BASE_DIR, filename),
            os.path.join(BASE_DIR, "public", filename),
            os.path.join(os.path.dirname(__file__), filename),
            filename
        ]
        file_path = None
        for cand in candidates:
            if os.path.exists(cand) and os.path.isfile(cand):
                file_path = cand
                break

        if file_path:
            with open(file_path, "rb") as f:
                content = f.read()
            self._set_headers(200, content_type)
            self.wfile.write(content)
            return True
        return False

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path.strip()

        # 1. Root and frontend static routes (serve HTML/CSS/JS even if Vercel routes root to Python)
        if path in ("", "/", "/index.html"):
            if self._serve_file("index.html", "text/html; charset=utf-8"):
                return

        if path == "/style.css":
            if self._serve_file("style.css", "text/css; charset=utf-8"):
                return

        if path == "/script.js":
            if self._serve_file("script.js", "application/javascript; charset=utf-8"):
                return

        # 2. Blockchain API endpoints
        raw_data = load_blockchain()
        if raw_data:
            bc = Blockchain.from_data(raw_data)
        else:
            bc = Blockchain()

        clean_path = path.rstrip("/")

        if clean_path in ("/api/blockchain", "/api/records"):
            blocks = []
            for block in bc.chain:
                blocks.append({
                    "index": block.index,
                    "timestamp": block.timestamp,
                    "record_id": block.record_id,
                    "record_hash": block.record_hash,
                    "previous_hash": block.previous_hash,
                    "current_hash": block.current_hash
                })
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "status": "success",
                "total_blocks": len(blocks),
                "total_records": max(0, len(blocks) - 1),
                "chain": blocks
            }).encode("utf-8"))
            return

        elif clean_path == "/api/integrity":
            is_valid = bc.is_chain_valid()
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "status": "success",
                "is_valid": is_valid,
                "total_blocks": len(bc.chain),
                "system_status": "SECURE" if is_valid else "COMPROMISED"
            }).encode("utf-8"))
            return

        elif clean_path.startswith("/api"):
            response = {
                "project": "BlockVerify",
                "status": "running",
                "message": "Blockchain-Based Tamper-Proof Record Verification API",
                "algorithm": "SHA-256",
                "total_blocks": len(bc.chain),
                "total_records": max(0, len(bc.chain) - 1),
                "is_valid": bc.is_chain_valid()
            }
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # Fallback to index.html for any other non-API route
        if self._serve_file("index.html", "text/html; charset=utf-8"):
            return

        # Final fallback JSON
        self._set_headers(404, "application/json")
        self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8")) if body else {}

            parsed_url = urlparse(self.path)
            path = parsed_url.path.rstrip("/")

            # Load blockchain
            raw_data = load_blockchain()
            if raw_data:
                bc = Blockchain.from_data(raw_data)
            else:
                bc = Blockchain()

            # 1. Verification endpoint
            if path in ("/api/verify", "/api/verify-record"):
                record_id = data.get("record_id", "").strip()
                student_name = data.get("student_name", "").strip()
                course = data.get("course", "").strip()
                cgpa = data.get("cgpa", "").strip()

                if not record_id:
                    self._set_headers(400, "application/json")
                    self.wfile.write(json.dumps({"error": "record_id is required"}).encode("utf-8"))
                    return

                record_data = f"{student_name}|{course}|{cgpa}" if student_name else data.get("record_data", "")
                generated_hash = generate_hash(record_data)

                found_block = None
                for block in bc.chain:
                    if block.record_id == record_id:
                        found_block = block
                        break

                if not found_block:
                    self._set_headers(404, "application/json")
                    self.wfile.write(json.dumps({
                        "status": "not_found",
                        "message": f"Record ID {record_id} not found in blockchain ledger."
                    }).encode("utf-8"))
                    return

                stored_hash = found_block.record_hash
                is_match = stored_hash == generated_hash

                self._set_headers(200, "application/json")
                self.wfile.write(json.dumps({
                    "status": "verified" if is_match else "tampered",
                    "record_id": record_id,
                    "stored_hash": stored_hash,
                    "generated_hash": generated_hash,
                    "is_genuine": is_match,
                    "block_index": found_block.index,
                    "timestamp": found_block.timestamp
                }).encode("utf-8"))
                return

            # 2. Add record endpoint
            elif path in ("/api/add", "/api/add-record"):
                record_id = data.get("record_id", "").strip()
                student_name = data.get("student_name", "").strip()
                course = data.get("course", "").strip()
                cgpa = data.get("cgpa", "").strip()

                if not all([record_id, student_name, course, cgpa]):
                    self._set_headers(400, "application/json")
                    self.wfile.write(json.dumps({"error": "record_id, student_name, course, cgpa are required"}).encode("utf-8"))
                    return

                if any(b.record_id == record_id for b in bc.chain):
                    self._set_headers(409, "application/json")
                    self.wfile.write(json.dumps({"error": f"Record ID {record_id} already exists."}).encode("utf-8"))
                    return

                record_data = f"{student_name}|{course}|{cgpa}"
                record_hash = generate_hash(record_data)
                bc.add_block(record_id, record_hash)
                save_blockchain(bc)

                self._set_headers(201, "application/json")
                self.wfile.write(json.dumps({
                    "status": "added",
                    "record_id": record_id,
                    "record_hash": record_hash,
                    "block_index": len(bc.chain) - 1,
                    "total_blocks": len(bc.chain)
                }).encode("utf-8"))
                return

            # 3. Default hashing endpoint
            record_id = data.get("record_id")
            record_data = data.get("record_data")

            if not record_id or not record_data:
                self._set_headers(400, "application/json")
                self.wfile.write(json.dumps({"error": "record_id and record_data are required"}).encode("utf-8"))
                return

            record_hash = generate_hash(record_data)

            response = {
                "project": "BlockVerify",
                "record_id": record_id,
                "record_hash": record_hash,
                "algorithm": "SHA-256",
                "status": "Hash generated successfully"
            }

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except Exception as error:
            self._set_headers(500, "application/json")
            self.wfile.write(json.dumps({"error": str(error)}).encode("utf-8"))