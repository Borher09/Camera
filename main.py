import cv2
from pyzbar import pyzbar
import serial
import time
import sys

# =========================
# CONFIGURAÇÕES
# =========================
PORTA_SERIAL = "COM5"   # ajuste para a porta correta do Arduino
BAUD_RATE = 9600
CAMERA_INDEX = 0
TEMPO_COOLDOWN = 1.0    # intervalo mínimo entre leituras válidas

# Mapeamento do QR Code para o comando do Arduino
MAPA_IDS = {
    "id1": "ESQ",
    "id2": "DIR"
}


def conectar_arduino():
    try:
        arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1, write_timeout=1)
        time.sleep(2)  # aguarda o reset automático do Arduino ao abrir a serial
        arduino.reset_input_buffer()
        arduino.reset_output_buffer()
        print(f"Conectado ao Arduino na porta {PORTA_SERIAL}")
        return arduino
    except serial.SerialException as e:
        print(f"ERRO: não foi possível conectar ao Arduino na porta {PORTA_SERIAL}")
        print(f"Detalhe: {e}")
        sys.exit(1)


def abrir_camera():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("ERRO: não foi possível abrir a câmera.")
        sys.exit(1)
    return cap


def enviar_comando(arduino, comando):
    try:
        mensagem = f"{comando}\n".encode("utf-8")
        arduino.write(mensagem)
        arduino.flush()
        print(f"Comando enviado: {comando}")
    except serial.SerialException as e:
        print(f"ERRO ao enviar comando pela serial: {e}")


def ler_resposta_arduino(arduino):
    try:
        while arduino.in_waiting > 0:
            resposta = arduino.readline().decode("utf-8", errors="ignore").strip()
            if resposta:
                print(f"Arduino: {resposta}")
    except serial.SerialException:
        pass


def main():
    arduino = conectar_arduino()
    cap = abrir_camera()

    print("Câmera aberta. Aponte um QR Code com id1 ou id2.")
    print("Pressione 'q' para encerrar.")

    ultimo_id_processado = None
    ultimo_envio = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERRO: falha ao capturar imagem da câmera.")
                break

            codigos = pyzbar.decode(frame)
            id_valido_visivel = None

            for code in codigos:
                id_lido = code.data.decode("utf-8", errors="ignore").strip().lower()
                x, y, w, h = code.rect

                if id_lido in MAPA_IDS:
                    cor = (0, 255, 0)
                    texto = f"QR reconhecido: {id_lido}"
                    id_valido_visivel = id_lido
                else:
                    cor = (0, 0, 255)
                    texto = f"QR desconhecido: {id_lido}"

                cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
                cv2.putText(
                    frame,
                    texto,
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    cor,
                    2
                )

            # lógica de disparo: envia apenas uma vez por aparição do QR
            if id_valido_visivel is not None:
                agora = time.time()

                if (
                    id_valido_visivel != ultimo_id_processado
                    and (agora - ultimo_envio) >= TEMPO_COOLDOWN
                ):
                    comando = MAPA_IDS[id_valido_visivel]
                    enviar_comando(arduino, comando)
                    ultimo_id_processado = id_valido_visivel
                    ultimo_envio = agora
            else:
                # libera nova leitura quando o QR sair da tela
                ultimo_id_processado = None

            ler_resposta_arduino(arduino)

            cv2.imshow("Sistema de Separacao", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Encerrado manualmente pelo usuário.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        arduino.close()
        print("Sistema encerrado com segurança.")


if __name__ == "__main__":
    main()