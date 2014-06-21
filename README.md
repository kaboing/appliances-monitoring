appliances-monitoring
=====================

Monitor your appliances connected to a plugwise network

# Installation

Install python-plugwise: (https://bitbucket.org/hadara/python-plugwise/wiki/Home)
```
hg clone https://bitbucket.org/hadara/python-plugwise
cd python-plugwise
sudo python setup.py install
```
Install nexmo-message: (https://github.com/marcuz/libpynexmo)
```
pip install -e git+https://github.com/marcuz/libpynexmo.git#egg=nexmomessage
```

Edit the `config.cfg`-file:
* Add the appliances you want to monitor as new devices (device1, device2, etc). Update the devices-list
* For each device:
 * Config the mac adress
 * Set the correct type
 * Set the sms_name you want
* Set the phone numbers you want sms's to be sent to. International format, no leading + or zeroes. For instance: 4670123456
* In the Nexmo section, set your api-key and api-secret

# Run
`python monitor.py`
