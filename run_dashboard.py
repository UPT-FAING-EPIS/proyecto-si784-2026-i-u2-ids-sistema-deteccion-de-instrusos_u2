from web.app import app
from src.network_utils import detect_network_info

if __name__ == "__main__":
    print("[INFO] Dashboard local: http://127.0.0.1:5000")

    try:
        network_info = detect_network_info()
        print(f"[INFO] Dashboard en red: http://{network_info.ip_address}:5000")
        print(f"[INFO] Laboratorio remoto: http://{network_info.ip_address}:5000/attack-lab")
    except Exception as error:
        print(f"[AVISO] No se pudo detectar la IP local: {error}")

    app.run(host="0.0.0.0", port=5000, debug=True)
