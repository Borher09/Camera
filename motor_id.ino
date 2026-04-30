#include <Servo.h>

// Declaração dos dois motores
Servo motor1;
Servo motor2;

// Definição dos pinos
const int pinoMotor1 = 10;
const int pinoMotor2 = 11;

// Calibração (ajuste conforme necessário)
int tempoUmaVolta = 800; 

void setup() {
  Serial.begin(9600); // Inicia a comunicação serial
  
  motor1.attach(pinoMotor1);
  motor2.attach(pinoMotor2);
  
  // Garante que ambos comecem parados
  motor1.write(90);
  motor2.write(90);
  
  Serial.println("Digite o ID do motor (1 ou 2) para girar:");
}

void loop() {
  // Verifica se há dados chegando no Serial
  if (Serial.available() > 0) {
    int idRecebido = Serial.parseInt(); // Lê o número digitado

    if (idRecebido == 1) {
      Serial.println("Girando Motor 1...");
      executarCiclo(motor1);
    } 
    else if (idRecebido == 2) {
      Serial.println("Girando Motor 2...");
      executarCiclo(motor2);
    }
  }
}

// --- FUNÇÃO PARA EXECUTAR O CICLO COMPLETO ---
// Passamos o motor como parâmetro para a função saber qual girar
void executarCiclo(Servo &motorAlvo) {
  // 1. Gira Direita
  motorAlvo.write(180);
  delay(tempoUmaVolta);
  motorAlvo.write(90);
  
  delay(1000); // Pequena pausa entre inversão

  // 2. Gira Esquerda
  motorAlvo.write(0);
  delay(tempoUmaVolta);
  motorAlvo.write(90);

  // 3. Pausa final de 10 segundos
  Serial.println("Ciclo finalizado. Aguardando 10 segundos...");
  delay(10000); 
}