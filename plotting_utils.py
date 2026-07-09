import matplotlib.pyplot as plt
import os
import numpy as np
import folium


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
    """Plottet die Spannungs- und Stromprofile über der Zeit beginnend bei t=0s.
    Das voltage_profile muss mit der Anfangsspannung bei t=0s beginnen, und die nachfolgenden Spannungswerte entsprechen der Spannung, nachdem der Strom für das jeweilige Zeitintervall angelegt wurde.
    Es wird angenommen, dass Spannung und Strom über die gegebenen Zeitintervalle stückweise konstant sind.

    Parameters
    ----------
    voltage_profile : list[float]
        Liste von Spannungswerten in Volt (V) für jedes Intervall, plus die Anfangsspannung bei t=0s.
    current_profile : list[float]
        Liste von Stromwerten in Ampere (A) für jedes Intervall.
    duration_profile : list[float]
        Liste von Dauerwerten in Sekunden (s) für jedes Intervall. Muss die gleiche Länge wie voltage_profile und current_profile haben.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Das Matplotlib-Figure-Objekt, das den Plot von Spannung und Strom über der Zeit enthält.
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
    """Plottet die Spannungs- und Stromprofile über der Zeit beginnend bei t=0s.
    Das voltage_profile muss mit der Anfangsspannung bei t=0s beginnen, und die nachfolgenden Spannungswerte entsprechen der Spannung, nachdem der Strom für das jeweilige Zeitintervall angelegt wurde.
    Es wird angenommen, dass Spannung und Strom über die gegebenen Zeitintervalle stückweise konstant sind.

    Parameters
    ----------
    voltage_profile : list[float]
        Liste von Spannungswerten in Volt (V) für jedes Intervall, plus die Anfangsspannung bei t=0s.
    current_profile : list[float]
        Liste von Stromwerten in Ampere (A) für jedes Intervall.
    duration_profile : list[float]
        Liste von Dauerwerten in Sekunden (s) für jedes Intervall. Muss die gleiche Länge wie voltage_profile und current_profile haben.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Das Matplotlib-Figure-Objekt, das den Plot von Spannung und Strom über der Zeit enthält.
    """

    assert len(voltage_profile) - 1 == len(current_profile) == len(duration_profile), "Voltage profile must be longer by 1 than current and duration profiles to account for the starting voltage at t=0s."
   
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

    output_ordner = os.path.join(hauptordner, "output")
    os.makedirs(output_ordner, exist_ok=True)

    
    zeit_s = (berechnete_daten['time'] - berechnete_daten['time'].iloc[0]).dt.total_seconds()
    zeit_min = zeit_s / 60.0
    
    def add_time_axis(ax):
        # hilfsfunktion fuer zeitachse
        ax_time = ax.twiny()
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
        
        ax_time.set_xlim(ax.get_xlim())
        ax_time.set_xticks(km_ticks)
        ax_time.set_xticklabels(time_labels, fontsize=9, alpha=0.8)
        ax_time.set_xlabel('zeit', fontsize=10, labelpad=10)

    # 1. höhe
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(distanz_km, berechnete_daten['ele'], color='green', linewidth=2, label='höhe (m)')
    ax1.set_ylabel('höhe (m)')
    ax1.set_xlabel('distanz (km)')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    add_time_axis(ax1)
    fig1.tight_layout()
    fig1.savefig(os.path.join(output_ordner, '1_höhenprofil.png'), dpi=300)

    # 2. geschwindigkeit
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(distanz_km, berechnete_daten['v'] * 3.6, color='purple', linewidth=2, label='geschw. (km/h)')
    ax2.set_ylabel('geschw. (km/h)')
    ax2.set_xlabel('distanz (km)')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    add_time_axis(ax2)
    fig2.tight_layout()
    fig2.savefig(os.path.join(output_ordner, '2_geschwindigkeit.png'), dpi=300)

    # 3. leistung
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.plot(distanz_km, berechnete_daten['P_mech'], color='red', linewidth=2, label='leistung (W)')
    ax3.set_ylabel('leistung (W)')
    ax3.set_xlabel('distanz (km)')
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.legend()
    add_time_axis(ax3)
    fig3.tight_layout()
    fig3.savefig(os.path.join(output_ordner, '3_leistung.png'), dpi=300)

    # 4. soc
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    ax4.plot(distanz_km, daten_lipo['akku_soc'] * 100, label='LiPo SoC (%)', color='blue', linewidth=2)
    ax4.plot(distanz_km, daten_nmc['akku_soc'] * 100, label='NMC SoC (%)', color='orange', linewidth=2)
    ax4.set_ylabel('SoC (%)')
    ax4.set_xlabel('distanz (km)')
    ax4.set_ylim(-5, 105)
    ax4.grid(True, linestyle='--', alpha=0.7)
    ax4.legend()
    add_time_axis(ax4)
    fig4.tight_layout()
    fig4.savefig(os.path.join(output_ordner, '4_soc.png'), dpi=300)

    # 5. spannung
    fig5, ax5 = plt.subplots(figsize=(10, 4))
    ax5.plot(distanz_km, daten_lipo['akku_spannung'], label='LiPo (V)', color='blue', linewidth=1.5)
    ax5.plot(distanz_km, daten_nmc['akku_spannung'], label='NMC (V)', color='orange', linewidth=1.5)
    ax5.set_ylabel('spannung (V)')
    ax5.set_xlabel('distanz (km)')
    ax5.grid(True, linestyle='--', alpha=0.7)
    ax5.legend()
    add_time_axis(ax5)
    fig5.tight_layout()
    fig5.savefig(os.path.join(output_ordner, '5_spannung.png'), dpi=300)


    plt.close("all")
    return [fig1, fig2, fig3, fig4, fig5]





def create_route_map(df):

    m = folium.Map(
        location=[df["lat"].mean(), df["lon"].mean()],
        zoom_start=12
    )

    def speed_color(v):
        v = v * 3.6   # m/s -> km/h

        if v < 10:
            return "blue"
        elif v < 20:
            return "cyan"
        elif v < 30:
            return "green"
        elif v < 40:
            return "yellow"
        elif v < 50:
            return "orange"
        else:
            return "red"

    for i in range(len(df)-1):

        p1 = [df.iloc[i]["lat"], df.iloc[i]["lon"]]
        p2 = [df.iloc[i+1]["lat"], df.iloc[i+1]["lon"]]

        folium.PolyLine(
            [p1, p2],
            color=speed_color(df.iloc[i]["v"]),
            weight=6,
            opacity=0.9
        ).add_to(m)

    folium.Marker(
        [df.iloc[0]["lat"], df.iloc[0]["lon"]],
        popup="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        [df.iloc[-1]["lat"], df.iloc[-1]["lon"]],
        popup="Ende",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium.Marker(
        [df.iloc[-1]["lat"], df.iloc[-1]["lon"]],
        popup="Ende",
        icon=folium.Icon(color="red")
    ).add_to(m)

    legend_html = """
    <div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    width: 170px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding:10px;
    ">
    <b>Geschwindigkeit</b><br><br>
    <span style="color:blue;">■</span> 0 - 10 km/h<br>
    <span style="color:cyan;">■</span> 10 - 20 km/h<br>
    <span style="color:green;">■</span> 20 - 30 km/h<br>
    <span style="color:yellow;">■</span> 30 - 40 km/h<br>
    <span style="color:orange;">■</span> 40 - 50 km/h<br>
    <span style="color:red;">■</span> über 50 km/h
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    m.save("route_map.html")

    print("Karte gespeichert als route_map.html")






    

