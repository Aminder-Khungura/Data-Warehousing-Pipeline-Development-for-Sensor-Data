import MySQLdb
import xlrd

excel = xlrd.open_workbook("data.xlsx")
sheet = excel.sheet_by_index(0)

database = MySQLdb.connect(host="localhost", user="root", passwd="", db="table")
cursor = database.cursor()

query = """INSERT INTO Sensor_DB (Date, Temperature, HeartRate) VALUES (%s, %s, %s)"""

for r in range(1, sheet.nrows):
    Date = sheet.cell(r, 0).value
    Temperature = sheet.cell(r, 1).value
    HeartRate = sheet.cell(r, 2).value
    values = (Date, Temperature, HeartRate)
    cursor.execute(query, values)

cursor.close();
database.commit()
database.close()
print('UPLOAD COMPLETE')