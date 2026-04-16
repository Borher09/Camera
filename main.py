from flask import Flask, render_template, jsonify
import cv2
from pyzbar import pyzbar
import threading
import time

app = Flask(__name__)

# Variável para armazenar o último QR Code lido
dados_qrcode = {
    "conteudo": "Aguardando leitura...",
    "timestamp": "-"
}

def loop_camera():
    global dados_qrcode
    # Tenta abrir a câmera (0 é a padrão)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro: Câmera não detectada!")
        return

    print("Câmera ligada. Servidor rodando em http://127.0.0.1:5000")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detecta QR Codes
        qrcodes = pyzbar.decode(frame)

        for qrcode in qrcodes:
            conteudo = qrcode.data.decode('utf-8')
            
            # Atualiza os dados para o site
            dados_qrcode = {
                "conteudo": conteudo,
                "timestamp": time.strftime("%H:%M:%S")
            }
            print(f"Lido: {conteudo}")
            
            # Pequena pausa para não ler o mesmo código mil vezes por segundo
            time.sleep(1.5)

        # Se quiser ver a imagem da câmera no PC, descomente a linha abaixo:
        # cv2.imshow("Scanner", frame)
        if cv2.waitKey(1) & 0xFF == 27: break

    cap.release()
    cv2.destroyAllWindows()

# Rota para abrir a página
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o site "pegar" os dados
@app.route('/dados')
def get_dados():
    return jsonify(dados_qrcode)

if __name__ == '__main__':
    # Rodar a câmera em segundo plano
    threading.Thread(target=loop_camera, daemon=True).start()
    # Rodar o servidor Web
    app.run(debug=False, port=5000)