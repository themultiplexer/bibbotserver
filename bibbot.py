from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse, parse_qs
import requests

hostName = "localhost"
serverPort = 8281

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options) 
driver.install_addon("./bibbotmod.xpi")
driver.install_addon("./cookies.xpi")

sites = ["https://www.spiegel.de",
        "https://www.zeit.de",
        "https://www.wiwo.de",
        "https://www.welt.de",
        "https://www.tagesspiegel.de",
        "https://www.sueddeutsche.de",
        "https://sz-magazin.sueddeutsche.de",
        "https://www.handelsblatt.com",
        "https://www.berliner-zeitung.de",
        "https://www.morgenpost.de",
        "https://www.nordkurier.de",
        "https://www.abendblatt.de",
        "https://www.moz.de",
        "https://www.noz.de",
        "https://www.waz.de",
        "https://www.heise.de",
        "https://www.maz-online.de",
        "https://www.lr-online.de",
        "https://www.nachrichten.at",
        "https://ga.de",
        "https://www.ksta.de",
        "https://www.rundschau-online.de",
        "https://rp-online.de",
        "https://www.tagesanzeiger.ch",
        "https://www.falter.at",
        "https://www.stuttgarter-zeitung.de",
        "https://www.stuttgarter-nachrichten.de",
        "https://www.ostsee-zeitung.de",
        "https://www.stimme.de",
        "https://kurier.at",
        "https://freizeit.at",
        "https://www.diepresse.com",
        "https://www.sn.at",
        "https://www.kleinezeitung.at",
        "https://www.vn.at",
        "https://www.thueringer-allgemeine.de",
        "https://www.mopo.de",
        "https://www.saechsische.de",
        "https://www.freiepresse.de",
        "https://www.haz.de",
        "https://www.lvz.de",
        "https://www.dnn.de",
        "https://www.swp.de",
        "https://www.ruhrnachrichten.de",
        "https://www.businessinsider.de",
        "https://www.badische-zeitung.de",
        "https://www.stern.de",
        "https://www.mittelbayerische.de",
        "https://www.tagblatt.de",
        "https://www.mz.de",
        "https://www.capital.de",
        "https://www.iz.de",
        "https://www.shz.de",
        "https://www.aerztezeitung.de",
        "https://www.geo.de",
        "https://www.nzz.ch",
        "https://www.manager-magazin.de"
      ]

class MyServer(BaseHTTPRequestHandler):

    def error(self, text):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>BibBot Server</title></head>", "utf-8"))
        self.wfile.write(bytes("<h2>%s</h2>" % text, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)

        url = None
        if "url" in query_components and len(query_components["url"]) > 0:
            url = query_components["url"][0]

        if self.path.startswith("/get") and url is not None:
            print("Checking...", url)

            try:
                r = requests.head(url)
                print(r.status_code)
                if r.status_code == 302:
                    url = r.headers.get('location')
                    print("Following redirect", url)
                    
            except requests.ConnectionError:
                self.error("URL is down.")
                return

            if not url.startswith(tuple(sites)):
                self.error("BibBot does not support this page yet :/")
                return
            
            print("Loading...", url)
            driver.get("https://google.com")
            driver.get(url)

            print("Waiting for Bibbot extension to load")

            if url != "https://google.com":
                
                try:
                    WebDriverWait(driver, 5.0).until(ec.presence_of_element_located((By.XPATH, "//*[@id='bibbot-loader']")))
                except TimeoutException:
                    self.error("BibBot Extension not initilizaing. (Timeout)")
                    return

                print("Found loader")

                try:
                    WebDriverWait(driver, 15.0).until(ec.invisibility_of_element_located((By.XPATH, "//*[@id='bibbot-loader']")))
                except TimeoutException:
                    self.error("BibBot Extension did not load article. (Timeout)")
                    return

                print("Loaded article")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(driver.page_source, "utf-8"))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<p>URL Param: %s</p>" % url, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

