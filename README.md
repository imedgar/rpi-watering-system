# rpi-watering-system

[rpi-watering-system](https://github.com/imedgar/rpi-watering-system) is a Raspberry Pi automated watering system based on Ben Eagan's project (https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc). 

## Built With

rpi-watering-system is built with the following Stack:


* rpi-watering-system web interface is written using the [Flask](http://flask.pocoo.org/) Python microframework. For now, it runs 
on Python 2.7. which is most probably already installed on your machine.

* This interface allows to send request to the Raspberry Pi through the GPIO (https://pypi.org/project/RPi.GPIO/)

* It is running on a Gunicorn WSGI server (https://gunicorn.org/). Considering that Flask is only recommended for development purposes, it would not handle a production environment properly.

* Sendgrid API is used to send emails to a specified email every time the plant has been watered. 

## Software Requirements

*  Python 2.7
*  Python PIP (python-pip)


### Installing:
```
    user@host:~$ git https://github.com/imedgar/rpi-watering-system
    user@host:~$ cd rpi-watering-system
    user@host:~/rpi-watering-system$ pip install -r requirements.txt #this sets up python deps in your environment  
```    

## Setting up the rpi-watering-system environment
    
### server.config    

```
    user@host:~/rpi-watering-system$ touch server.config
    user@host:~/rpi-watering-system$ nano server.config
    
    APP_NAME="web_plants"
    HOST="127.0.0.1"
    PORT= 5000
```    
 You can change the host to 0.0.0.0 to public expose the server
 

### Server scripts

Once the server.config has been set, there are 2 scripts to start up or shutdown the server:
* startup.sh
* shutdown.sh

The startup.sh will start the server on the background and save the PID of the process in a file named {app_name}.pid, used after to automatically shutdown the server through the PID process.

### Auto watering

There is a method in water.py used in auto_water.py to water the plant only if the soil moisture sensor detects it's needed.
In order to automatize it we need to add a cron in the crontab:

```
    user@host:~/rpi-watering-system$ crontab -e

    0 */2 * * * cd <your path to web_plants>; sudo python auto_water.py
```

The cron above will be executed every 2h. Although, you can always change its frequency, e.g. (https://crontab.guru/examples.html)


## Acknowledgments

* Thanks to Ben Eagan for his code and idea (https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc)

## Author

* Edgar Rubio (https://github.com/imedgar)

## License

MIT License

Copyright (c) 2019 Edgar Rubio

 
