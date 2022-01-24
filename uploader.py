#!/bin/python3
import requests
import os
from subprocess import Popen, PIPE
import clipboard
from notifypy import Notify

# Config
IMAGE_SERVER = "http://localhost:8000"
SKYNET_PORTAL = "https://siasky.net"
LOGIN_TOKEN = "beepboop"

client = SkynetClient()
process = Popen(["maim", "-s"], stdout=PIPE)
stdout = process.communicate()[0]

# Upload to sia
r = requests.post(SKYNET_PORTAL + "/skynet/skyfile/image.png", files={"file": stdout})
skylink = r.json()["skylink"]

# Get signing key
headers = {
    "Authorization": LOGIN_TOKEN
}

r = requests.post(IMAGE_SERVER + "/api/upload", params={"image_id": skylink}, headers=headers)
data = r.json()
if "error" in data.keys():
    # Error notification
    notification = Notify()
    notification.title = "Crop"
    notification.message = f"Upload failed. Details: {data['error']}"
    notification.send()
    exit(1)

# Output to user
print(data)
clipboard.copy(data["image"])
os.system("paplay ~/Tools/CaptureSound.wav")

