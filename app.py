import http.server
import socketserver

# Configurar el puerto en el que se ejecutará el servidor
port = 8000

# Configurar el manejador para servir archivos estáticos
handler = http.server.SimpleHTTPRequestHandler

# Crear el servidor
with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Servidor web en el puerto {port}")

    # Mantener el servidor en ejecución
    httpd.serve_forever()