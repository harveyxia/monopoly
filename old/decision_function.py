import csv


def generate_square_buy_decisions(npv_filename):
    npv = {}
    with open("csv/" + npv_filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            npv[row['name']] = row['value']
    return stupid_function(npv)


# replace this with a more logical function
def stupid_function(npv):
    l = list(npv)
    sorted(l, key=lambda x: npv[x])
    return {l[i]: float(i + 1) / len(l) for i in xrange(len(l))}
