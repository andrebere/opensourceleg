import numpy as np
import matplotlib.pyplot as plt

folder_path = r'C:\Users\bere2\OneDrive - Fondazione Istituto Italiano Tecnologia\Rehab\Umich\Benchmarking\postprocessing'
print(folder_path + '\\ramp_current_stall_torque.csv')

data = np.genfromtxt(folder_path + '\\ramp_current_stall_torque.csv', delimiter=',', skip_header=1)


time = data[:, 0]      # Time
bool_vals = data[:, 1]
target_current = data[:, 2]   # Target Current
measured_current = data[:, 3]  # Measured Current
position = data[:, 4]  # Position
torque = data[:, 5]    # Torque

plt.figure()
plt.plot(measured_current, -torque, 'b-', linewidth=1.5)
plt.xlabel('Current (mA)')
plt.ylabel('Torque (Nm)')
plt.title('Torque vs Current')
plt.grid(True)

# Perform linear fit
p = np.polyfit(measured_current, -torque, 1)  # p[0] is the slope, p[1] is the intercept

# Display the slope and intercept
slope = p[0] * 100
intercept = p[1]
print(f'Slope: {slope:.2f} Nm/A')
print(f'Intercept: {intercept:.2f} Nm')

# Plot the linear fit line
fit_line = np.polyval(p, measured_current)
plt.plot(measured_current, fit_line, 'r--', linewidth=1.5)  # Plot the fit line
plt.legend(['Measured Data', 'Linear Fit'])
plt.show()

# Plot Measured and Target Current vs Time
plt.figure()
plt.plot(time, measured_current, label='Measured Current')
plt.plot(time, target_current, label='Target Current')
plt.xlabel('Time')
plt.ylabel('Current (mA)')
plt.legend()
plt.show()

print('----------------')