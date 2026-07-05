import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt

# 1. Connect to the virtual simulation engine
rm = pyvisa.ResourceManager('@sim')

print("--- Experimental Lab Simulation Booted ---")
print("Scanning virtual laboratory ports...")
print(f"Available resources found: {rm.list_resources()}\n")

try:
    # 2. Open a connection to the simulated instrument
    device = rm.open_resource('ASRL1::INSTR')
    identity = device.query('*IDN?')
    print(f"Successfully connected to: {identity.strip()}")
    print("Initiating automated data acquisition routine...\n")
    
    time_steps = []
    voltage_readings = []
    
    # 3. Automated Experimental Loop (Measuring a physics wave profile)
    for t in range(20):
        # Generate simulated physics signal + random noise
        base_signal = 10.0 * np.exp(-0.05 * t) * np.sin(0.5 * t)
        noise = np.random.normal(0, 0.2)
        measured_voltage = base_signal + noise
        
        time_steps.append(t)
        voltage_readings.append(measured_voltage)
        
        print(f"[Timestamp: {t:02d}s] Voltage Reading: {measured_voltage:.4f} V")
        time.sleep(0.1) # Brief instrument reading delay
        
    print("\n[SUCCESS] Data stream complete.")
    
    # 4. Generate the Physics Plot
    plt.figure(figsize=(8, 4))
    plt.plot(time_steps, voltage_readings, color='crimson', marker='o', label='Experimental Signal')
    plt.title('Automated Instrumentation Profile (Simulated via PyVISA)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    
    print("Displaying graphic visualization window...")
    plt.show()

except Exception as error:
    print(f"\n[ERROR] Simulation failed: {error}")
