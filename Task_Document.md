# Rover CSE Recruitment — Task Guide

## Evaluation Approach

Submissions are evaluated on correctness, clarity, and engineering process. Complete
solutions are appreciated, but thoughtful partial progress with clear debugging and
learning notes is also valued and can also be submitted.

---

# Category 1: Embedded Systems & MicroROS

## Objective

Read and process data from onboard sensors (GPS, IMU, Encoder) on a Teensy 4.1
microcontroller, and optionally publish the data as ROS 2 topics using MicroROS.

## Submission Requirements

Submit your `platformio.ini` file along with all relevant Teensy source code for
sensor integration and MicroROS implementation.

If anyone wishes to they also come and test their codes on actual hardware and see if it will work any attempts even failed or succesfull will be rewarded extra credits for this depending on the outcome.

## Hardware Details

### Microcontroller
- **Teensy 4.1** — ARM Cortex-M7 microcontroller

### GPS Module
- **7Semi L86-M33 GPS/GNSS Breakout Board**
  - **Datasheet:** [7Semi L86-M33 GPS GNSS Breakout Board](https://7semi.com/l86-m33-gps-gnss-breakout-board/?srsltid=AfmBOorb7h6uKE5F2D6D4SoCVoVuQPeEgG30AyWD7evtRqXZlzTI44tq)

### IMU Module
Choose one of the following options:

- **BNO055**: 9-DOF Absolute Orientation Sensor
  (3-axis accelerometer, 3-axis gyroscope, 3-axis magnetometer)
  - [BNO055 Arduino Library](https://github.com/arduino-libraries/BNO055)

### Encoder Module
- **OE-775 DC Motor Magnetic Encoder** — 7 PPR (Pulses Per Revolution)

---

## Task Breakdown

Make sure to only do task based on the numebr assigned to u in the excel sheet

### Task 1: GPS Reading

**Objective:** Read GPS data from the 7Semi L86-M33 module and parse NMEA sentences.

**What You Will Implement:**
- Configure the appropriate baud rate
- Parse incoming NMEA sentences
- Extract: Latitude, Longitude, Altitude, Timestamp
- Print formatted GPS data to the serial monitor

**Expected Output:**
```
Lat: 13.195987
Lon: 80.224016
Altitude: 15.34 m
```

---

### Task 2: IMU Sensor Reading & Data Fusion

**Objective:** Read IMU data and output orientation (roll, pitch, yaw).

**BNO055**
- Initialize **I2C communication** on Teensy
- Configure BNO055 to output the appropriate orientation
- Read Euler angles (roll, pitch, yaw) directly
- Print sensor data

**Expected Output:**
```
Roll: 2.34°
Pitch: -1.56°
Yaw: 45.67°

```

---

### Task 3: Encoder-Based RPM & Odometry (Interrupt-Driven)

**Objective:** Calculate RPM and distance traveled using OE-775 encoder pulses with
interrupt handling.

**About Hardware Setup:**
- Encoder provides quadrature output (2 channels for direction detection)
- Encoder resolution: **7 PPR** (Pulses Per Revolution)
- More about the encoder is given the requiement doc

**Expected Output:**
```
RPM: 45.6
Distance: 2.35 meters
Pulses: 47
Direction: Forward
```

---

## Advanced Task: MicroROS Integration (Genral Task for everyone)

**Objective:** Publish your assigned sensor's readings (GPS, IMU, or Encoder) as
ROS 2 topics from the Teensy.

**What You Will Implement:**
- Initialize **micro_ros_arduino** on Teensy
- Create a ROS 2 node on Teensy
- Publish the following topics (based on your assigned sensor):
  - `/gps/fix` — GPS data 
  - `/imu/data` — IMU data 
  - `/motor/rpm` — RPM data 
  - Make sure to choose the appropriate data foramt tht will be used to send the these messages list down wt u chose and Why.
---

## Evaluation Criteria

| Task | Criteria |
|------|----------|
| **Task 1 — GPS** | Accurate NMEA parsing, correct latitude/longitude extraction, works with real satellites or a simulator |
| **Task 2 — IMU** | Correct orientation angles, proper calibration, smooth sensor readings |
| **Task 3 — Encoder** | Accurate RPM calculation, correct distance estimation, proper interrupt handling without missed pulses |
| **Advanced — MicroROS** | Successfully publishes the topic from the assigned sensor |

---

# Category 2: ROS2 & Simulation

## Objective

Set up and run a basic rover simulation workflow using ROS 2 and Gazebo. 

## What Will Be Provided
- Rover URDF file
- Mesh package containing STL files referenced by the URDF

## Core Tasks (Mandatory to be Done for Everyone)
1. Spawn the provided rover model in Gazebo and verify that the robot appears correctly.
2. Configure and run a differential drive controller using `ros2_control`.
3. Publish odometry and TF transforms correctly so rover motion is reflected
   consistently in the frame tree.

## Bonus Tasks (Based on the task number assigned to you)
**Task 1 :** - Build a ROS 2 keyboard teleoperation node for driving the rover in simulation.

**Task 2 :** Create a single launch file that starts the full simulation stack in one command.

**Task 3 :** Visualize the rover in RViz2 with a correct TF tree.

## Submission Requirements
- Your modified URDF, configuration, and launch files, along with any other relevant
  output files (e.g., a screenshot of the TF tree or a recording of the moving rover).
- A short README describing what you implemented and how did yuou implement it.

---

# Category 3: Automation & Dashboard (Here All the task are common for everyone and the task number rule is can be ignored here)

**Theme:** Build a component or prototype for the rover's **operator dashboard /
ground control UI**.

---

## Task 3.1: Systemd Service Orchestration

> **Note:** This category has a single task that can be attempted by everyone.
> 100% completion is **not** required — we strongly encourage you to submit your
> progress and outcomes regardless of how far you get.

**Scenario (Fictional):**
You are given a rover ground control system that requires two services to start
simultaneously at the correct trigger:
- A ROS 2 bridge service
- A telemetry logging service

**Task:**
Configure these services to run on system startup, subject to the conditions outlined
in [Section 3.1.1](#311-conditions).

> Avoid using utilities involving timers, initializers, and wrappers or abstractions
> around native tools (e.g., `cron`). Research and find the appropriate native tool
> for this.

### 3.1.1 Conditions

- Both services require a network connection and **must only begin once the network
  is available**.
- The services can start as standalone programs, but **extra credits will be awarded**
  for configuring them to autostart together.
- Dependency ordering must be ensured — services should start only when their
  dependencies are satisfied.

---

## Task 3.2: Breaking

**Task:** Intentionally break the automation service you established — cause it to
misbehave or fail. A full **crash** is highly recommended.

Document in detail the exact steps taken. Credits are awarded as follows:

| Outcome |
|---------|
| Error in ROS 2 service |
| Error in telemetry logging service |
| Error in service configuration |
| Crash the automation due to errors |
Provide a detailed write-up of the method used to cause the crash.

---

## Task 3.3: Debugging

**Task:** Now treat the broken system as if it was sabotaged by an unknown entity
(say, Tung Tung Sahur) and perform a thorough **bug hunt**.

You are required to provide a detailed report containing:
- Relevant system logs and kernel hints
- Your interpretation of the logs
- Your approach to fixing the issue
- The final result

Every conclusion must be inferred from logs and system hints. If you are interested,
you can extend Sections 3.2 and 3.3 to break the system at a kernel level, attach a
recovery debugger, and fix the kernel. These two sections are your playground to flex
your knowledge. Good luck.

---
