import csv

def output_cap_file(filename, caps):
    with open('csv/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                'name',                
                'no_monopoly',
                'one_from_monopoly',
                'two_from_monopoly',
                'three_from_monopoly',
                'two_from_monopoly_me',
                'one_from_monopoly_me',
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
                'no_monopoly': values[0],
                'one_from_monopoly': values[1],
                'two_from_monopoly': values[2],
                'three_from_monopoly': values[3],
                'two_from_monopoly_me': values[4],
                'one_from_monopoly_me': values[5],
                'one_building': values[6],
                'two_building': values[7],
                'three_building': values[8],
                'four_building': values[9],
                'five_building': values[10]
            })
