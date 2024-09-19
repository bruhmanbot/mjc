import numpy as np
import pandas as pd

data = pd.read_csv('./tile_winners_data.csv')
keys = []
values = []
for i in data:
    if i == 'Grand Total':
        break

    keys.append(int(i))

    values = values + list(data[i])

keys = keys * 4
keys.sort()
print(keys.index(41))

apps = [1,2,3,4] * 34

ln_values = np.log(np.array(values))
ln_values = list(ln_values.astype(float))

ln_values = [round(float(x),3) for x in ln_values]

with open('data-in-arrays.txt', 'w') as file:
    file.write('Keys: ' + str(keys)+ '\n')
    file.close()

with open('data-in-arrays.txt', 'a') as file:
    file.write('Appearances: ' + str(apps) + '\n')
    file.close()

with open('data-in-arrays.txt', 'a') as file:
    file.write('Values: ' + str(values) + '\n')
    file.close()

with open('data-in-arrays.txt', 'a') as file:
    file.write('ln_Values: ' + str(list(ln_values)))
    file.close()