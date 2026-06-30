import matplotlib.pyplot as plt
import os
import numpy as np

def plot_current_profile(current_profile: list[float], duration_profile: list[float]):
    """Plots the current over time profile starting from t=0s. The current is assumed to be piecewise constant over the given duration intervals.

    Parameters
    ----------
    current_profile : list[float]
        List of current values in Amperes (A) for each interval.
    duration_profile : list[float]
        List of duration values in seconds (s) for each interval. Must have the same length as current_profile.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot of current over time.
    """

    assert len(current_profile) == len(duration_profile), "Current and duration profiles must have the same length."

    t_plot, I_plot = [], []
    t_total = 0.0
    for I, d in zip(current_profile, duration_profile):
        t_plot += [t_total, t_total + d]
        I_plot += [I, I]
        t_total += d

    fig, ax = plt.subplots()
    ax.plot(t_plot, I_plot)
    ax.set_xlabel("Time $t$ / s")
    ax.set_ylabel("Current $I$ / A")
    ax.set_yticks(range(-2, 12, 1))
    ax.set_xticks(range(0, int(t_total) + 1, 60))
    ax.grid(True)
    fig.show()

    return fig

def plot_power_profile(power_profile: list[float], duration_profile: list[float]):
    """Plots the power over time profile starting from t=0s. The power is assumed to be piecewise constant over the given duration intervals.

    Parameters
    ----------
    power_profile : list[float]
        List of power values in Watts (W) for each interval.
    duration_profile : list[float]
        List of duration values in seconds (s) for each interval. Must have the same length as power_profile.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot of power over time.
    """

    assert len(power_profile) == len(duration_profile), "Power and duration profiles must have the same length."

    t_plot, P_plot = [], []
    t_total = 0.0
    for P, d in zip(power_profile, duration_profile):
        t_plot += [t_total, t_total + d]
        P_plot += [P, P]
        t_total += d

    fig, ax = plt.subplots()
    ax.plot(t_plot, P_plot)
    ax.set_xlabel("Time $t$ / s")
    ax.set_ylabel("Power $P$ / W")
    ax.set_xticks(range(0, int(t_total) + 1, 60))
    ax.grid(True)
    fig.show()

    return fig


def plot_voltage_profile(voltage_profile: list[float], duration_profile: list[float]):
    """Plots the voltage over time profile starting from t=0s. 
    The voltage_profile must start with the initial voltage at t=0s, and the subsequent voltage values correspond to the voltage after applying the current for the respective duration intervals.
    The voltage is assumed to be piecewise constant over the given duration intervals.

    Parameters
    ----------
    voltage_profile : list[float]
        List of voltage values in Volts (V) for each interval. Plus the initial voltage at t=0s.
    duration_profile : list[float]
        List of duration values in seconds (s) for each interval. Must have the same length as voltage_profile.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot of voltage over time.
    """

    assert len(voltage_profile) - 1 == len(duration_profile), "Voltage profile must be longer by 1 than duration profile and to account for the starting voltage at t=0s."

    t_plot, U_plot = [], []

    t_plot.append(0.0)
    U_plot.append(voltage_profile[0])

    t_total = 0.0
    for U, d in zip(voltage_profile[1:], duration_profile):
        t_plot += [t_total, t_total + d]
        U_plot += [U, U]
        t_total += d

    fig, ax = plt.subplots()
    ax.plot(t_plot, U_plot)
    ax.set_xlabel("Time $t$ / s")
    ax.set_ylabel("Voltage $U$ / V")
    ax.grid(True)
    fig.show()

    return fig

def plot_voltage_and_current_profile(voltage_profile: list[float], current_profile: list[float], duration_profile: list[float]):
    """Plots the voltage and current over time profiles starting from t=0s. 
    The voltage_profile must start with the initial voltage at t=0s, and the subsequent voltage values correspond to the voltage after applying the current for the respective duration intervals.
    The voltage and current are assumed to be piecewise constant over the given duration intervals.

    Parameters
    ----------
    voltage_profile : list[float]
        List of voltage values in Volts (V) for each interval. Plus the initial voltage at t=0s.
    current_profile : list[float]
        List of current values in Amperes (A) for each interval.
    duration_profile : list[float]
        List of duration values in seconds (s) for each interval. Must have the same length as voltage_profile and current_profile.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib figure object containing the plot of voltage and current over time.
    """

    assert len(voltage_profile) - 1 == len(current_profile) == len(duration_profile), "Current and duration profiles must have the same length, and voltage profile must be longer by 1 to account for the starting voltage at t=0s."

    t_plot, U_plot, I_plot = [], [], []

    t_plot.append(0.0)
    U_plot.append(voltage_profile[0])

    t_total = 0.0
    for U, I, d in zip(voltage_profile[1:], current_profile, duration_profile):
        t_plot += [t_total, t_total + d]
        U_plot += [U, U]
        I_plot += [I, I]

        t_total += d

    fig, axV = plt.subplots(figsize=(9, 4.5))
    axI = axV.twinx()

    axV.plot(t_plot[0:], U_plot, "b-", label="Voltage U / V")
    axI.plot(t_plot[1:], I_plot, "r--", label="Current I / A")
    axV.set_xlabel("Time $t$ / s")
    axV.set_ylabel("Voltage $U$ / V", color="b")
    axI.set_ylabel("Current $I$ / A", color="r")
    axV.grid(True)
    
    fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.85))
    fig.show()

    return fig

def plot_simulations_ergebnisse(berechnete_daten, daten_lipo, daten_nmc, hauptordner):
    """
    Generiert ein Diagramm mit drei Subplots bezogen auf die zurückgelegte Distanz (km)
    und zeigt zusätzlich die verstrichene Zeit auf einer oberen Achse an.
    """

    
    distanz_km = berechnete_daten['delta_s'].cumsum() / 1000.0
    
    zeit_s = (berechnete_daten['time'] - berechnete_daten['time'].iloc[0]).dt.total_seconds()
    zeit_min = zeit_s / 60.0
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 11), sharex=True)
    
    # graph 1 hohe
    axs[0].plot(distanz_km, berechnete_daten['ele'], color='green', linewidth=2, label='Höhenprofil (m)')
    axs[0].set_ylabel('Höhe (m)')
    axs[0].grid(True, linestyle='--', alpha=0.7)
    axs[0].legend(loc='upper right')
    axs[0].set_title('E-Bike Simulationsergebnisse: LiPo vs. NMC Akkupack', fontsize=12, fontweight='bold')
    
    # graph 2 SoC
    axs[1].plot(distanz_km, daten_lipo['akku_soc'] * 100, label='LiPo SoC (%)', color='blue', linewidth=2)
    axs[1].plot(distanz_km, daten_nmc['akku_soc'] * 100, label='NMC SoC (%)', color='orange', linewidth=2)
    axs[1].set_ylabel('State of Charge (%)')
    axs[1].set_ylim(-5, 105)
    axs[1].grid(True, linestyle='--', alpha=0.7)
    axs[1].legend(loc='lower left')
    
    # graph 3
    axs[2].plot(distanz_km, daten_lipo['akku_spannung'], label='LiPo Spannung (V)', color='blue', linewidth=1.5)
    axs[2].plot(distanz_km, daten_nmc['akku_spannung'], label='NMC Spannung (V)', color='orange', linewidth=1.5)
    axs[2].set_xlabel('Distanz / km')
    axs[2].set_ylabel('Spannung ($U$) / V')
    axs[2].grid(True, linestyle='--', alpha=0.7)
    axs[2].legend(loc='lower left')
    

    ax_time = axs[0].twiny()
    

    max_km = distanz_km.max()
    km_ticks = np.arange(0, max_km + 1, max(1.0, round(max_km / 6)))
    

    time_labels = []
    for km in km_ticks:

        idx = (distanz_km - km).abs().idxmin()
        t_min = zeit_min.loc[idx]
        if t_min >= 60:
            time_labels.append(f"{int(t_min // 60)}h {int(t_min % 60):02d}m")
        else:
            time_labels.append(f"{int(t_min)} min")
            

    ax_time.set_xlim(axs[0].get_xlim())
    ax_time.set_xticks(km_ticks)
    ax_time.set_xticklabels(time_labels, fontsize=9, alpha=0.8)
    ax_time.set_xlabel('Verstrichene Zeit (Fahrtdauer)', fontsize=10, labelpad=10)
    
    plt.tight_layout()

    plt.show(block=True)
    return fig