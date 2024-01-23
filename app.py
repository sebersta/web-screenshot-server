from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import numpy as np
from PIL import Image
import io, time, os 
from threading import Thread
from flask import Flask, send_file

url = os.getenv('URL', 'https://example.com')
resolution = os.getenv('RESOLUTION', '1920x1080').split('x')
rotation = int(os.getenv('ROTATION', '0'))
zoom = os.getenv('ZOOM', '100%')
grayscale = os.getenv('GRAYSCALE', 'True') == 'True'
wait = int(os.getenv('WAITTIME', '2'))
update_interval = int(os.getenv('UPDATE_INTERVAL', '30'))

def GetImage(url, wait, resolution, zoom, rotation, grayscale):

    # Set up the Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    # Set window size 
    driver.set_window_size(int(resolution[0]), int(resolution[1]))
    driver.execute_script(f"document.body.style.zoom='{zoom}';")
    driver.execute_script("document.body.style.overflow = 'hidden';")
    time.sleep(wait)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    image = Image.open(io.BytesIO(screenshot))

    # Convert to grayscale
    if grayscale:
        image = image.convert('L')

    image = image.rotate(rotation, expand=True)
    return image

latest_image = GetImage(url, wait, resolution, zoom, rotation, grayscale)

def update_image(update_interval):
    global latest_image
    while True:
        # Wait for the specified update interval
        time.sleep(update_interval)

        # Get and update the image
        latest_image = GetImage(url, wait, resolution, zoom, rotation, grayscale)

app = Flask(__name__)
@app.route('/')
def display_image():
    if latest_image is not None:
        img_io = io.BytesIO()
        latest_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    else:
        return "Image not available yet."

if __name__ == '__main__':
    # Start the background thread
    thread = Thread(target=update_image, args=(update_interval,))
    thread.daemon = True
    thread.start()

    # Start the Flask web server on 0.0.0.0 to make it accessible over the network
    app.run(host='0.0.0.0', debug=True)
