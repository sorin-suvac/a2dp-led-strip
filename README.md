# a2dp-led-strip
RGB LED strip controlled by A2DP signal on Raspberry Pi

Raspberry Pi runs a simple Python webserver based on CGIHTTPRequestHandler. The server has two available endpoints:
/display - enable/disable leds
/mode - the intensity of leds

## pre-requirements
* Raspberry Pi 4 Model B with Ubuntu Server 2022.04.4 LTS (64-bit)
* A2DP streaming source (phone, TV)
* Schematics: https://dordnung.de/raspberrypi-ledstrip/

## setup Raspberry Pi
* connect to Raspberry Pi (ssh)
* enable pulseaudio
  ```shell
  pulseaudio -k
  pulseaudio --start
  ```
* start the pigpio daemon
  ```shell
  sudo pigpiod
  ```
* set bluetooth discoverable mode
  ```shell
  sudo bluetoothctl
  agent on
  default-agent
  pairable on
  discoverable on
  ```
* initiate the pairing process from the phone/TV and play music

## run the webserver
  ```shell
  python3 main.py
  ```
