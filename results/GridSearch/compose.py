import os
import xlsxwriter

def convert(key: str)->str:
    key = key.split(',')

    while len(key[0])<3:
        key[0] = '0' + key[0]

    if len(key[1])==2:
        key[1] = key[1] + '.0'
    while len(key[1])<5:
        key[1] = key[1] + '0'

    while len(key[2])<6:
        key[2] = key[2] + '0'

    return ','.join(key)


def write_xlsx(worksheet, indexes, values, row_start, col, col_name: str =''):
    row = row_start

    if row==0:
        worksheet.write(row, col, col_name)
        row +=1

    for key in indexes:
        
        worksheet.write(row, col, float(values[key]) if isinstance(values[key], float) else values[key])
        row += 1

# assign directory
directory = 'results/GS/results' 

indicator = False
column_start = 0

workbook = xlsxwriter.Workbook('results/GS/compose.xlsx')
worksheet = workbook.add_worksheet()

for filename in os.scandir(directory):
    if filename.is_file():

        city = filename.path[19:]
        city = city.split('.')[0]
        
        result = {}
        config = []
        with open(filename.path, 'r') as f:
            for line in f:
                line = line.strip()

                key, value = line.split('),')
                key = key[4:]
                value = value.split(',')[3]

                config.append(key)
                result[key] = value

        if not indicator:
            config.sort(key=convert)
            indexes = [i for i in range(len(config))]
            write_xlsx(worksheet, indexes, config, 1, column_start)
            indicator = True
            column_start += 1
            
        write_xlsx(worksheet, config, result, 0, column_start, city)

        column_start += 1
        print(city, " end")

workbook.close()
        
        