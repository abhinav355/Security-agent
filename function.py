import webview
import json
from pc_scan_one import scan_computer


class BridgeAPI:

    def test_bridge(self):
        return "Python is connected!"

    def run_scan(self):
        scan_computer()

        with open("scan-results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data


def start_app():
    window = webview.create_window(
        title="Security Agent",
        url="UI.html",
        js_api=BridgeAPI(),
        width=1200,
        height=800
    )

    webview.start()


if __name__ == "__main__":
    start_app()
