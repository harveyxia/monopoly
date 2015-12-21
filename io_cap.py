import csv


# return a caprate data structure from a csv file
def input_cap_file(filename):
    caps = []
    with open('csv/' + filename, 'r') as csvfile:
        reader = csv.DictReader(
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
        for row in reader:
            cap_rates = [
                row['no_monopoly'],
                row['one_from_monopoly'],
                row['two_from_monopoly'],
                row['three_from_monopoly'],
                row['two_from_monopoly_me'],
                row['one_from_monopoly_me'],
                row['one_building'],
                row['two_building'],
                row['three_building'],
                row['four_building'],
                row['five_building'],
            ]
            t = (row['name'], cap_rates)
            caps.append(t)
    return caps


# output a csv file given a caprate data structure
def output_cap_file(filename, caps):
    with open('csv/' + filename, 'w') as csvfile:
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
