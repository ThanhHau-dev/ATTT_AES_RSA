from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Khai báo biến toàn cục để lưu dữ liệu từ POST
data = []

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

   

    def do_POST(self):
        if self.path == "/api/data":
            try:
                # Đọc dữ liệu JSON từ body của request
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data_received = json.loads(post_data.decode())

                print(f"Dữ liệu nhận được: {data_received}")

                # Lưu dữ liệu vào biến toàn cục
                data.append(data_received)

                # Trả phản hồi xác nhận đã nhận dữ liệu
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                response = {"message": "Dữ liệu đã được lưu thành công"}
                self.wfile.write(json.dumps(response).encode())

            except json.JSONDecodeError:
                # Xử lý lỗi JSON không hợp lệ
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                response = {"error": "Dữ liệu không phải JSON hợp lệ"}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)  # Nếu không tìm thấy đường dẫn
            self.end_headers()


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Phản hồi với dữ liệu đã lưu từ POST
        response = {"kq1": data}
        self.wfile.write(json.dumps(response).encode())

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
# khi GET được gọi, sẽ lấy dữ liệu từ biến cục bộ này
