#include <Arduino.h>
#include <TinyGPS++.h>
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/string.h>

TinyGPSPlus gps;
HardwareSerial &gpsUart = Serial1;

constexpr uint32_t USB_SERIAL_BAUD = 115200;
constexpr uint32_t GPS_BAUD = 9600;

rcl_allocator_t allocator;
rclc_support_t support;
rcl_node_t node;
rcl_publisher_t gpsPublisher;

std_msgs__msg__String gpsMsg;
char gpsPayload[96];

void errorLoop() {
	while (true) {
		delay(100);
	}
}

#define RCCHECK(fn) do { if ((fn) != RCL_RET_OK) { errorLoop(); } } while (0)
#define RCSOFTCHECK(fn) do { (void)(fn); } while (0)

void setup() {
	Serial.begin(USB_SERIAL_BAUD);
  // Serial2.begin(9600, SERIAL_8N1, 16, 17); // (Baud, Config, RX_Pin, TX_Pin)
	gpsUart.begin(GPS_BAUD);

	set_microros_transports();
	delay(2000);

	allocator = rcl_get_default_allocator();

	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));
	RCCHECK(rclc_node_init_default(&node, "teensy_gps_node", "", &support));
	RCCHECK(rclc_publisher_init_default(
		&gpsPublisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
		"/gps/fix"
	));

	gpsMsg.data.data = gpsPayload;
	gpsMsg.data.capacity = sizeof(gpsPayload);
	gpsMsg.data.size = 0;
}

void loop() {
	while (gpsUart.available() > 0) {
		const char nmeaByte = static_cast<char>(gpsUart.read());
		gps.encode(nmeaByte);
	}

	if (gps.location.isUpdated() && gps.location.isValid() && gps.altitude.isValid()) {
		const int written = snprintf(
			gpsPayload,
			sizeof(gpsPayload),
			"Lat: %.6f, Lon: %.6f, Altitude: %.2f m",
			gps.location.lat(),
			gps.location.lng(),
			gps.altitude.meters()
		);

		if (written > 0) {
			gpsMsg.data.size = static_cast<size_t>(
				written < static_cast<int>(sizeof(gpsPayload))
				? written
				: static_cast<int>(sizeof(gpsPayload)) - 1
			);
			RCSOFTCHECK(rcl_publish(&gpsPublisher, &gpsMsg, NULL));
		}
	}
}