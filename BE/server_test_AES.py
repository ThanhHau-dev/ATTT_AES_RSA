from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Biến cục bộ lưu dữ liệu đã mã hóa và key đi kèm
encrypted_data = None
client_key = None



# mọi người code mã hóa trong đoạn này
# đây là hàm ví dụ mã hóa cơ bản, để mô phỏng luồng dữ liệu hoạt động
# từ cliet gửi POST rồi nhận GET
def simple_xor_encrypt_decrypt(data, key):
    """Hàm mã hóa/giải mã đơn giản bằng XOR."""
    key_bytes = key.encode()
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])
# ####################################



class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, AES-Key")
        self.end_headers()

    def do_POST(self):
        global encrypted_data, client_key  # Dùng biến cục bộ

        if self.path == "/api/data":
            try:
                # Đọc dữ liệu JSON từ body của request
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data_received = json.loads(post_data.decode())

                # Trích xuất 'data' và 'key' từ object client gửi
                raw_data = data_received["data"]
                client_key = data_received["key"]

                # Mã hóa dữ liệu bằng key của client
                encrypted_data = simple_xor_encrypt_decrypt(
                    raw_data.encode(), client_key
                )

                # Trả về xác nhận mã hóa thành công
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response = {"message": "Dữ liệu đã được mã hóa và lưu trữ thành công."}
                self.wfile.write(json.dumps(response).encode())

            except (json.JSONDecodeError, KeyError):
                # Xử lý lỗi nếu JSON không hợp lệ hoặc thiếu key/data
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                response = {"error": "Dữ liệu không hợp lệ hoặc thiếu trường bắt buộc."}
                self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        global encrypted_data, client_key  # Dùng biến cục bộ

        # Lấy key từ header của request
        provided_key = self.headers.get("AES-Key")

        if not provided_key or provided_key != client_key:
            # Trả về lỗi nếu key không hợp lệ
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Invalid AES key")
            return

        if encrypted_data:
            # Giải mã dữ liệu trước khi trả về
            decrypted_data = simple_xor_encrypt_decrypt(encrypted_data, client_key).decode()
            
            # Trả về dữ liệu đã giải mã
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response = {"data": decrypted_data}
            self.wfile.write(json.dumps(response).encode())
        else:
            # Không có dữ liệu để trả về
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"No data available")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()


# Tạm thời xong httpRequest 
# Luồng dữ liệu hoạt động như sau:
# POST sẽ nhận dữ liệu từ client, sau đó lưu vào biến rỗng cục bộ
# khi GET được gọi, sẽ lấy dữ liệu từ biến cục bộ này, và được mã hóa bằng một hàm ví dụ cơ bản
# khi GET thì phải có key đã POST mới GET được, lưu ý, chắc là phải cần chỉnh lại header ở FE lúc GET
# Hiện tại đang test api bằng postman
