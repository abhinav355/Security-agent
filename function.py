import webview
from pc_scan_one import scan_computer

class BridgeAPI:

    def test_bridge(self):
        return "Python is connected!"

    def run_scan(self):
        return scan_computer()


def start_app():
    window = webview.create_window(
    "Security Agent",
    "UI.html",
    js_api=BridgeAPI(),
    width=920,
  height=620,
    resizable=True
    )
    webview.start()


if __name__ == "__main__":
    start_app()