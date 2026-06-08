import webview

class BridgeAPI:
    """
    This class connects your Python code to your teammate's HTML.
    Any function you put here can be used by their UI.
    """
    def test_bridge(self):
        return "Python is connected!"

def start_app():
    # This is the pywebview window element looking for UI.html
    window = webview.create_window(
        title="Our Team Project",
        url="UI.html",
        js_api=BridgeAPI(),
        width=800,
        height=600
    )
    webview.start()

if __name__ == "__main__":
    start_app()