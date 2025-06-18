#include <ESP8266WiFi.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ThingSpeak settings
const char* host = "api.thingspeak.com"; 
const char* writeAPIKey = "YOUR_API_KEY"; // Replace with your ThingSpeak Write API Key

// DHT sensor setup
#define DHTPIN D4       // GPIO2
#define DHTTYPE DHT11   // Use DHT22 if needed
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(1000); // Safer delay

  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Connected to WiFi");
}

void loop() {
  // Read sensor values
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // in Celsius

  // Validate readings
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("❌ Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  Serial.print("🌡️ Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C  💧 Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  // Connect to ThingSpeak
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("❌ Connection to ThingSpeak failed");
    return;
  }

  // Create URL
  String url = "/update?api_key=";
  url += writeAPIKey;
  url += "&field1=";
  url += String(temperature);
  url += "&field2=";
  url += String(humidity);

  // Send HTTP GET request
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("✅ Data sent to ThingSpeak");

  delay(20000); // ThingSpeak limit is 15 sec, using 20 sec for safety
}
