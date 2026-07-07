import numpy as np
import matplotlib.pyplot as plt

def run_detector_simulation(source_energy_kev, distance_cm, total_emitted_gammas=100000):
    """
    Simulates a cylindrical NaI(Tl) detector reacting to variable source energy and distance.
    Matches the framework described in the FLUKA study abstract.
    """
    # 1. GEOMETRY & SOLID ANGLE (Inverse Square Law)
    # As distance increases, fewer gamma rays physically hit the cylindrical detector face
    detector_radius_cm = 3.81  # Standard 3x3 inch NaI detector radius
    
    # Calculate geometric efficiency (fraction of the total sphere covered by the detector)
    # Solid angle approximation: Area of detector / Area of sphere at that distance
    solid_angle_fraction = (np.pi * detector_radius_cm**2) / (4 * np.pi * (distance_cm**2))
    # Cap it at 0.5 (if source is practically touching the face, max 50% go forward)
    solid_angle_fraction = min(solid_angle_fraction, 0.5)
    
    # Number of gammas that actually enter the detector crystal
    gammas_hitting_detector = int(total_emitted_gammas * solid_angle_fraction)
    
    # 2. ENERGY-DEPENDENT CROSS SECTIONS (Physics Trends)
    # Low energy = photoelectric dominates. High energy = compton dominates.
    if source_energy_kev < 200:
        prob_photoelectric = 0.80
        prob_compton = 0.15
    elif source_energy_kev < 700:
        prob_photoelectric = 0.30
        prob_compton = 0.65
    else:
        prob_photoelectric = 0.10
        prob_compton = 0.85
        
    prob_no_interaction = 1.0 - (prob_photoelectric + prob_compton)

    # 3. DISTANCE-DEPENDENT RESOLUTION
    # Abstract finding: "with the increase in distance... the sharpness decreased" (worse resolution)
    # Base resolution + a penalty factor for distance simulating light collection loss/scatter
    base_resolution = 0.07  
    distance_resolution_penalty = 0.002 * distance_cm
    effective_resolution = base_resolution + distance_resolution_penalty

    # 4. MONTE CARLO CORE LOOP
    detected_energies = []
    
    for _ in range(gammas_hitting_detector):
        interaction = np.random.choice(
            ['photoelectric', 'compton', 'miss'], 
            p=[prob_photoelectric, prob_compton, prob_no_interaction]
        )
        
        if interaction == 'photoelectric':
            energy_deposited = source_energy_kev
        elif interaction == 'compton':
            max_compton = source_energy_kev * (2 * (source_energy_kev / 511)) / (1 + 2 * (source_energy_kev / 511))
            energy_deposited = np.random.uniform(0, max_compton)
        else:
            continue

        # Apply the distance-dependent resolution blurring
        sigma = (energy_deposited * effective_resolution) / 2.355
        blurred_energy = np.random.normal(energy_deposited, sigma)
        
        if blurred_energy > 0:
            detected_energies.append(blurred_energy)

    # Calculate Detector Efficiency
    efficiency = (len(detected_energies) / total_emitted_gammas) * 100
    
    return detected_energies, efficiency

# ==========================================
# RUNNING THE COMPARISON STUDY (e.g., 4cm vs 15cm)
# ==========================================
energy_input = 662  # Cs-137 source energy

# Run simulation for a close source (4cm) and a far source (15cm)
energies_4cm, eff_4cm = run_detector_simulation(source_energy_kev=energy_input, distance_cm=4.0)
energies_15cm, eff_15cm = run_detector_simulation(source_energy_kev=energy_input, distance_cm=15.0)

# Print analytical findings to terminal
print(f"--- Simulation Results for {energy_input} keV Source ---")
print(f"Source at 4.0 cm -> Total Efficiency: {eff_4cm:.3f}% | Detected Counts: {len(energies_4cm)}")
print(f"Source at 15.0 cm -> Total Efficiency: {eff_15cm:.3f}% | Detected Counts: {len(energies_15cm)}")

# ==========================================
# PLOTTING AND GRAPH GENERATION
# ==========================================
plt.figure(figsize=(12, 6))

# Plot 4cm data
plt.hist(energies_4cm, bins=150, range=(0, energy_input + 100), 
         color='darkblue', alpha=0.6, label=f'4 cm Distance (Eff: {eff_4cm:.2f}%)')

# Plot 15cm data
plt.hist(energies_15cm, bins=150, range=(0, energy_input + 100), 
         color='crimson', alpha=0.7, label=f'15 cm Distance (Eff: {eff_15cm:.2f}%)')

plt.title("Influence of Source Position on NaI(Tl) Energy Deposition & Spectral Resolution", fontsize=14, fontweight='bold')
plt.xlabel("Energy Deposited (keV)", fontsize=12)
plt.ylabel("Counts / Channel", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)

plt.tight_layout()
plt.show()
