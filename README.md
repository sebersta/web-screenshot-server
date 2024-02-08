# Web Screenshot Server
Periodically capture screenshots of a webpage and serve them through a web service. It supports various resolutions, rotation, zooming, and grayscale.

## Installation
### docker-compose
A docker-compose.yml file is available as an example. It must be edited to match your needs. You probably want to adjust the port mapping and environment variables.

> *Note:* If you are running it on macOS, you have to disable Airplay Receiver in Settings.
```
version: '3.8'

services:
  web-screenshot-server:
    image: sebersta/web-screenshot-server
    ports:
      - 5000:5000
    environment:
      - URL=https://example.com
      - RESOLUTION=1488x1072
      - ROTATION=-90         
      - ZOOM=200%           
      - GRAYSCALE=True
      - WAIT_TIME=2       
      - UPDATE_INTERVAL=30 
    restart: unless-stopped
```
#### Environment variables
- `URL`: The web page URL to capture screenshots from.
- `RESOLUTION`: The resolution for the screenshot (width x height).
- `ROTATION`: Rotation angle for the image (anticlockwise). 
- `ZOOM`: The zoom level for the web page.
- `GRAYSCALE`: Convert the screenshot to grayscale if set to True.
- `WAIT_TIME`: The time in seconds to wait for the web page to load before capturing the screenshot.
- `UPDATE_INTERVAL`: The interval in seconds at which to update and recapture the screenshot.

Then lauch the container:

```
cd /path/to/docker-compose.yml/
docker-compose up -d
```

## Integration with Kindle
Web Screenshot Server is designed to be work with a jailbroken Kindle and [Online Screensaver](https://www.mobileread.com/forums/showthread.php?t=236104).
The Web Screenshot Server captures screenshots and makes them available for download on the Kindle. The Online Screensaver, running on the Kindle, fetches these images and uses them as the Screensaver.

### Instructions
- Set `RESOLUTION` to match the exact physical resolution of your specific Kindle model. For instance, the Kindle Voyage has a resolution of `1488x1072`.
- Set `GRAYSCALE` to `True`.
- For landscape usage, set `ROTATION` to either -90 or 90.
- To use it with landscape, set `ROTATION` to `-90` or `90`.
- Set `ZOOM` to your preference.
