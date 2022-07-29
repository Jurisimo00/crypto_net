import          http.server
import          json
import          socketserver
import          cgi
import          requests
import          sys, signal
from urllib     import parse
from utils      import *

LOG_GET_FILE = "./get.log.txt"
LOG_POST_FILE = "./post.log.txt"

port = 8080
host = "localhost"
api_base_url = "https://api.coingecko.com/api/v3"

if sys.argv[1:]:
    try:
        port = int(sys.argv[1])
    except Exception as e:
        print(f"Unable to parse port number -> {str(e)}")

host_url = f"http://{host}:{port}"

"""
Genera il file coinsdata.json, il motivo per cui è neccessario generare questo file è dato 
dal fatto che deriva da una richiesta GET a coingecko cun una grande quantità di dati.
Pper evitare che questa richiesta possa risultare 'bloccante' ho deciso di salvare i dati 
su un file, che è sicuramente più veloce da leggere.
"""
def fetch_coin_list():
    path = "/coins/list"
    res = requests.get(api_base_url + path)
    json_data = res.json()
    try:
        with open("./coinsdata.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Couldn't read file -> {str(e)}")
        return False
    return True

"""
Chiedo a coingecko una lista delle critpovalute di tendenza
"""
def fetch_trending_coins():
    path = "/search/trending"
    res = requests.get(api_base_url + path)
    return res.json()

"""
Chiedo a coingecko maggiori dettagli su una criptovaluta specificandoil suo id in query string
"""
def get_single_coin(id):
    path = f"/coins/{id}"
    res = requests.get(api_base_url + path)
    return res.json()

"""
Questa funzione non fa altro che reperire dal file coinsdata un singolo record di una criptovaluta.
"""
def single_coin_info(params):
    with open("./coinsdata.json", "r") as json_file:
        data = json.load(json_file)
        sym = params["symbol"]
    for c in data:
        if c["symbol"] == sym:
            return get_single_coin(c["id"])
    return None

"""
Classe derivata da SimpleHTTPRequstHandler, si occupa di gestire tutte le chiamate http in arrivo al server
"""
class ReqHandle(http.server.SimpleHTTPRequestHandler):

    """
    I due seguenti metodi di log, come presumibile dal nome, servono a salvare su un file di log tutte le richieste ricevuto dal server.
    """
    def log_get(self):
        with open(LOG_GET_FILE, "a") as f:
            log_str = "GET request\nPath: {0}\nFrom: {1}\nHeaders: {2}\n\n"
            f.write(log_str.format(self.path, self.client_address, self.headers))
            
    def log_post(self):
        with open(LOG_POST_FILE, "a") as f:
            log_str = "POST request\nPath: {0}\nFrom: {1}\nHeaders: {2}\n\n"
            f.write(log_str.format(self.path, self.client_address, self.headers))

    """
    I due seguenti metodi servono a cambiare headers in base al tipo di oggetto in risposta ad una richiesta GET o POST.
    """
    def _set_headers_json(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _set_headers_html(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    """
    In questo metodo si controlla il percorso richiesto dal client, con una serie di espressioni condizionali,
    in caso sia presente il percorso specificato si risponde di conseguenza.
    """
    def guess_get_request(self):
        splitted = parse.urlsplit(self.path)
        path = splitted.path
        params = parse.parse_qs(splitted.query)
        params = { k: v[0] for k, v in params.items() }

        if path == "/is_authorized":
            ip, port = self.client_address
            user = find_user_by_ip(ip)
            if user is not None:
                return {"success": True, "message": "user is authorized!"}
            return {"success": False, "message": "user is not authorized!"}
        
        if path == "/trending":
            with open("./pages/trending.html", "r") as f:
                self._set_headers_html()
                self.wfile.write(bytes(f.read(), "utf8"))
                return True

        if path == "/trending_coins":
            return fetch_trending_coins()
            
        if path == "/coins/list":
            with open("./coinsdata.json", "r") as json_file:
                return json.load(json_file)

        if path == "/coins/single":
            return single_coin_info(params)

        if path == "/buysell":
            create_buy_sell_page(params["symbol"])
            with open("./pages/buysell.html", "r") as f:
                self._set_headers_html()
                self.wfile.write(bytes(f.read(), "utf8"))
                return True

        if path == "/userpage":
            with open("./pages/userpage.html", "r") as f:
                self._set_headers_html()
                self.wfile.write(bytes(f.read(), "utf8"))
                return True

        if path == "/login":
            with open("./pages/login.html", "r") as f:
                self._set_headers_html()
                self.wfile.write(bytes(f.read(), "utf8"))
                return True

        if path == "/coins/coin_info":
            create_coin_info_page(params["symbol"], params["coin_id"])
            with open("./pages/coin_info.html", "r") as f:
                self._set_headers_html()
                self.wfile.write(bytes(f.read(), "utf8"))
                return True
        return None

    """
    Simile al metodo soprastante, solo che le risposte sono tutte di tipo json.
    """
    def guess_post_request(self, body):
        path = parse.urlsplit(self.path).path
        if path == "/authenticate":
            ip, port = self.client_address
            delete_sessions_with_same_ip(ip)
            if authenticate_user(body["username"], body["pwd"], ip):
                return { "success": True, "message": "authentication successful!" }
            return { "success": False, "message": "wrong password or username!" }

        if path == "/update_wallet":
            ip, port = self.client_address
            user = find_user_by_ip(ip)
            if user is not None:
                coin = Coin(body["crypto_name"], body["symbol"], body["crypto_amount"])
                update_user(user, coin, body["dollar_amount"])
                return { "success": True, "message": "transaction successful!" }
            return { "success": False, "message": "user is not anuthenticated anymore!" }

        if path == "/userdata":
            ip, port = self.client_address
            user = find_user_by_ip(ip)
            if user is not None:
                return { "success": True, "data": user }
            return { "success": False, "message": "user not authorized!" }

        if path == "/logout":
            ip, port = self.client_address
            if logout_user(ip):
                return { "success": True, "message": "logout successful!" }
            return { "success": False, "message": "user was not logged!" }
        return None            


    """
    Entry point delle richieste GET, lascio che guess_get_request() decida la risposta,
    poi in base al tipo di oggetto mando una risposta di conseguenza.
    """
    def do_GET(self):
        self.log_get()
        res = self.guess_get_request()
        if res is None:
            """
            lascio che il server mandi una pagina di errore.
            """
            http.server.SimpleHTTPRequestHandler.do_GET(self)
            return
        #any request whose not found as a form of a file, is supposed to be a json data request
        self._set_headers_json()
        self.wfile.write(bytes(json.dumps(res), "utf8"))

    """
    Similmente al caso soprastante lascio che guess_post_request() decida la rispota, solo che qui si fa un ulteriore controllo,
    ovvero il content-type della richiesta deve essere per forza json, anche per request body vuoti.
    Se non c'è il campo content-type settato ad application/json nell'header allora mando un messaggio di errore al chiamante.
    """
    def do_POST(self):
        self.log_post()
        ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
        if ctype != "application/json":
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"success": False, "message": "content type must be json"}), "utf8"))
            return
        length = int(self.headers.get("content-length"))
        body = None
        if length > 0:
            body = json.loads(self.rfile.read(length))
        res = self.guess_post_request(body)
        self._set_headers_json()
        if res is None:
            self.send_response(404)
        elif "success" in res:
            self.wfile.write(bytes(json.dumps(res), "utf8"))
        
server = socketserver.ThreadingTCPServer(("localhost", port), ReqHandle)

"""
Gestione dell'interrupt generato dalla pressione di Ctrl+C.
"""
def handle_interrupt(signal, frame):
    print("Exit...")
    try:
        if(server):
            server.server_close()
    finally:
        sys.exit()

def main():
    server.daemon_threads = True
    server.allow_reuse_address = True
    signal.signal(signal.SIGINT, handle_interrupt)

    print(f"Serving on -> {host_url}")
    try:
        while True:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == "__main__":
    main()
