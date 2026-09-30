import json
import os
import re
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        prodotti = []
        
        def analizza_file(filename, categoria, cartella):
            if filename.startswith('.'):
                return None
            
            prezzo = 10
            nome_pulito = filename
            
            match = re.search(r'_p(\d+)(\.[^.]+)?$', filename, re.IGNORECASE)
            if not match:
                match = re.search(r'_(\d+)(\.[^.]+)?$', filename)
            
            if match:
                prezzo = int(match.group(1))
                estensione = match.group(2) if match.group(2) else os.path.splitext(filename)[1]
                parte_base = filename[:match.start()]
                nome_pulito = parte_base + estensione

            return {
                "nome": nome_pulito,
                "nome_file_reale": filename,
                "categoria": categoria,
                "prezzo": prezzo,
                "url": f"/{cartella}/{filename}"
            }

        # Scansiona le cartelle nel contesto di esecuzione Vercel
        for cartella in ['librerie', 'programmi']:
            cat_nome = "CLI-Libreria" if cartella == 'librerie' else "CLI-Tool"
            path_dir = os.path.join(os.getcwd(), cartella)
            if os.path.exists(path_dir):
                for f in os.listdir(path_dir):
                    prod = analizza_file(f, cat_nome, cartella)
                    if prod:
                        prodotti.append(prod)
                        
        self.wfile.write(json.dumps(prodotti).encode('utf-8'))
        return