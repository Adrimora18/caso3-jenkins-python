"""Servidor de pruebas independiente que carga la aplicación desplegada."""

import json
import runpy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APLICACION = Path("/despliegue/current/app.py")


class ServidorPruebas(BaseHTTPRequestHandler):
    """Expone el estado real del código desplegado por Jenkins."""

    def responder(self, codigo, datos):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        ruta = self.path.split("?", 1)[0]
        if ruta not in ("/", "/health"):
            self.responder(404, {"error": "Ruta no encontrada"})
            return

        if not APLICACION.is_file():
            self.responder(503, {
                "status": "pending", "detail": "Sin despliegue"
            })
            return

        try:
            aplicacion = runpy.run_path(str(APLICACION))
            if ruta == "/health":
                datos = aplicacion["health"]()
            else:
                datos = {"message": aplicacion["saludar"]("desde Jenkins")}
            self.responder(200, datos)
        except (OSError, KeyError, RuntimeError) as error:
            self.responder(500, {"status": "error", "detail": str(error)})


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("0.0.0.0", 5000), ServidorPruebas)
    print("Servidor de pruebas en el puerto 5000", flush=True)
    servidor.serve_forever()
