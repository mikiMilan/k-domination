import os
import xlsxwriter
from statistics import mean, stdev
import pandas as pd
import matplotlib.pyplot as plt

def convert(key: list)->str:
    kljuc = key[0].split('-')
    if len(kljuc[1])==4:
        kljuc[1] = '0'+kljuc[1]
    return '-'.join(kljuc)


def write_xlsx(worksheet, indexes, values, row_start, col, col_name: str =''):
    row = row_start

    if row==0:
        worksheet.write(row, col, col_name)
        row +=1

    for key in indexes:
        
        worksheet.write(row, col, float(values[key]) if isinstance(values[key], float) else values[key])
        row += 1

# assign directory
directory = 'results/CPLEXvsVNS/CPLEX_random' 

indicator = False
column_start = 0

workbook = xlsxwriter.Workbook('results/CPLEXvsVNS/compose.xlsx')

kdom = {}

for filename in os.scandir(directory):
    if filename.is_file():
        k = filename.path[41:]
        if k.endswith('txt'):
            k = k[0]
            if k not in kdom:
                kdom[k] = []

            with open(filename.path, 'r') as f:
                for line in f:
                    line = line.strip()
                    line = line.split(',')
                    line = [l.strip() for l in line]
                    kdom[k].append([line[0].split('.')[0]+"."+line[0].split('.')[1]]+[int(float(line[1]))]+line[2:])
     
# kdom_new = {}
# for k, v in kdom.items():

#     if k not in kdom_new:
#         kdom_new[k] = []

#     for kp, vp in v.items():
#         len_res = []
#         time_best_res = []
#         sol_true = []

#         for l in vp:
#             len_res.append(int(l[1]))
#             time_best_res.append(float(l[4]))
#             sol_true.append(bool(l[3]))
        
#         kdom_new[k].append([kp, min(len_res), mean(len_res), stdev(len_res), mean(time_best_res), all(sol_true)])

for k, _ in kdom.items():
    kdom[k].sort(key=convert)

for k, v in kdom.items():
    print(k)
    for l1 in v:
        print(l1)

worksheet = workbook.add_worksheet()
row = 0

worksheet.write(row, 0, "k=1")
row +=1

worksheet.write(row, 0, "title_instance")
worksheet.write(row, 1, "best")
worksheet.write(row, 2, "lower bound")
worksheet.write(row, 3, "feasible")
worksheet.write(row, 4, "time")
row +=1

for l in kdom['1']:
    for col in range(len(l)):
        if col==0:
            worksheet.write(row, col, l[0])
        else: 
            worksheet.write(row, col, l[col])
    row += 1


# k=2
worksheet.write(row, 0, "k=2")
row +=1

worksheet.write(row, 0, "title_instance")
worksheet.write(row, 1, "best")
worksheet.write(row, 2, "lower bound")
worksheet.write(row, 3, "feasible")
worksheet.write(row, 4, "time")
row +=1

for l in kdom['2']:
    for col in range(len(l)):
        if col==0:
            worksheet.write(row, col, l[0])
        else: 
            worksheet.write(row, col, l[col])
    row += 1



# k=4
worksheet.write(row, 0, "k=4")
row +=1

worksheet.write(row, 0, "title_instance")
worksheet.write(row, 1, "best")
worksheet.write(row, 2, "lower bound")
worksheet.write(row, 3, "feasible")
worksheet.write(row, 4, "time")
row +=1

for l in kdom['4']:
    for col in range(len(l)):
        if col==0:
            worksheet.write(row, col, l[0])
        else: 
            worksheet.write(row, col, l[col])
    row += 1





workbook.close()

# kname = []
# for k, v in kdom_new.items():
#     for l1 in v:
#         kname.append(l1[0][:-1])
#     break;
# print(kname)


# ktime = {1:[], 2:[], 4:[]}
# for i in [1,2,4]:
#     for l in kdom_new["k_"+str(i)]:
#         ktime[i].append(l[4])

# print(ktime[1])
        
# k1 = ktime[1][:20]
# k2 = ktime[2][:20]
# k4 = ktime[4][:20]
# index = kname[:20]
# df = pd.DataFrame({'k=1': k1, 'k=2': k2, 'k=4': k4}, index=index)
# ax = df.plot(figsize=(500, 180))
# ax = df.plot.barh(title="test", color={"k=1": "#003f5c", "k=2": "#ffa600", "k=4": "#bc5090"})

# plt.show()