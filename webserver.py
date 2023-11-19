import http.server
import socketserver
import os
import cgi
import urllib.parse

PORT = 8000  # Change this to your desired port number
UPLOADS_DIR = "./uploads"

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Get the URL path and decode it
        url_path = urllib.parse.unquote(self.path)

        # Construct the subfolder path based on the URL path
        subfolder_path = os.path.join(UPLOADS_DIR, url_path.lstrip("/"))
        
        # Create the subfolder if it doesn't exist
        os.makedirs(subfolder_path, exist_ok=True)

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        # Process each uploaded file
        for field_name in form.keys():
            field_item = form[field_name]
            if field_item.filename:
                # Create a new file in the subfolder
                file_path = os.path.join(subfolder_path, os.path.basename(field_item.filename))
                with open(file_path, 'wb') as f:
                    # Write the uploaded file data to the new file
                    f.write(field_item.file.read())

        # Respond with a 200 OK status and a message
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File(s) uploaded successfully.')

# Create an HTTP server with the custom handler
httpd = socketserver.TCPServer(("", PORT), UploadHandler)

print(f"Serving on port {PORT}")
httpd.serve_forever()
