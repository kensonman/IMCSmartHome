# -*- coding: utf-8 -*-
import RPi.GPIO as gpio


pin_power=3
pin_light=5

# Setup
gpio.setmode(gpio.BOARD)
gpio.setup(pin_power, gpio.OUT)
gpio.setup(pin_light, gpio.OUT)
gpio.output(pin_power, gpio.HIGH)
gpio.output(pin_light, gpio.LOW)
