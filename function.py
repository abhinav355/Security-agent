import webview
import json
from pc_scan_one import scan_computer

class BridgeAPI:

    def test_bridge(self):
        return "Python is connected!"

    def run_scan(self):

        scan_computer()

        with open("scan-results.json","r",encoding="utf-8") as f:
            data = json.load(f)

        return data


window = webview.create_window(
    "Security Agent",
    "UI.html",
    js_api=BridgeAPI(),
    width=1100,
    height=700
)

webview.start()
