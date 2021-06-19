#include <RF24.h>
#include <printf.h>
#include "EmonLib.h"   

/*
 * TOROIDE
 */
EnergyMonitor emon1;             // caricoBoiler
int carico = -1;
const int pin_carico = 0;
int tensione=230;
double Irms;
/* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
RF24 radio(9, 8); // CE, CSN
const byte address[6] = "00001";
/*
 * SONDA NCT
 */
int pin= A3;
double VOLT=5;
double v;/*voltaggio tra 0 e 1023*/
double volt;/* voltaggio reale tra o e 5 volt*/
double Rt;/* resistenza del termistore*/
double R1=10000;/*resistenza in ohm che abbiamo messo noi*/
double temp;/* temperatura in Kelvin*/
double Temperatura;
/**
 * led ricezione
 */
int ledPin = 7;






void setup() {
  //EMON INIT
  emon1.current(pin_carico,29);
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();  
  pinMode(ledPin, OUTPUT);
}

void loop() {
  /**lettura toroide**/
  Irms = emon1.calcIrms(1480);
  carico=Irms*tensione;
  if(carico<-100 || carico>5000){
     carico=-9999;
  }
  char car[50];
  sprintf(car,"%d",carico);
  char boiler[50]="0;";//codifica 0 per boiler
  strcat(boiler,car);
  Serial.println(boiler);    
  delay(200);
  /**ricezione**/
  if (radio.available()) {  
    digitalWrite(ledPin, LOW);
    char text[50] = "1;";//codifica 1 per la stringa completa, 0 per boiler
    char ptext[50] = "";  
    char tens[3]="";
    radio.read(&ptext, sizeof(text));
    strcat(text,ptext);
    /**estrai tensione**/
    tens[0]=text[0];
    tens[1]=text[1]; 
    tens[2]=text[2];
    tensione=atoi(tens);
    
    //check
    if(tensione>300 || tensione<200){
      tensione=230;
    }  
    
    

    /**lettura sonda ntc**/
    v=analogRead(pin);/*leggiamo il valore della tensione ai capi di R1*/
    volt=VOLT*v/1023;/* riportiamo la tensiOne tra 0 e 5 volt con una proporzione*/
    Rt=R1*(VOLT/volt-1);/*resistenza del termistore*/
    temp=1/(0.001125308852122+(0.000234711863267*log(Rt))+(0.000000085663516*log(Rt)*log(Rt)*log(Rt)));/*calcolo la temperatura con la formula di Steinhart-Hart*/
    Temperatura=temp-273.15;/* gradi Chelsius*/
    
     

     /**concatenazione**/
    char temp[50];
    sprintf(car,"%d",carico);
    dtostrf(Temperatura,5, 2, temp);
    strcat(text,car);
    strcat(text,";");
    strcat(text,temp);
    Serial.println(text);    
  }
  digitalWrite(ledPin, HIGH); 
  //delay(800);
  

  
}
