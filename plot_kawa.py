import numpy as np
import matplotlib.pyplot as plt

energy = np.load("energy.npy")
heat_cap = np.load("heat_cap.npy")
mag = np.load("mag.npy")
susc = np.load("susc.npy")
T = np.load("temp.npy")
c_err = np.load("c_err.npy")

f1 = plt.figure()
plt.title("Average Energy vs Temperature")
plt.xlabel("Temperature (K)")
plt.ylabel("Energy")
plt.plot(T, energy, marker = "x", mec="black")
plt.grid()
plt.savefig("E.png")

f1 = plt.figure()
plt.title("Heat Capacity vs Temperature")
plt.xlabel("Temperature (K)")
plt.ylabel("Energy")
plt.errorbar(T, heat_cap, yerr = c_err, marker = "x", mec = "black", ecolor = "black")
plt.grid()
plt.text(1, 4, f"Critical Temp = {round(T[np.argmax(heat_cap)], 2)} K")
plt.savefig("heat_cap_err.png")

f1 = plt.figure()
plt.plot(T, heat_cap, marker = "x", mec = "black")
plt.xlabel("Temperature (K)")
plt.ylabel("Heat Capacity")
plt.title("Heat Capacity vs Temperature")
plt.grid()
plt.text(1, 1, f"Critical Temp = {round(T[np.argmax(heat_cap)], 2)} K")
plt.savefig("heat_cap.png")



