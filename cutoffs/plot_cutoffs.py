import itertools
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import json
import scienceplots

plt.style.use(["science"])
plt.tight_layout()
fig, ax = plt.subplots()
ax.set_aspect(4)
size=5
data = json.load(open("cutoffs_output.json"))

dimer_dists = {}

dists = []
energies = []
for dimer in data["qmmbe"]["nmers"][1]:
    dimer_dist = dimer["fragment_distance"]
    fragments = dimer["fragments"]
    frag_tuple = tuple(fragments)
    dimer_dists[frag_tuple] = dimer_dist
    dists.append(dimer_dist)
    energies.append(
        (
            dimer["delta_hf_energy"]
            + dimer["delta_mp2_os_correction"]
            + dimer["delta_mp2_ss_correction"]
        )
        * 2625.5
    )

ax.scatter(dists, energies, marker="x", s=size, alpha=0.5, color='#6396c5')
dimer_legend = ax.scatter([], [], marker="x", s=size, label="Dimer", color='#6396c5')

dists = []
energies = []
for trimer in data["qmmbe"]["nmers"][2]:
    trimer_dist = 100000
    for pair in itertools.combinations(trimer["fragments"], 2):
        trimer_dist = min(trimer_dist, dimer_dists[pair])
    dists.append(trimer_dist)
    energies.append(
        (
            trimer["delta_hf_energy"]
            + trimer["delta_mp2_os_correction"]
            + trimer["delta_mp2_ss_correction"]
        )
        * 2625.5
    )
legend_fontsize = 6
axis_fontsize = 7
ax.scatter(dists, energies, color='#1da563', marker=".", s=size, alpha=0.3)
trimer_legend = ax.scatter([], [], color='#1da563', marker=".", s=size, label="Trimer")

ax.set_xlabel("Distance (Å)", fontsize=axis_fontsize)
ax.set_ylabel("$\\Delta E$ (kJ/mol)", fontsize=axis_fontsize)
ax.set_ylim(-3.3, 1.30)
ax.set_xlim(2, 30)
ax.tick_params(axis='both', which='major', labelsize=axis_fontsize)


dimers = ax.axvspan(xmin=9, xmax=22, color='#6396c5', alpha=0.1, label='Dimer cutoff')
trimers = ax.axvspan(xmin=0, xmax=9, color='#1da563', alpha=0.1, label='Trimer cutoff')
ax.axvline(22, color='#35638e', linestyle="--", linewidth=0.7)
ax.axvline(9, color='#136d41', linestyle="--", linewidth=0.7)
ax.axhline(0.1, color="black", linestyle="-.", linewidth=0.7, label="0.1 kJ/mol")
ax.axhline(-0.1, color="black", linestyle="-.", linewidth=0.7)

handles, labels = ax.get_legend_handles_labels()
handles.append(trimers)
handles.append(trimer_legend)
handles.append(dimer_legend)

ax.legend(handles, labels)
plt.legend(fontsize=legend_fontsize)
# plt.legend(fontsize=legend_fontsize, loc=(0.65, 0.06))
plt.savefig("dimer_energy_vs_distance.png", dpi=300)
