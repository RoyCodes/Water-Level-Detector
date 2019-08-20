# Water Level Detector

This project uses an ultrasonic sensor and a Raspberry Pi Zero to send sensor data through Soracom's Cellular Cloud to Azure's Anomaly Detector API.

Azure's Anomaly detector let's us offload logic to the cloud. Increase battery life and reduce the hardware requirements

Using cellular connectivity instead of Wi-Fi or ethernet allows this IoT device to go where it otherwise would have no internet connectivity. Soracom gives us the cellular connection and also access to several services which will help us remotely manage our IoT device, and also help streamline our API call to Azure's Anomaly Detector API.

Let's get started!

## Hardware Requirements

* Raspberry Pi Zero
* Huawei 3G USB Modem and USB OTG adapter cable (MS2131i) 
* Soracom Global IoT SIM Card
* 8GB+ Class 10 SD Card and Micro-SD Card Reader 
* USB-A to Micro-USB Cable
* Ultrasonic range finder (HC-SR04)
* Perma-Proto Breadboard and Color-coded Wires 
* Red LED
* 330 ohm Resistor

All of the hardware used for this project is available in Soracom's [IoT Starter Kit with Raspberry Pi and IoT Sim](https://www.soracom.io/store/soracom-cellular-iot-starter-kit/).

## Set up

### 1. Hardware

And the tutorial for setting up the kit: [Soracom IoT Starter Kit with Raspberry Pi](https://developers.soracom.io/en/start/iot-starter-kit/raspberry-pi/)


### 2. Azure

* Create Anomaly Detector. They currently offer a free pricing tier woo hoo!

[Anomaly Detector API Reference](https://westus2.dev.cognitive.microsoft.com/docs/services/AnomalyDetector/operations/post-timeseries-entire-detect)

Make note of our key and endpoint, which is listed under the "Quick start" section of the resource.

### 3. Soracom

* Soracom Beam - HTTP to HTTP translation. Prevents us from having to store our API Key on the IoT device. Frees us up to change to endpoint in the future without having to make any changes on the device.

* Soracom Napter - Quick remote access to device over cellular. SSH. Don't have to install anything on the IoT device. 

## Installation

### 1. Use Soracom Napter to establish an SSH connection over cellular to the device.

Here's a quick 1 minute video on how to accomplish this:
[IoT Remote Access with SORACOM Napter](https://www.youtube.com/watch?v=wky_BHC1PUQ)

### 2. Download this repo to the device

```bash
wget PATH_TO_REPO
```

## Usage

### Run the script

```bash
python ultrasonic_beam.py 60
```

Adding 60 to the end let's the script know to take a sensor reading every 60 seconds. This is because we've got our Azure Anomaly Detector API granularity set to "minutely".

Once the count of readings hits 12, it will beging sending the readings to Anomaly Detector.

## Contributing

Pull requests are welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)