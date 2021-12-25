import pyfirmata
import pandas as pd
import datetime
import time

board = pyfirmata.Arduino('COM3')  # Set the connection with the Arduino board
temp_sensor = board.get_pin('a:0:i')  # Set pin 0 as a analog input
heartRate_sensor = board.get_pin('a:1:i')  # Set pin 1 as a analog input
data = pd.DataFrame(columns=['Date', 'Temperature', 'Heart Rate'])


# Count the number of beats in 15 seconds, and multiply by four. That's your heart rate.
def resting_heartRate(x):
    print(x)


it = pyfirmata.util.Iterator(board)  # Assigns an iterator used to read the status of the inputs
it.start()  # starts iterator, which keeps a loop running in parallel with your main code

while True:
    try:
        temp_sensor_value = temp_sensor.read()
        voltage = temp_sensor_value * 5
        temperature = (voltage - 0.5) * 100

        heartRate_sensor_value = heartRate_sensor.read()
        heartRate = 0
    except TypeError:
        temperature = 0

    datetime_object = str(datetime.datetime.now().replace(second=0, microsecond=0))
    data = data.append({'Date': datetime_object, 'Temperature': temperature, 'Heart Rate': heartRate}, ignore_index=True)

    time.sleep(60)

# Add notification to phone app
# The American Heart Association notes that a normal resting heart rate ranges from 60 to 100 beats
# per minute (bpm) for adults. Medical experts also agree that a lower resting heart rate can indicate more efficient
# heart function and cardiovascular fitness, as highly conditioned athletes typically have a resting heart rate of 40
# to 60 bpm.
# Body temperature is an independent determinant of heart rate, causing an increase of approximately 10 beats per minute
# per degree centigrade. Body temperature is also an independent determinant of respiratory rate. This quantification
# may help in the assessment of the hot and unwell child, to determine whether any tachycardia or tachypnoea is caused
# solely by fever, or whether there may be an element of concurrent shock.