"""This python script takes in the data from the full game simulation and plots
the proportion of the games ended against the number fo appearance of the tile in the game's public domain
So for instance for tile 45, it plots the values of proportion of games ended on tile 45 on its 1st appearance
2nd appearance, 3rd appearance, 4th appearance etc. against 1 2 3 4"""

from matplotlib import pyplot as plt
import pandas as pd
import scipy
import numpy as np

tileData = pd.read_csv('./tile_winners_data.csv')
print(tileData.head())


def exp_decay(x, k, A):
    return A * np.exp(-1*k*x)

fitted_vars = {}

fig = plt.figure(figsize=(12,8))

for q in tileData:
    # Initialise the data for each tile
    x_values = np.array([1, 2, 3, 4])
    y_values = np.array(tileData[q])

    # Fitting to an exponential decay curve
    fitted_params = scipy.optimize.curve_fit(exp_decay, x_values, y_values/sum(y_values))
    fitted_k = fitted_params[0][0]
    fitted_A = fitted_params[0][1]

    # Making the numpy curve
    fitted_x = np.linspace(0, 4, 200)
    fitted_y = exp_decay(fitted_x, fitted_k, fitted_A)

    plt.scatter(x_values, y_values / sum(y_values), marker='x')
    plt.plot(fitted_x, fitted_y, c='k', linewidth=0.5)

    plt.xlim((0, 5))
    plt.ylim((0, 5))
    plt.grid(visible=True)


    fitted_vars[q] = (fitted_k, fitted_A)
    #
    # if input() == "quit":
    #     quit()
plt.savefig('fit.png', dpi=600)

op_text = open('exp_dist.txt', 'w')
df = pd.DataFrame(fitted_vars)
op_text.write(df.to_string())
op_text.close()