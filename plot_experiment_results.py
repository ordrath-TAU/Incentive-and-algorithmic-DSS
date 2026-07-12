import numpy as np
import matplotlib.pyplot as plt

from src.config import apply_ieee_style
from src.experimental_data import (
    EXPERIMENTAL_SCORES, EXPERIMENTAL_D_PRIME,
    SUBJECTIVE_USEFULNESS, SUBJECTIVE_SELF_SUCCESS, SUBJECTIVE_AUTOMATION_SUCCESS,
    GROUPS, LEVELS
)

# Apply IEEE Standard formatting
apply_ieee_style(font_size=12, label_size=14, title_size=14)

def plot_scores():
    plt.figure(figsize=(10, 6))
    markers = ['^', 'o', 's']
    linestyles = ['-', '--', ':']

    for i, level in enumerate(LEVELS):
        means = EXPERIMENTAL_SCORES[level]['Mean']
        lower_ci = EXPERIMENTAL_SCORES[level]['Lower CI']
        upper_ci = EXPERIMENTAL_SCORES[level]['Upper CI']

        # Shift x-coordinates
        x_positions = np.arange(len(GROUPS)) + (0.05 + i * 0.15)
        yerr = [means - lower_ci, upper_ci - means]

        plt.errorbar(
            x_positions, means, yerr=yerr, fmt=markers[i], label=level,
            capsize=5, color='black', markeredgecolor='black', markerfacecolor='white',
            markersize=9, elinewidth=1.5
        )

        plt.plot(x_positions, means, color='black', linestyle=linestyles[i], linewidth=1.5, alpha=0.8)

    plt.xlabel('Manipulation')
    plt.ylabel("Scores")
    plt.xticks(np.arange(len(GROUPS)) + 0.2, GROUPS)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.ylim(6, 24)
    plt.legend(title="d`", frameon=True, framealpha=1, edgecolor='black')
    
    output_filename = 'experiment_scores.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Experimental scores plot saved as {output_filename}")
    plt.close()

def plot_d_prime():
    plt.figure(figsize=(10, 6))
    markers = ['^', 'o', 's']
    linestyles = ['-', '--', ':']

    for i, level in enumerate(LEVELS):
        means = EXPERIMENTAL_D_PRIME[level]['Mean']
        lower_ci = EXPERIMENTAL_D_PRIME[level]['Lower CI']
        upper_ci = EXPERIMENTAL_D_PRIME[level]['Upper CI']

        # Shift x-coordinates
        x_positions = np.arange(len(GROUPS)) + (0.05 + i * 0.15)
        yerr = [means - lower_ci, upper_ci - means]

        plt.errorbar(
            x_positions, means, yerr=yerr, fmt=markers[i], label=f"Level {level}",
            capsize=5, color='black', markeredgecolor='black', markerfacecolor='white',
            markersize=9, elinewidth=1.5
        )

        plt.plot(x_positions, means, color='black', linestyle=linestyles[i], linewidth=1.5, alpha=0.8)

    # Plot Reference Lines
    ref_line_style = {'color': 'dimgrey', 'linestyle': '--', 'linewidth': 1.2, 'alpha': 0.7}
    target_values = [0.75, 1.16, 1.9]
    for val in target_values:
        plt.axhline(y=val, **ref_line_style)
        plt.text(x=4.45, y=val + 0.02, s=f"Target: {val}", color='dimgrey', fontsize=10, fontweight='bold', ha='left')

    plt.axhline(y=1.25, color='black', linestyle='-.', linewidth=1.2, alpha=0.8)
    plt.text(x=4.45, y=1.25 + 0.02, s="Human: 1.25", color='black', fontsize=10, fontweight='bold', ha='left')

    plt.xlabel('Manipulation')
    plt.ylabel("Sensitivity ($d'$)")
    plt.xticks(np.arange(len(GROUPS)) + 0.2, GROUPS)
    plt.grid(axis='y', linestyle=':', alpha=0.4)
    plt.ylim(0.7, 2.1)
    plt.legend(title="Automation Level", loc='upper left')

    output_filename = 'experiment_d_prime.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Experimental d-prime plot saved as {output_filename}")
    plt.close()

def plot_subjective_metric(data_dict, ylabel_text, filename):
    plt.figure(figsize=(10, 6))
    markers = ['^', 'o', 's']
    linestyles = ['-', '--', ':']
    manipulations_capitalized = [g.title() for g in GROUPS]

    for i, level in enumerate(LEVELS):
        means = []
        x_positions = []
        lower_ci = []
        upper_ci = []

        for j, manipulation in enumerate(manipulations_capitalized):
            m_data = data_dict[manipulation][level]
            means.append(m_data['Mean'])
            lower_ci.append(m_data['Lower CI'])
            upper_ci.append(m_data['Upper CI'])
            
            offset = (i - 1) * 0.15
            x_positions.append(j + offset)

        means = np.array(means)
        lower_ci = np.array(lower_ci)
        upper_ci = np.array(upper_ci)
        yerr = [means - lower_ci, upper_ci - means]

        plt.errorbar(
            x_positions, means, yerr=yerr, fmt=markers[i], label=level,
            capsize=5, color='black', markeredgecolor='black', markerfacecolor='white',
            markersize=9, elinewidth=1.5
        )

        plt.plot(x_positions, means, color='black', linestyle=linestyles[i], linewidth=1.5, alpha=0.8)

    plt.xlabel('Manipulation')
    plt.ylabel(ylabel_text)
    plt.xticks(np.arange(len(GROUPS)), GROUPS)
    plt.yticks()
    plt.legend(title="Automation Level", loc='upper left', frameon=True, edgecolor='black')
    plt.grid(axis='y', linestyle=':', alpha=0.4)
    
    # Adapt Y-limits slightly for different ranges
    if 'Usefulness' in ylabel_text or 'Self' in ylabel_text:
        plt.ylim(2, 7.5)
    else:
        plt.ylim(4, 8)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Subjective plot saved as {filename}")
    plt.close()

if __name__ == "__main__":
    plot_scores()
    plot_d_prime()
    plot_subjective_metric(SUBJECTIVE_USEFULNESS, "Subjective Scores - Automation Usefulness", "subjective_usefulness.png")
    plot_subjective_metric(SUBJECTIVE_SELF_SUCCESS, "Subjective Scores - Self Success", "subjective_self_success.png")
    plot_subjective_metric(SUBJECTIVE_AUTOMATION_SUCCESS, "Subjective Scores - Automation Success", "subjective_automation_success.png")
    print("All experimental results plots generated successfully!")
