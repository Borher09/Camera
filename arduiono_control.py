import serial
import time

# Troque 'COM3' pela porta onde seu Arduino estiver conectado
# porta_serial = 'COM3' 
# conexao = serial.Serial(porta_serial, 9600)

def enviar_comando(regiao):
    """ Envia o número da região para o Arduino via Serial """
    try:
        # conexao.write(regiao.encode())
        print(f"Comando '{regiao}' enviado ao hardware!")
    except Exception as e:
        print(f"Erro ao enviar comando: {e}")