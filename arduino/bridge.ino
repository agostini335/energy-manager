/*
* Arduino Wireless Communication Tutorial
*       Example 1 - Receiver Code
*                
* by Dejan Nedelkovski, www.HowToMechatronics.com
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
#include <SPI.h>
#include <RF24.h>


/*RF24 radio(9, 8); // CE, CSN*/
RF24 radio(9, 10); // CE, CSN
/* address ricezione*/
const byte address[6] = "00001";

/* address trasmissione*/
const byte address_tx[6] = "00002";

/**
 * led ricezione
 */
int ledPin = 7;

void setup() {
  Serial.begin(9600);
  radio.begin();
  
  radio.openWritingPipe(address_tx);
  radio.openReadingPipe(0, address);
  
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  pinMode(ledPin, OUTPUT);   
  Serial.println();
  
  
  /*
  
  radio_tx.openWritingPipe(address_tx);
  radio_tx.setPALevel(RF24_PA_MIN);
  
  radio_tx.stopListening();*/
  
 
}
void loop() {
  if (radio.available()) {
    digitalWrite(ledPin, HIGH);
    delay(20);     
    digitalWrite(ledPin, LOW);  
    char text[50] = "";    
    radio.read(&text, sizeof(text));
    radio.stopListening();
    radio.write(&text, sizeof(text));
    radio.startListening();
    Serial.println(text);
      
  }  
}
