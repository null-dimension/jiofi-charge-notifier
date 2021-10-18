import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import time

# For debugging:

# import logging
# import http.client
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
# headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

start_time = time.time()
total_time = 0

# Set the minimum charge to notify
MIN_CHARGE = 40

# Set the maximum charge to notify
MAX_CHARGE = 95

while True:
    try:
        total_time += 1
        print("Checking battery for %s times" % total_time)
        r = requests.get("http://jiofi.local.html/cgi-bin/en-jio-4-1/mStatus.html")
        soup = BeautifulSoup(r.text, "html.parser")
        battery = soup.find(id="lDashBatteryQuantity")
        charging_status = soup.find(id="lDashChargeStatus")
        charging_status = charging_status.string
        battery_percent = int(battery.string[:-1])
        toaster = ToastNotifier()

        print("Current charge is %s %%" % battery_percent)
        print("Battery is currently %s" % charging_status)
        if battery_percent >= MAX_CHARGE and charging_status == "Charging":
            toaster.show_toast("Battery is almost full!", "%s %% charged" % battery_percent, duration=30)
        elif battery_percent <= MIN_CHARGE and charging_status == "Discharging":
            toaster.show_toast("Battery needs charge!", "%s %% left" % battery_percent, duration=30)
        
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))
    except:
        print("An error has occured. Retrying...")
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))
