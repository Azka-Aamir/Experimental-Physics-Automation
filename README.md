# Automated Instrumentation & Experimental Signal Acquisition

An automated data acquisition (DAQ) framework built to simulate real-time laboratory instrument telemetry. This pipeline interfaces virtually with sensor nodes to capture transient voltage profiles, apply signal processing filters, and output academic-grade data visualizations without requiring physical hardware connections.

## Core Implementations
* **Virtual Instrument Control:** Employs `PyVISA-sim` to mimic IEEE 488.2 protocol compliance for virtual instrument addressing.
* **Telemetry Emulation:** Simulates a decaying physical wave profile embedded with stochastic laboratory background noise.
* **Data Processing & Visualization:** Utilizes NumPy matrix structures for real-time array tracking and Matplotlib for automated graphing.

## Core Packages Required
* `pyvisa`
* `pyvisa-sim`
* `numpy`
* `matplotlib`

## Academic Application
This methodology is optimized for deployment in experimental frameworks—such as thin-film transient response testing, laser spectroscopy tracking, or cryogenic sensor logs—where manual data logging is inefficient.

