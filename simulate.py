# put simulation code here

import output
import csv

def simulate(filename, turns, discount = .05):
    # read in filename.csv
    # run simulation with those NPVs
    npvs = run(turns, discount)

    # distribute the npvs
    npvs = output.npv_distribute(npvs)

    # write out
    output.output_npv_file(filename, npvs)