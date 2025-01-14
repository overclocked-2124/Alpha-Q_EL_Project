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
const char* ssid = "";
const char* password = "";

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
    float temperature_front = sensors.getTempCByIndex(0);
    float temperature_back = sensors.getTempCByIndex(1);

    // Read INA219 sensor data
    float current_teg = ina219_1.getCurrent_mA() / 1000.0; // Convert mA to A
    float current_solar = ina219_2.getCurrent_mA() / 1000.0; // Convert mA to A
    float voltage_solar = ina219_2.getBusVoltage_V();
    float voltage_teg = ina219_1.getBusVoltage_V();
    float power_solar = ina219_2.getPower_mW() / 1000.0; // Convert mW to W
    float power_teg = ina219_1.getPower_mW() / 1000.0; // Convert mW to W

    // Prepare the JSON data
    String json = "{";
    json += "\"temperature_front\": " + String(temperature_front) + ",";
    json += "\"temperature_back\": " + String(temperature_back) + ",";
    json += "\"current_teg\": " + String(current_teg) + ",";
    json += "\"current_solar\": " + String(current_solar) + ",";
    json += "\"voltage_solar\": " + String(voltage_solar) + ",";
    json += "\"voltage_teg\": " + String(voltage_teg) + ",";
    json += "\"power_solar\": " + String(power_solar) + ",";
    json += "\"power_teg\": " + String(power_teg);
    json += "}";

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
