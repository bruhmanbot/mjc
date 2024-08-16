# Reads the csv file and outputs to json with alignment to index
import shutil
import pandas as pd

def csv_to_json(csv_path, output_path='csv2json_output.json', orientation=None):
    df = pd.read_csv(csv_path)
    df.to_json(path_or_buf=output_path, orient=orientation)

csv_to_json('tw_accolades_info.csv', output_path='tw_accolades_info.json', orientation='index')
print('json file updated!')
# Copy output json file to js-ver
shutil.move('tw_accolades_info.json', './js-ver/tw_accolades_info.json')
print('moved to ./js-ver directory')