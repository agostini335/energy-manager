#include <LiquidCrystal_I2C.h>




#include "EmonLib.h"             
#include <Wire.h>

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3,POSITIVE); //LCD I2C address

EnergyMonitor emon1;             // carico
EnergyMonitor emon2;             // produzione
EnergyMonitor emon3;             // tensione

//calibrazione voltmetro
#define VOLT_CAL 195.99

//pin 
const int pin_carico = 2;
const int pin_produzione= 3;
const int pin_tensione = 0;

//trasmissione
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

//variabili correnti
double Irms;
double Vrms;
float tensione = -1; 
int carico = -1;
int produzione = -1;
int immissione = -1;

void updateDisplay(int v,int c,int p,int i){ 
  //immissione
  lcd.setCursor(0,3);
  if(i>-4000 and i<4000){
    if(immissione>0){
        lcd.print("Immissione      ");
        printChar(11,3," ");   
        lcd.print(allineaQuattro(i));
        lcd.print(" W");
    }else{
        i=-i;
        lcd.print("Prelievo      ");
        printChar(11,3," ");   
        lcd.print(allineaQuattro(i));
        lcd.print(" W");
    }
   }else{
    lcd.print("Immissione error");
  }
  //tensione
  lcd.setCursor(0,0);
  if(v>=0 and v<300){
    lcd.print("Tensione            ");
    printChar(11,0," ");
    lcd.print(allineaQuattro(v));
    lcd.print(" V");
  }else{
    lcd.print("Tensione error");
  }
  //carico
  lcd.setCursor(0,1);
  if(c>=0 and c<9000){
    lcd.print("Carico          ");
    printChar(11,1," ");
    lcd.print(allineaQuattro(c));
    lcd.print(" W");
  }else{
    lcd.print("Carico error");
  }
  //produzione
  lcd.setCursor(0,2);
  if(p>=0 and p<9000){
    lcd.print("Produzione         ");
    printChar(11,2," ");
    lcd.print(allineaQuattro(p));
    lcd.print(" W");
  }else{
    lcd.print("Produzione error");
  }
}

void printChar(int c,int r,String ch){
    lcd.setCursor(c,r);
    lcd.print(ch);    
}

String allineaQuattro(int n){
  if(n<1000 and n>99)
    return(" "+(String)n);
  if(n<100 and n>9)
    return("  "+(String)n);
  if(n<10)
    return("   "+(String)n);
  return (String)n;
}

void setup() {
  //LCD INIT
  lcd.begin(20,4);
  lcd.setCursor(0,0);
  lcd.print("INIT");
  //EMON INIT
  Serial.begin(9600);
  emon1.current(pin_carico,29);
  emon2.current(pin_produzione,29);
  emon3.voltage(pin_tensione,VOLT_CAL, 1.7); //pin,calibration,phase_shift
  //TRANS INIT
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

float tensioneCorretta(float t){
    return t-((t*(-0.81))+186.3); //ipotesi crescita lenta  
}


void loop() {
  //Tensione
  emon3.calcVI(20,2000);
  tensione=emon3.Vrms;
 // Serial.print(tensione);  
 //  Serial.print(" ");
 //  Serial.print(tensioneCorretta(tensione));
 //  Serial.println(" ");
  tensione=tensioneCorretta(tensione); //todo refactor
  //Carico 
  Irms = emon1.calcIrms(1480);
  carico=Irms*tensione;
  //Produzione
  Irms = emon2.calcIrms(1480);
  produzione=Irms*tensione;
  //Immissione
  immissione=produzione-carico;
  /******************UPDATE*******************/
  updateDisplay(tensione,carico,produzione,immissione);
  /******************Trnasmission*************/
 
  
  const char text[200]="val:"; //refactor
  char buffer[30];
  char car[10];
  char pro[10];
  char imm[10];
  sprintf(buffer,"%d",(int)tensione);
  sprintf(car,"%d",carico);
  sprintf(pro,"%d",produzione);
  sprintf(imm,"%d",immissione);
  
  strcat(text,buffer);
  strcat(text,";");
  strcat(text,car);
  strcat(text,";");
  strcat(text,pro);
  strcat(text,";");
  strcat(text,imm);
  strcat(text,";");



  
  Serial.print(buffer);
  
  
  radio.write(&text, sizeof(text));
  
  //reinit 
  carico = -1;
  produzione = -1;
  immissione = -1;
  tensione = -1;  
}
