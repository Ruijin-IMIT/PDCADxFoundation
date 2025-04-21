
import os

input_dir = '/pdcad/inputs'
output_dir = '/pdcad/outputs'


input_cases = os.listdir(input_dir)


for casename in input_cases:
    print(f'Working on {casename}')

    # call your predicting model ...

    # ...

    print(f'Finished {casename}')
    



