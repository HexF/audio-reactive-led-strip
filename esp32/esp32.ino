/*
*This example works for ESP32 and uses the NeoPixelBus library instead of the one bundle
*
*/
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <NeoPixelBus.h>

// Set to the number of LEDs in your LED strip
#define NUM_LEDS 150
// Maximum number of packets to hold in the buffer. Don't change this.
#define BUFFER_LEN 1024

// Wifi and socket settings
const char* ssid     = "";
const char* password = "";
unsigned int localPort = 7777;
char packetBuffer[BUFFER_LEN];

uint16_t N = 0;

WiFiUDP port;
// Network information
// IP must match the IP in config.py
IPAddress ip(192, 168, 1, 139);
// Set gateway to your router's gateway
IPAddress gateway(192, 168, 1, 254);
IPAddress subnet(255, 255, 255, 0);
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> ledstrip(NUM_LEDS, 2);

void setup() {
    Serial.begin(115200);
    WiFi.config(ip, gateway, subnet);
    WiFi.begin(ssid, password);
    Serial.println("");
    // Connect to wifi and print the IP address over serial
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    port.begin(localPort);
    ledstrip.Begin();//Begin output
    ledstrip.Show();//Clear the strip for use
}

void loop() {
    // Read data over socket
    int packetSize = port.parsePacket();
    // If packets have been received, interpret the command
    if (packetSize) {
        int len = port.read(packetBuffer, BUFFER_LEN);
        for(int i = 0; i < len; i+=5) {
            packetBuffer[len] = 0;
            N = (packetBuffer[i] << 8) | packetBuffer[i+1];
            RgbColor pixel((uint8_t)packetBuffer[i+2], (uint8_t)packetBuffer[i+3], (uint8_t)packetBuffer[i+4]);//color
            ledstrip.SetPixelColor(N, pixel);//N is the pixel number
        } 
        ledstrip.Show();
    }
}
