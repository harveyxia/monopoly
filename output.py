import csv

def npv_distribute(npvs):
    return npvs

def output_npv_file(filename, npvs):
    with open('csv/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'value'])
        writer.writeheader()
        for npv in npvs:
            for r in npv:
                writer.writerow({'name': r[0], 'value': r[2]})
