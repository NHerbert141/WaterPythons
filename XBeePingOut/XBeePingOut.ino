#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3); // Arduino RX, TX (Serial Dout, Din)

void setup() 
{ 
  // Initiate Xbee-Arduino communications at 9600 baud
  XBee.begin(9600);
}

void loop() 
{
  while(!XBee.available())
  {
    //  send the number 2 followed by the endl char
    XBee.write(0x32);
    XBee.write(0x0A);
    delay(1000); 
  }
}
