from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox() 
driver.install_addon("./bibbotmod.xpi")
driver.install_addon("./cookies.xpi")

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)

        url = None
        if "url" in query_components and len(query_components["url"]) > 0:
            url = query_components["url"][0]

        if self.path.startswith("/get") and url is not None:
            

            driver.get("https://google.com")
            driver.get(url)
            #driver.execute_script("window.localStorage.setItem('key','value');")
            #options = driver.execute_script("return window.localStorage.getItem('providerOptions');")
            #print(options)

            #presence_of_element_located Web
            if url != "https://google.com":
                found = False
                while not found:
                    found = True
                    try:
                        driver.find_element(By.XPATH, "//*[@id='bibbot-loader']")
                    except NoSuchElementException:
                        found = False

                print("Found loader")

                while found:
                    found = True
                    try:
                        driver.find_element(By.XPATH, "//*[@id='bibbot-loader']")
                    except NoSuchElementException:
                        found = False

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

