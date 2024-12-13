'''
Title: EV Truck Data Scaling
Author: Sameer Bajaj
Date: 12/04/2024
Description: This program allows for full functionality with or without arguments, allowing users to scale data
provided by NREL for larger use cases.
'''

import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
agg_data = []

def agg_plot(end, agg_data, wattage, charge_strats, csv_list, scale_factor):
    fig, ax = plt.subplots(figsize=(4, 3))
    labels = ['Beverage', 'Warehouse', 'Food']
    colors = ['#E77377', '#8dccbe', '#355070']
    if end == 'multiplot':
        for i, file_location in enumerate(csv_list):
            data = pd.read_csv(file_location)
            plt.plot(data['time'], scale_factor*data['avg_power_kw'], label=labels[i], color=colors[i])
        plt.legend(loc = 'upper left', fontsize = 8)
    else:
        if wattage == 'unscaled':
            plt.plot(agg_data['time'], agg_data['avg_power_kw'], color=colors[0])
        else:
            plt.plot(agg_data['time'], agg_data['avg_power_MW'], color=colors[0])
    plt.grid(axis='both', linestyle='--')
    plt.xlim(0, len(agg_data['time']))
    plt.xlabel('Time').set_fontsize(6)
    if wattage == 'unscaled':
        plt.ylabel('Power (kW)').set_fontsize(6)
    else:
        plt.ylabel('Power (MW)').set_fontsize(6)
    ax.set_xticks(np.linspace(0, len(agg_data['time']), 25)[::4])
    ax.set_xticklabels(range(0, 26)[::4], fontsize=8)
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    plot_fp = os.path.join('./', 'figures', f'{wattage}_{''.join(str(i[0]).upper() for i in charge_strats)}_{end}.png')
    plt.savefig(plot_fp, bbox_inches='tight', dpi=300)
    plt.show()

def scalemax(charge_strats = [''], wattage = None):
    csv_list = []
    while charge_strats == ['']:
        charge_strats = list(map(str, input("Enter your charge strategies (\"x1 x2 x3\") \n"
                                            "where each x is in [immediate, delayed, min_power] ").strip().split()))[:3]
    if wattage is None:
        wattage = str(input("What is the max wattage of your system in MW? \n"
                            "Press return to generate unscaled data: "))
    for i in range(len(charge_strats)):
        fp = os.path.join('./',f'fleet{i+1}-100-{charge_strats[i]}.csv')
        csv_list.append(fp)
    agg_data = pd.read_csv(csv_list[0])
    for i in range(2):
        agg_data['avg_power_kw'] += pd.read_csv(csv_list[i+1])['avg_power_kw']
    if wattage != '':
        scale_factor = int(wattage)/agg_data['avg_power_kw'].max()
        agg_data.rename(columns = {'avg_power_kw': 'avg_power_MW'}, inplace = True)
        wattage = str(wattage) + 'MW'
        agg_data['avg_power_MW'] *= scale_factor
    else:
        wattage = 'unscaled'
        scale_factor = 1
    end = 'multiplot'
    for i in range(2):
        agg_plot(end, agg_data, wattage, charge_strats, csv_list, scale_factor)
        end = 'agg_plot'
    save_loc = os.path.join('./', 'agg_data', f'{wattage}_{''.join(str(i[0]).upper() for i in charge_strats)}.csv')
    agg_data.to_csv(save_loc, index=False)
    print("Your scale factor was ", 1000**(wattage != 'unscaled')*scale_factor)

#charge_strats = ['delayed', 'delayed', 'delayed']
#scalemax(charge_strats)
scalemax()
