import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

from src.config import apply_ieee_style
from src.sdt_model import SDT, v_ratio_round

# Setup publication style settings
apply_ieee_style(font_size=10, label_size=10, title_size=10)

def create_contour_plot(ax, df, round_num, manipulation, column_to_plot):
    # Filter the DataFrame for the specified round and manipulation
    filtered_df = df[(df['Round'] == round_num) & (df['Manipulation'] == manipulation)]

    if filtered_df.empty:
        return

    # Extract the relevant data for the contour plot
    x = filtered_df['d_human'].values
    y = filtered_df['d_automation'].values
    z = filtered_df[column_to_plot].values * 100

    # Create a grid for the contour plot
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    X, Y = np.meshgrid(xi, yi)

    # Interpolate the data to create a smooth surface
    Z = griddata((x, y), z, (X, Y), method='cubic')

    cmap = plt.cm.Greys

    if column_to_plot == 'Performance Benefit':
        levels = np.linspace(-50, 30, 17)
    elif column_to_plot == 'Acceptance Rate':
        levels = np.linspace(30, 100, 15)
    elif column_to_plot == 'Responsibility':
        levels = np.linspace(0, 100, 11)
    else:
        levels = 10

    # 1. Plot Filled Contours (The Shading)
    cf = ax.contourf(X, Y, Z, levels=levels, cmap=cmap, alpha=0.7, extend='max')

    # 2. Plot Contour Lines
    c = ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.8)

    # 3. Add Labels to the Lines
    ax.clabel(c, inline=True, fontsize=8, fmt='%1.0f')

    # Special handling for Performance Benefit: Make the '0' line thicker if it exists
    if column_to_plot == 'Performance Benefit':
        try:
            c0 = ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=1.5, linestyles='--')
            ax.clabel(c0, inline=True, fontsize=9, fmt='%1.0f')
        except ValueError:
            pass

    ax.set_xlabel("d' Human")
    ax.set_ylabel("d' Automation")

    # Title formatting
    title_text = f'{manipulation}\n{column_to_plot}'
    if round_num > 1:
        title_text = f'Incentive {round_num}\n' + title_text
    else:
        title_text = f'Incentive {round_num}\n' + column_to_plot

    ax.set_title(title_text, fontsize=10)

    # Add a colorbar
    cbar = plt.colorbar(cf, ax=ax)
    cbar.ax.tick_params(labelsize=8)
    cbar.outline.set_linewidth(0.5)

    # Subtle grid just to help orientation, behind the plot
    ax.grid(True, linestyle=':', color='gray', alpha=0.3)


def run_simulation(file_path):
    """
    Runs the SDT parameter sweep and saves/returns the results dataframe.
    """
    print("Calculating simulation results (parameter sweep)...")
    result_columns = ['Round', 'Manipulation', 'd_human', 'd_automation', 
                      'Performance Benefit', 'Acceptance Rate', 'Responsibility']

    manipulations = ['Rightly Consent', 'Wrongly Object', 'Rightly Object', 'Wrongly Consent']
    p = 0.3
    v_ratio_automation = 1
    d = 0.05  # Coarse grid for faster computation
    d_round = 1
    d_humans = np.arange(0.5, 3 + d, d)
    d_automations = np.arange(0.5, 3 + d, d)
    Rounds = np.arange(1, 5 + d_round, d_round)
    v_matrix = {'TP': 1, 'FP': 1, 'TN': 1, 'FN': 1}

    rows = []
    for manipulation in manipulations:
        print(f"Processing condition: {manipulation}")
        for round_val in Rounds:
            v_ratio_alarm, v_ratio_no_alarm = v_ratio_round(round_val, manipulation, v_matrix)
            for d_human in d_humans:
                for d_automation in d_automations:
                    row_result = SDT(d_human, d_automation, v_ratio_alarm, v_ratio_no_alarm, 
                                     round_val, manipulation, p, v_ratio_automation)
                    rows.append(row_result)

    df_results = pd.DataFrame(rows, columns=result_columns)
    df_results.to_json(file_path)
    print(f"Calculation complete. Saved to {file_path}")
    return df_results


if __name__ == '__main__':
    file_path = 'sdt_results.json'

    if os.path.exists(file_path):
        print(f"Loading results from {file_path}")
        df_results = pd.read_json(file_path)
    else:
        df_results = run_simulation(file_path)

    # Cap 'Performance Benefit' values
    df_results['Performance Benefit'] = df_results['Performance Benefit'].apply(lambda x: max(x, -0.49))

    # Define conditions to plot in the 3x3 layout
    columns_to_plot = ['Performance Benefit', 'Acceptance Rate', 'Responsibility']
    conditions = [
        {'round_num': 1, 'manipulation': 'Rightly Consent'},
        {'round_num': 5, 'manipulation': 'Rightly Consent'},
        {'round_num': 5, 'manipulation': 'Rightly Object'}
    ]

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))

    for i, condition in enumerate(conditions):
        for j, column in enumerate(columns_to_plot):
            ax = axes[i, j]
            create_contour_plot(ax, df_results, condition['round_num'], condition['manipulation'], column)

    plt.tight_layout()
    output_filename = 'Contour_IEEE_BW.png'
    plt.savefig(output_filename, dpi=300)
    print(f"Contour plot saved successfully as {output_filename}")
    plt.show()
