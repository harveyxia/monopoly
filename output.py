import csv

def npv_distribute(npvs):
    return npvs

def output_npv_file(filename, npvs):
    with open('csv/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                'name',
                'value0',
                'value1',
                'value2',
                'value3',
                'value4',
                'value5'
            ])
        writer.writeheader()
        for npv in npvs:
            name = npv[0]
            values = npv[1]
            writer.writerow({
                'name': name,
                'value0': values[0],
                'value1': values[0],
                'value2': values[0],
                'value3': values[0],
                'value4': values[0],
                'value5': values[0]
            })
