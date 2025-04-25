// MetroCharRequest.cpp for Metro M4 Airlift Lite

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BNO08x.h>

// Define pins for Metro M4 Airlift Lite
#define BNO08X_I2C_SDA 20  // Default SDA pin for Metro M4
#define BNO08X_I2C_SCL 21  // Default SCL pin for Metro M4

// For SPI mode, we need CS pin
#define BNO08X_SPI_CS 10
#define BNO08X_INT 9

// For SPI mode we also need a RESET
#define BNO08X_RESET -1  // Not used for I2C

Adafruit_BNO08x bno08x(BNO08X_RESET);
sh2_SensorValue_t sensorValue;
unsigned long currentTime = 0;

// Function to set sensor reports
void setReports() {
  if (!bno08x.enableReport(SH2_ACCELEROMETER)) {
    Serial.println("Could not enable accelerometer");
  } else {
    Serial.println("Accelerometer enabled");
  }
  if (!bno08x.enableReport(SH2_GYROSCOPE_CALIBRATED)) {
    Serial.println("Could not enable gyroscope");
  } else {
    Serial.println("Gyroscope enabled");
  }
  if (!bno08x.enableReport(SH2_ROTATION_VECTOR)) {
    Serial.println("Could not enable rotation vector");
  } else {
    Serial.println("Rotation vector enabled");
  }
}

//_______________SETUP__________________________________
void setup(void) {
  // Initialize Serial for debugging
  Serial.begin(115200);
    Serial.print("Initializing BNO08x Sensor...");

  while (!Serial) {
    delay(10); // Wait for Serial to be ready
  }

  // Initialize I2C communication
  Wire.begin(BNO08X_I2C_SDA, BNO08X_I2C_SCL);

  // Initialize the BNO08x sensor
  if (!bno08x.begin_I2C()) {
    Serial.println("Failed to find BNO08x chip");
    delay(1000);
    return; // Stop execution if initialization fails
  } else {
    Serial.println("Found BNO08x chip");
    setReports();
  }
}

//___________LOOP______________________________________
void loop() {
  currentTime = millis();

  // Retrieve sensor data
  if (bno08x.getSensorEvent(&sensorValue)) {
    Serial.println("Sensor data retrieved successfully");

    // Print accelerometer data
    Serial.print("Accelerometer: ");
    Serial.print(sensorValue.un.accelerometer.x);
    Serial.print(", ");
    Serial.print(sensorValue.un.accelerometer.y);
    Serial.print(", ");
    Serial.println(sensorValue.un.accelerometer.z);

    // Print gyroscope data
    Serial.print("Gyroscope: ");
    Serial.print(sensorValue.un.gyroscope.x);
    Serial.print(", ");
    Serial.print(sensorValue.un.gyroscope.y);
    Serial.print(", ");
    Serial.println(sensorValue.un.gyroscope.z);

    // Print rotation vector data
    Serial.print("Rotation Vector: ");
    Serial.print(sensorValue.un.rotationVector.real);
    Serial.print(", ");
    Serial.print(sensorValue.un.rotationVector.i);
    Serial.print(", ");
    Serial.print(sensorValue.un.rotationVector.j);
    Serial.print(", ");
    Serial.println(sensorValue.un.rotationVector.k);

    // Format data as a CSV string
    String data1 = String(millis()) + ", " +
                   String(sensorValue.un.accelerometer.x, 6) + ", " +
                   String(sensorValue.un.accelerometer.y, 6) + ", " +
                   String(sensorValue.un.accelerometer.z, 6) + ", " +
                   String(sensorValue.un.gyroscope.x, 6) + ", " +
                   String(sensorValue.un.gyroscope.y, 6) + ", " +
                   String(sensorValue.un.gyroscope.z, 6) + ", " +
                   String(sensorValue.un.rotationVector.real, 6) + ", " +
                   String(sensorValue.un.rotationVector.i, 6) + ", " +
                   String(sensorValue.un.rotationVector.j, 6) + ", " +
                   String(sensorValue.un.rotationVector.k, 6);

    // Send data over UART
    Serial.println(data1);
  } else {
    Serial.println("Failed to retrieve sensor data");
  }

  delay(100); // Add a small delay to avoid flooding the Serial Monitor
}