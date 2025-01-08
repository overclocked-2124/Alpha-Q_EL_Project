#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_INA219.h>
#include <Wire.h>

// DS18B20 Temperature Probes
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// INA219 Sensors
Adafruit_INA219 ina219_1(0x40);  // Default I2C address (0x40)
Adafruit_INA219 ina219_2(0x44);  // Change address if needed (e.g., 0x41)

// LDRs
#define LDR1_PIN 32
#define LDR2_PIN 33
#define LDR3_PIN 34

int enabled = 1;

// Replace with your network credentials
const char* ssid = "gvdinesh_airtel";
const char* password = "sringeri123";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize DS18B20 sensors
  sensors.begin();
  sensors.setResolution(12);  // Set resolution to 12 bits

  // Initialize INA219 sensors
  if (!ina219_1.begin() || !ina219_2.begin()) {
    Serial.println("Failed to find INA219 sensors");
    enabled = 0;
  }
  else {
  Serial.println("INA219 Sensors Initialized");
  }

  // Initialize LDRs
  pinMode(LDR1_PIN, INPUT);
  pinMode(LDR2_PIN, INPUT);
  pinMode(LDR3_PIN, INPUT);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.1.9:5000/receive_data"); // Replace with your server's IP and port

    // Read DS18B20 temperatures
    sensors.requestTemperatures();
    float temp1 = sensors.getTempCByIndex(0);
    float temp2 = sensors.getTempCByIndex(1);
    float temp3 = sensors.getTempCByIndex(2);

    // Read LDR values
    int ldr1 = analogRead(LDR1_PIN);
    int ldr2 = analogRead(LDR2_PIN);
    int ldr3 = analogRead(LDR3_PIN);

    // Prepare the JSON data
    String json = "{";
    json += "\"temperature1\": " + String(temp1) + ",";
    json += "\"temperature2\": " + String(temp2) + ",";
    json += "\"temperature3\": " + String(temp3) + ",";
    json += "\"ldr1\": " + String(ldr1) + ",";
    json += "\"ldr2\": " + String(ldr2) + ",";
    json += "\"ldr3\": " + String(ldr3);
    json += "}";
    if (enabled==1){
  
      // Read INA219 sensor data
      float busVoltage1 = ina219_1.getBusVoltage_V();
      float current1 = ina219_1.getCurrent_mA();
      float power1 = ina219_1.getPower_mW();

      float busVoltage2 = ina219_2.getBusVoltage_V();
      float current2 = ina219_2.getCurrent_mA();
      float power2 = ina219_2.getPower_mW();

      json += "\"busVoltage1\": " + String(busVoltage1) + ",";
      json += "\"current1\": " + String(current1) + ",";
      json += "\"power1\": " + String(power1) + ",";
      json += "\"busVoltage2\": " + String(busVoltage2) + ",";
      json += "\"current2\": " + String(current2) + ",";
      json += "\"power2\": " + String(power2) + ",";
    }

    // Set the Content-Type header
    http.addHeader("Content-Type", "application/json");

    // Send the JSON payload
    int httpCode = http.POST(json);
    if (httpCode > 0) {
      if (httpCode == HTTP_CODE_OK) {
        String response = http.getString();
        Serial.println("Data sent successfully");
        Serial.println(response);
      } else {
        Serial.print("HTTP error code: ");
        Serial.println(httpCode);
      }
    } else {
      Serial.println("Error sending data");
      Serial.print("Error details: ");
      Serial.println(http.errorToString(httpCode).c_str());
    }
    http.end();
  } else {
    Serial.println("WiFi disconnected. Attempting to reconnect...");
    WiFi.begin(ssid, password);
  }
  delay(5000); // Send data every 5 seconds
}