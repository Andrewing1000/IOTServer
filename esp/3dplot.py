import struct
import serial  # pySerial library
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Serial port configuration
SERIAL_PORT = "COM3"  # Replace with the actual port name (e.g., /dev/ttyUSB0 on Linux)
BAUD_RATE = 100000    # Must match the ESP32's UART baud rate
BYTES_PER_PACKET = 40 # 10 floats x 4 bytes each

# Create a serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Data storage for plotting
data_buffer = {
    "acc_x": [],
    "acc_y": [],
    "acc_z": [],
    "gyro_x": [],
    "gyro_y": [],
    "gyro_z": [],
    "mag_x": [],
    "mag_y": [],
    "mag_z": [],
    "temp": []
}

# Initialize the plot
fig, ax = plt.subplots(4, 1, figsize=(10, 8))
lines = []

# Define labels and plot initialization
labels = [
    "Acceleration (x, y, z)",
    "Gyroscope (x, y, z)",
    "Magnetometer (x, y, z)",
    "Temperature"
]

for i, label in enumerate(labels):
    ax[i].set_title(label)
    ax[i].set_xlim(0, 100)  # Display the last 100 points
    ax[i].set_ylim(-10, 10) # Adjust as needed for your sensor data
    if i < 3:  # 3-axis sensors
        lines.extend(ax[i].plot([], [], label="x"))
        lines.extend(ax[i].plot([], [], label="y"))
        lines.extend(ax[i].plot([], [], label="z"))
    else:  # Temperature
        lines.append(ax[i].plot([], [], label="Temp")[0])

plt.tight_layout()
for a in ax:
    a.legend()

# Update function for the live plot
def update(frame):
    if ser.in_waiting >= BYTES_PER_PACKET:
        raw_data = ser.read(BYTES_PER_PACKET)
        try:
            # Unpack the data
            unpacked_data = struct.unpack(">10f", raw_data)

            # Append new data to the buffer
            keys = list(data_buffer.keys())
            for i, key in enumerate(keys):
                data_buffer[key].append(unpacked_data[i])
                # Keep only the last 100 data points
                if len(data_buffer[key]) > 100:
                    data_buffer[key] = data_buffer[key][-100:]

            # Update the plot lines
            for i, line in enumerate(lines):
                key = keys[i // 3] if i < 9 else keys[-1]
                line.set_data(range(len(data_buffer[key])), data_buffer[key])

        except struct.error as e:
            print(f"Struct unpack error: {e}")

    # Adjust plot limits dynamically
    for i, a in enumerate(ax):
        if i < 3:  # 3-axis sensors
            a.set_ylim(min(min(data_buffer["acc_x"]), -10),
                       max(max(data_buffer["gyro_x"]), 10))
        else:  # Temperature
            a.set_ylim(min(data_buffer["temp"]) - 1, max(data_buffer["temp"]) + 1)

    return lines

# Set up the animation
ani = FuncAnimation(fig, update, interval=100)

plt.show()
