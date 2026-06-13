from threading import Timer
import webbrowser

from src.network_utils import detect_network_info
from web.app import app


def open_dashboard():
    webbrowser.open("http://127.0.0.1:5000/")


if __name__ == "__main__":
    print("[INFO] TrafficWatch IDS iniciado")
    print("[INFO] Dashboard local: http://127.0.0.1:5000")

    try:
        network_info = detect_network_info()
        print(f"[INFO] Dashboard en red: http://{network_info.ip_address}:5000")
        print(f"[INFO] Laboratorio remoto: http://{network_info.ip_address}:5000/attack-lab")
    except Exception as error:
        print(f"[AVISO] No se pudo detectar la IP local: {error}")

    Timer(1.2, open_dashboard).start()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
