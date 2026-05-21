
#include <Servo.h>

// --- Definição dos Pinos ---
#define S1_PIN 5  // Garra
#define S2_PIN 11 // Braço 2 (Profundidade)
#define S3_PIN 6  // Braço 1 (Altura)
#define S4_PIN 3  // Base

// --- Instanciando os Servos ---
Servo s1, s2, s3, s4;

// --- Variáveis de Posição Atual ---
int pos1 = 70; 
int pos2 = 70;
int pos3 = 70;
int pos4 = 70;

// --- Configurações de Movimento ---
int velocidade = 15; // Milissegundos entre cada grau
int tempoPausa = 800; // Pausa entre as etapas p1, p2...

void setup() {
  Serial.begin(9600);

  // Conectando os servos
  s1.attach(S1_PIN);
  s2.attach(S2_PIN);
  s3.attach(S3_PIN);
  s4.attach(S4_PIN);

  // Leva o braço suavemente para a posição inicial (p1)
  Serial.println("Inicializando braço...");
  executarMovimento(130, 70, 74, 97); 
  delay(1000);
}

void loop() {
  Serial.println("Iniciando Sequencia Automatica...");

  // Executa a sequência baseada nas suas posições p1 a p7
  p1(); delay(tempoPausa);
  p2(); delay(tempoPausa);
  p3(); delay(tempoPausa);
  p4(); delay(tempoPausa);
  p5(); delay(tempoPausa);
  p6(); delay(tempoPausa);
  p7(); delay(tempoPausa);

  Serial.println("Sequencia finalizada. Reiniciando em 2 segundos...");
  delay(2000);
}

// --- FUNÇÃO MESTRE DE MOVIMENTAÇÃO COORDENADA (Corrigida para "x") ---
void executarMovimento(int d1, int d2, int d3, int d4) {
  
  // TRAVA DE SEGURANÇA: Garante que nenhum comando passe de 70° ou 130°
  d1 = constrain(d1, 70, 130);
  d2 = constrain(d2, 70, 130);
  d3 = constrain(d3, 70, 130);
  d4 = constrain(d4, 70, 130);

  // Enquanto qualquer servo não estiver no destino, continue movendo
  while (pos1 != d1 || pos2 != d2 || pos3 != d3 || pos4 != d4) {
    
    // Servo 1 (Garra)
    if (pos1 < d1) pos1++;
    else if (pos1 > d1) pos1--;
    s1.write(pos1);

    // Servo 2 (Braço 2)
    if (pos2 < d2) pos2++;
    else if (pos2 > d2) pos2--;
    s2.write(pos2);

    // Servo 3 (Braço 1)
    if (pos3 < d3) pos3++;
    else if (pos3 > d3) pos3--;
    s3.write(pos3);

    // Servo 4 (Base)
    if (pos4 < d4) pos4++;
    else if (pos4 > d4) pos4--;
    s4.write(pos4);

    delay(velocidade); // Controla a suavidade do movimento
  }
  servosPos(); 
}

// --- Funções de Posição ---

void p1() { 
  Serial.println("P1: Fechando Garra");
  executarMovimento(100, 70, 74, 97);  
}

void p2() { 
  Serial.println("P2: Abrindo Garra");
  executarMovimento(80, 70, 74, 97); 
}

void p3() {
  Serial.println("P3: Posicionando para pegar");
  executarMovimento(70, 70, 80, 97);   
}

void p4() {
  Serial.println("P4: Fechando garra no objeto");
  executarMovimento(130, 70, 70, 97);  
}

void p5() {
  Serial.println("P5: Levantando e Girando Base");
  executarMovimento(130, 90, 74, 130); 
}

void p6() {
  Serial.println("P6: Posicionando no destino");
  executarMovimento(130, 80, 70, 130); 
}

void p7() {
  Serial.println("P7: Soltando objeto");
  executarMovimento(70, 90, 70, 130);  
}

// --- Monitoramento ---
void servosPos() {
  Serial.print("S1:"); Serial.print(pos1);
  Serial.print(" | S2:"); Serial.print(pos2);
  Serial.print(" | S3:"); Serial.print(pos3);
  Serial.print(" | S4:"); Serial.println(pos4);
}
