import pychrome
import json

def on_download_started(event):
    print("Download started:", json.dumps(event, indent=2))

def on_download_finished(event):
    print("Download finished:", json.dumps(event, indent=2))

def main():
    # Connect to the Chrome instance
    browser = pychrome.Browser(url="http://127.0.0.1:9222")

    # Get the first tab
    tab = browser.list_tab()[0]
    tab.start()

    # Set up event listeners
    tab.set_listener("Network.requestWillBeSent", on_download_started)
    tab.set_listener("Network.responseReceived", on_download_finished)

    # Enable the Network domain to receive events
    tab.call_method("Network.enable")

    print("Listening for downloads... Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        tab.stop()

if __name__ == "__main__":
    main()
