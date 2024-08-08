from accoladeClass import Acco
import pandas as pd


def accoladecsv_init(path=r'C:/Users/Asus/Documents/GitHub/mjc/mjc-py/tw_accolades_info.csv') -> list:
    # Initialises the accolade information and loads them onto an output list
    # Using path as a way to point which file to go to
    # Default is taiwan scoring
    # Source of everything
    score_df = pd.read_csv(path)
    # print(score_df.head())

    # Initialising empty list for output
    accolades = [0] * len(score_df)

    for i in range(len(score_df)):
        acc_name = score_df['acco_name'][i]  # extracting accolade name
        acc_pts = score_df['points'][i]  # Extracting points of said accolade
        acc_double = bool(score_df['double_on_conceal'][i])

        # Initialising class object
        accolades[i] = Acco(acc_name, acc_pts, acc_double)

    return accolades

if __name__ == '__main__':
    vlist = accoladecsv_init()
    print(vlist[27].acco_name)

