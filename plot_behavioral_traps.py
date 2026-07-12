import numpy as np
import matplotlib.pyplot as plt
from src.config import apply_ieee_style

# Apply IEEE Standard formatting
apply_ieee_style(font_size=10, label_size=11, title_size=12)

def main():
    # Point A: Consent Trap (qH > qA, V > PR)
    qA_A = 0.65; qH_A = 39/46; v_A = 3.5
    # Point B: Rational Consent (qH > qA, V < PR)
    qA_B = 0.65; qH_B = 65/79; v_B = 1.5
    # Point C: Override Trap (qA > qH, V > PR)
    qA_C = 0.80; qH_C = 8/13; v_C = 3.5
    # Point D: Rational Override (qA > qH, V < PR)
    qA_D = 0.80; qH_D = 4/7; v_D = 1.5

    points = {
        'A': {'qA': qA_A, 'qH': qH_A, 'V': v_A, 'marker': 'o', 'label': 'A (Consent Shift)'},
        'B': {'qA': qA_B, 'qH': qH_B, 'V': v_B, 'marker': 's', 'label': 'B (Stable)'},
        'C': {'qA': qA_C, 'qH': qH_C, 'V': v_C, 'marker': '^', 'label': 'C (Override Shift)'},
        'D': {'qA': qA_D, 'qH': qH_D, 'V': v_D, 'marker': 'D', 'label': 'D (Stable)'}
    }

    for k, pt in points.items():
        oA = pt['qA'] / (1 - pt['qA'])
        oH = pt['qH'] / (1 - pt['qH'])
        pt['oA'] = oA
        pt['oH'] = oH
        pt['PR'] = (oH / oA) if pt['qH'] > pt['qA'] else (oA / oH)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # Style variables for greyscale
    color_trap = '#d9d9d9'
    color_rational = '#f2f2f2'
    line_bound = 'black'

    # Graph 1: Specific Boundary (Consent Trap)
    ax = axs[0, 0]
    qA_fixed = 0.65
    x_vals = np.linspace(0.501, 0.99, 500)
    y_vals = (x_vals / (1 - x_vals)) / (qA_fixed / (1 - qA_fixed))

    ax.plot(x_vals, y_vals, color=line_bound, linestyle='-', label=r'Boundary $V = O_H / O_A$')
    ax.axvline(x=qA_fixed, color='dimgrey', linestyle='--', label=f'Baseline $q_A = {qA_fixed}$')

    ax.fill_between(x_vals, y_vals, 6, where=(x_vals > qA_fixed), color=color_trap, hatch='//', alpha=0.5)
    ax.fill_between(x_vals, 0, y_vals, where=(x_vals > qA_fixed), color=color_rational, alpha=0.5)
    ax.fill_between(x_vals, 0, y_vals, where=(x_vals < qA_fixed), color=color_trap, hatch='\\\\', alpha=0.5)
    ax.fill_between(x_vals, y_vals, 6, where=(x_vals < qA_fixed), color=color_rational, alpha=0.5)

    ax.plot(points['A']['qH'], points['A']['V'], marker=points['A']['marker'], color='black', markerfacecolor='grey', label=points['A']['label'])
    ax.plot(points['B']['qH'], points['B']['V'], marker=points['B']['marker'], color='black', markerfacecolor='white', label=points['B']['label'])
    ax.annotate('A', (points['A']['qH']+0.01, points['A']['V']))
    ax.annotate('B', (points['B']['qH']+0.01, points['B']['V']))

    ax.set_xlim(0.65, 1.0)
    ax.set_ylim(0, 6)
    ax.set_xlabel(r'Human Accuracy ($q_H$)')
    ax.set_ylabel(r'Incentive Value ($V$)')
    ax.set_title('Consent Shift Boundary')
    ax.legend(loc='upper right')

    # Graph 2: Specific Boundary (Override Trap)
    ax = axs[0, 1]
    qA_fixed = 0.80
    x_vals = np.linspace(0.501, 0.99, 500)
    y_vals = (qA_fixed / (1 - qA_fixed)) / (x_vals / (1 - x_vals))

    ax.plot(x_vals, y_vals, color=line_bound, linestyle='-', label=r'Boundary $V = O_A / O_H$')
    ax.axvline(x=qA_fixed, color='dimgrey', linestyle='--', label=f'Baseline $q_A = {qA_fixed}$')

    ax.fill_between(x_vals, y_vals, 6, where=(x_vals < qA_fixed), color=color_trap, hatch='//', alpha=0.5)
    ax.fill_between(x_vals, 0, y_vals, where=(x_vals < qA_fixed), color=color_rational, alpha=0.5)
    ax.fill_between(x_vals, 0, y_vals, where=(x_vals > qA_fixed), color=color_trap, hatch='\\\\', alpha=0.5)
    ax.fill_between(x_vals, y_vals, 6, where=(x_vals > qA_fixed), color=color_rational, alpha=0.5)

    ax.plot(points['C']['qH'], points['C']['V'], marker=points['C']['marker'], color='black', markerfacecolor='grey', label=points['C']['label'])
    ax.plot(points['D']['qH'], points['D']['V'], marker=points['D']['marker'], color='black', markerfacecolor='white', label=points['D']['label'])
    ax.annotate('C', (points['C']['qH']+0.01, points['C']['V']))
    ax.annotate('D', (points['D']['qH']+0.01, points['D']['V']))

    ax.set_xlim(0.5, 0.8)
    ax.set_ylim(0, 6)
    ax.set_xlabel(r'Human Accuracy ($q_H$)')
    ax.set_ylabel(r'Incentive Value ($V$)')
    ax.set_title('Override Shift Boundary')
    ax.legend(loc='upper right')

    # Graph 3: Universal Phase Space
    ax = axs[1, 0]
    x_vals = np.linspace(0, 5, 100)
    ax.plot(x_vals, x_vals, color='black', linestyle='-.', label='Boundary Y = X')

    ax.fill_between(x_vals, x_vals, 5, color=color_trap, hatch='//', alpha=0.5)
    ax.fill_between(x_vals, 0, x_vals, color=color_rational, alpha=0.5)

    for k, pt in points.items():
        facecolor = 'grey' if pt['V'] > pt['PR'] else 'white'
        ax.plot(pt['PR'], pt['V'], marker=pt['marker'], color='black', markerfacecolor=facecolor, label=pt['label'])
        ax.annotate(k, (pt['PR']+0.1, pt['V']-0.1))

    ax.text(2, 4, 'Shifted Action', fontsize=11, fontweight='bold', ha='center')
    ax.text(4, 2, 'Stable Action', fontsize=11, fontweight='bold', ha='center')

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xlabel(r'Performance Ratio ($O_{superior} / O_{inferior}$)')
    ax.set_ylabel(r'Incentive Value ($V$)')
    ax.set_title('Universal Phase Space')
    ax.legend(loc='upper right')

    # Graph 4: Sensor Odds Space
    ax = axs[1, 1]
    x_vals = np.linspace(0, 10, 100)
    ax.plot(x_vals, x_vals, color='black', linestyle='-', label=r'Equal Performance ($O_H = O_A$)')

    v_lines = [1.5, 3.5]
    linestyles = ['--', ':']

    for v, ls in zip(v_lines, linestyles):
        ax.plot([0, 10/v], [0, 10], color='black', linestyle=ls, label=f'Boundary V={v}')
        ax.plot([0, 10], [0, 10/v], color='black', linestyle=ls)

    for k, pt in points.items():
        facecolor = 'grey' if pt['V'] > pt['PR'] else 'white'
        ax.plot(pt['oA'], pt['oH'], marker=pt['marker'], color='black', markerfacecolor=facecolor, label=pt['label'])
        ax.annotate(k, (pt['oA']+0.2, pt['oH']-0.2))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel(r'Automation Odds ($O_A$)')
    ax.set_ylabel(r'Human Odds ($O_H$)')
    ax.set_title('Sensor Odds Space')

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left')

    plt.tight_layout()
    output_filename = 'academic_behavioral_traps_greyscale.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Behavioral traps plot saved successfully as {output_filename}")
    plt.show()

if __name__ == "__main__":
    main()
