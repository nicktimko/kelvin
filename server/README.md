# Server

## Hardware

* Raspberry Pi 3B+
* Adafruit LoRa 900 MHz Bonnet

## Software

* Raspbian installed headless (SSH only)

With `raspi-config`, enable I2C and SPI.

```
sudo apt install \
    python-smbus \
    i2c-tools

python3 -m pip install \
    adafruit-circuitpython-ssd1306 \
    adafruit-circuitpython-framebuf \
    adafruit-circuitpython-rfm9x

curl -sSL -O https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/main/examples/font5x8.bin

# install system packages
source /etc/os-release
curl -sSL https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
curl -sSL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update
sudo apt-get install -y grafana influxdb

sudo systemctl enable grafana-server.service
sudo systemctl start grafana-server.service
sudo systemctl unmask influxdb.service
sudo systemctl enable influxdb.service
sudo systemctl start influxdb.service

influx -execute "CREATE USER grafana WITH PASSWORD 'xxxxxxxx' WITH ALL PRIVILEGES"
influx -execute "CREATE USER kelvin WITH PASSWORD 'xxxxxxxx'"
influx -execute "CREATE DATABASE kelvin"
influx -execute "GRANT ALL ON kelvin TO kelvin"


# InfluxDB 2.x doesn't seem OK for RasPi?
# curl -sSL https://repos.influxdata.com/influxdb.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdb.gpg > /dev/null
# export DISTRIB_CODENAME=$(lsb_release -sc)
# echo "deb [signed-by=/etc/apt/trusted.gpg.d/influxdb.gpg] https://repos.influxdata.com/debian ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
# sudo apt-get update
# sudo apt-get install influxdb2
```
