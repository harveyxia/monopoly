import csv
import cases

def output_cap_file(filename, caps):
    with open('csv/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                'name',
                'three_from_monopoly',
                'two_from_monopoly',
                'one_from_monopoly',
                'no_monopoly',
                'one_building',
                'two_building',
                'three_building',
                'four_building',
                'five_building',
            ])
        writer.writeheader()
        for cap in caps:
            name = cap[0]
            values = cap[1]
            writer.writerow({
                'name': name,
                'three_from_monopoly': values[0],
                'two_from_monopoly': values[1],
                'one_from_monopoly': values[2],
                'no_monopoly': values[3],
                'one_building': values[4],
                'two_building': values[5],
                'three_building': values[6],
                'four_building': values[7],
                'five_building': values[8]
            })
