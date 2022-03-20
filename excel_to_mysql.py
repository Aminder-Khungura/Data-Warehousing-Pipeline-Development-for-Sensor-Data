import mysql.connector
import pandas as pd


database = mysql.connector.connect(host='localhost', user='root', password='pass', port='3306', database='sensor_data', auth_plugin='mysql_native_password')
cursor = database.cursor()
data = pd.read_excel(r'C:\Users\amind\PycharmProjects\Data-Warehousing-Pipeline-Development-for-Sensor-Data\data.xlsx')
num_of_rows = data.count(axis='index')[0]


for i in range(num_of_rows):
    Date = (data.iloc[i][0])
    Temperature = (data.iloc[i][1])
    HeartRate = (data.iloc[i][2])
    cursor.execute('''INSERT INTO data (Date, Temperature, HeartRate) VALUES (%s, %s, %s)''', (str(Date), str(Temperature), str(HeartRate)))

cursor.close();
database.commit()
database.close()
print('UPLOAD COMPLETE')