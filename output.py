import csv

def output_cap_file(filename, caps):
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
        for cap in caps:
            name = cap[0]
            values = cap[1]
            writer.writerow({
                'name': name,
                'value0': values[0],
                'value1': values[1],
                'value2': values[2],
                'value3': values[3],
                'value4': values[4],
                'value5': values[5]
            })
