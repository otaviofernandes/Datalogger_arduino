#include "DHT.h"
#include "RTClib.h"
#include <SD.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#define DHTPIN 9
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

LiquidCrystal_I2C lcd(0x27, 16, 2);

File myFile;

RTC_DS3231 rtc;
 
int botao = 2; //botão para acionar log
int botao_menos = 7; //botão para diminuir tempo
int botao_mais = 6; //botão para aumentar tempo
int led = 3; // indica se está gravando ou não logs
bool registralog = 0; //estado do log
int tp = 1;
int tp1 = 1;
String tempo = "001";


void setup() {
 Wire.begin();
 lcd.init();
 lcd.setBacklight(HIGH);
 
 Serial.begin(9600); 
 pinMode(botao, INPUT);
 pinMode(botao_mais, INPUT);
 pinMode(botao_menos, INPUT);
 pinMode(led, OUTPUT);
  
 if (SD.begin()) {
  Serial.println("SD Card pronto para uso.");
  }
 else {
  Serial.println("Falha na inicialização do SD Card.");
  return;
  }
 if(! rtc.begin()) {
  Serial.println("DS3231 não encontrado");
  while(1);
  }
 if(rtc.lostPower()){
  Serial.println("DS3231 OK!");
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
 Serial.println(F("DHT22 test!"));
 dht.begin();

 myFile = SD.open("log.txt", FILE_WRITE);
 if (myFile){
  myFile.close();
 }
 else {
  Serial.println("Erro ao Abrir Arquivo .txt");
 }
}


void loop() {
 digitalWrite(led, LOW);   
 if(digitalRead(botao) == LOW){
  registralog = !registralog;
  myFile = SD.open("log.txt", FILE_WRITE);
  if ((registralog) == 1){
   myFile.println("begin");
  }
  else{
   myFile.println("end");
  }
  myFile.close();
  delay(500); 
 }
 if(digitalRead(botao_mais) == LOW){
  tp ++;
  delay(200);
 }
 if(digitalRead(botao_menos) == LOW){
  tp --;
  delay(200);
 }
 if (tp > 9){
  tp = 9;
 }
 if (tp < 1) {
  tp = 1;
 }
 if (tp == 9){
  tempo = "600";
  tp1 = 600;
 }
 else if (tp == 8){
  tempo = "300";
  tp1 = 300;
 }
 else if (tp == 7){
  tempo = "120";
  tp1 = 120;
 }
 else if (tp == 6){
  tempo = "060";
  tp1 = 60;
 }
 else if (tp == 5){
  tempo = "030";
  tp1 = 30;
 }
 else if (tp == 4){
  tempo = "010";
  tp1 = 10;
 }
 else if (tp == 3){
  tempo = "005";
  tp1 = 5;
 }
 else if (tp == 2){
  tempo = "002";
  tp1 = 2;
 }
 else if (tp == 1){
  tempo = "001";
  tp1 = 1;
 }
 lcd.setCursor(0,0);
 lcd.print("Intervalo entre");  
 lcd.setCursor(0,1);
 lcd.print("leituras(s): " + tempo); 
 
 if ((registralog) == 1){
  leitura(tp1, led);
 }
 else{
  lcd.setBacklight(HIGH);
  delay(100);   
  }
}


void leitura(int tp1, int led){
 lcd.setBacklight(LOW);
 digitalWrite(led, HIGH);
 DateTime now = rtc.now(); 
 float h = dht.readHumidity();
 float t = dht.readTemperature();
 float f = dht.readTemperature(true);
 float hic = dht.computeHeatIndex(t, h, false); 
 String linha = String(now.day()) + "." +  String(now.month()) + "." + String(now.year()) + "-" + String(now.hour()) + "." +  String(now.minute()) + "." + String(now.second()) + " " + String(h) + " " + String(t);
 myFile = SD.open("log.txt", FILE_WRITE);
 myFile.println(linha);
 myFile.close();
 delay(tp1*1000);
}
