import pyfirmata
import time

board = pyfirmata.Arduino('COM3')  # Set the connection with the Arduino board
it = pyfirmata.util.Iterator(board)  # Assigns an iterator used to read the status of the inputs
it.start()  # starts iterator, which keeps a loop running in parallel with your main code

temp_sensor = board.get_pin('a:0:i')  # Set pin 0 as a analog input
motor = board.get_pin('d:9:o')  # Define pin 9 as a digital output

baseline_temp = 17  # Set ambient room temperature

while True:
    try:
        sensor_value = temp_sensor.read()
        voltage = sensor_value * 5
        temperature = (voltage - 0.5) * 100
        print('analog_value/Voltage/Temperature: ', sensor_value, '/', voltage, '/', temperature)
    except TypeError:
        temperature = 0

    if temperature > baseline_temp:
        motor.write(1)  # Digital pin 3 is turned on
    else:
        motor.write(0)  # Digital pin 3 is turned off

    time.sleep(10)

# Add heart rate sensor, and detect when change is at risk
# Add notifaction to phone app
# Aim fan at user
