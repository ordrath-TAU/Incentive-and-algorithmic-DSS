import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from src.config import apply_ieee_style
from src.sdt_model import calculate_optimal_c

# Apply IEEE Standard formatting
apply_ieee_style(font_size=12, label_size=12, title_size=14)

def main():
    d_prime = 1.5
    std_dev = 1.0

    # Means centered around 0
    mu_noise = -d_prime / 2
    mu_signal = d_prime / 2

    # Stage 1 Parameters (The Alert System)
    prior_signal_global = 0.3
    v_ratio_system = 1.0

    # Calculate System Threshold
    c_system = calculate_optimal_c(d_prime, prior_signal_global, v_ratio_system)

    # Calculate System Performance (Hit Rate and False Alarm Rate)
    hit_rate_system = norm.sf(c_system, loc=mu_signal, scale=std_dev)
    fa_rate_system = norm.sf(c_system, loc=mu_noise, scale=std_dev)

    print("--- Stage 1: Alert System ---")
    print(f"Prior P(S): {prior_signal_global}")
    print(f"Optimal Threshold (c): {c_system:.3f}")
    print(f"Hit Rate: {hit_rate_system:.3f}")
    print(f"False Alarm Rate: {fa_rate_system:.3f}\n")

    # Stage 2: Posterior Probabilities
    # Case A: System ALERTS (Yes)
    p_alert = (hit_rate_system * prior_signal_global) + (fa_rate_system * (1 - prior_signal_global))
    p_signal_given_alert = (hit_rate_system * prior_signal_global) / p_alert

    # Case B: System DOES NOT ALERT (No)
    p_no_alert = ((1 - hit_rate_system) * prior_signal_global) + ((1 - fa_rate_system) * (1 - prior_signal_global))
    p_signal_given_no_alert = ((1 - hit_rate_system) * prior_signal_global) / p_no_alert

    print("--- Stage 2: Interaction Updates ---")
    print(f"P(Signal | Alert): {p_signal_given_alert:.3f}")
    print(f"P(Signal | No Alert): {p_signal_given_no_alert:.3f}\n")

    v_ratios_stage2 = [0.3, 1, 3]
    thresholds_given_alert = []
    thresholds_given_no_alert = []

    print("--- Stage 2: New Thresholds ---")
    for v in v_ratios_stage2:
        c_given_alert = calculate_optimal_c(d_prime, p_signal_given_alert, v)
        thresholds_given_alert.append(c_given_alert)
        c_given_no_alert = calculate_optimal_c(d_prime, p_signal_given_no_alert, v)
        thresholds_given_no_alert.append(c_given_no_alert)
        print(f"V-Ratio: {v:<5} | Given Alert (c): {c_given_alert:<6.3f} | Given No Alert (c): {c_given_no_alert:<6.3f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    x = np.linspace(-4, 4, 1000)

    # Plot Distributions
    y_noise = norm.pdf(x, mu_noise, std_dev)
    y_signal = norm.pdf(x, mu_signal, std_dev)

    # Noise: Dashed line, Light Grey Fill
    plt.plot(x, y_noise, label='Noise Dist (N)', color='black', linestyle='--', linewidth=1)
    plt.fill_between(x, y_noise, color='lightgray', alpha=0.5)

    # Signal: Solid line, Darker Grey Fill
    plt.plot(x, y_signal, label='Signal Dist (S)', color='black', linestyle='-', linewidth=1)
    plt.fill_between(x, y_signal, color='gray', alpha=0.3)

    # Plot Stage 1 Threshold (Bold Solid Black)
    plt.axvline(c_system, color='black', linestyle='-', linewidth=2.5,
               label=f'Stage 1 (System): {c_system:.2f}')

    # Linestyles for V-ratios
    linestyles = [':', '--', '-.']

    # Plot Stage 2 Thresholds
    for i, (c, v) in enumerate(zip(thresholds_given_alert, v_ratios_stage2)):
        plt.axvline(c, color='black', linestyle=linestyles[i], linewidth=1.5,
                   label=f'Given Alert (V={v})')

    for i, (c, v) in enumerate(zip(thresholds_given_no_alert, v_ratios_stage2)):
        plt.axvline(c, color='0.4', linestyle=linestyles[i], linewidth=1.5,
                   label=f'Given No Alert (V={v})')

    plt.title(f"SDT Analysis: Interaction Effects (d'={d_prime}), p= 0.3 and v ratio = [0.3,1,3]")
    plt.xlabel("Internal Response")
    plt.ylabel("Probability Density")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
    plt.grid(False)
    plt.axhline(0, color='black', linewidth=0.5)

    output_filename = 'sdt_thresholds_ieee.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\nSDT Thresholds plot saved as {output_filename}")
    plt.show()

if __name__ == "__main__":
    main()
