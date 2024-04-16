import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import ticker
import pandas as pd
import os
from pathlib import Path
import numpy as np
import scienceplots
plt.style.use(["science"])
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'\usepackage{relsize}'

weak_scaling_front = pd.DataFrame(pd.read_csv("weak_scaling_front.csv"))

nodes = pd.Series(weak_scaling_front["nodes"])
times = pd.Series(weak_scaling_front["time"])
flops = pd.Series(weak_scaling_front["PFLOPs"])

fontsize = 7
peak_per_node = 22.3 * 8 / 1000

def plot_weak_scaling(flops, nodes, label, marker, text_offset, color, strong=True):
    ax.plot(
        nodes, flops, label=label, marker=marker, fillstyle="none", color=color
    )
    for i in range(len(nodes)):
      ax.annotate(
          f"{round(flops[i]/(nodes[i]*peak_per_node)*100)}\\%",
          xy=(nodes[i], flops[i]),
          xytext=text_offset,
          textcoords="offset pixels",
          color=color,
          fontsize=fontsize,
      )

fig, ax = plt.subplots()
ax.set_aspect(0.51)
ax.set_xscale("log", base=2)
ax.set_yscale("log", base=2)
min_nodes = 350
max_nodes = 6000
plot_weak_scaling(flops, nodes, "Frontier $(C H_4 N_2 O)_{4n}$", "^", (20, -30), '#6396c5', strong=False)
ax.plot([min_nodes, max_nodes], [flops[0]*min_nodes/nodes[0], flops[0]*max_nodes/nodes[0]], label="Ideal", linestyle="dashdot", color="grey")
ax.plot([min_nodes, max_nodes], [peak_per_node * min_nodes, peak_per_node * max_nodes], label="Peak", linestyle="--", color='#1da563')
ax.legend(fontsize=fontsize)
ax.set_xlabel("Number of Nodes", fontsize=fontsize)
ax.set_ylabel("PFLOP/s", fontsize=fontsize)
ax.set_xlim(min_nodes, max_nodes)
ax.set_ylim(40, 1000)
all_ps = nodes.values.tolist()
ax.set_xticks(all_ps)
ax.set_xticklabels([str(i) for i in all_ps], fontsize=fontsize)
ax.set_yticks([50, 100, 200, 400, 800])
ax.set_yticklabels(["50", "100", "200", "400", "800"], fontsize=fontsize)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
secax = ax.secondary_xaxis("top")
secax.xaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda val, pos: f"{val*4}"
    )
)
secax.xaxis.set_major_locator(ticker.FixedLocator(all_ps))
secax.xaxis.set_minor_locator(ticker.FixedLocator([]))
secax.set_xlabel("Number of GPUs", fontsize=fontsize)
secax.tick_params(axis='x', which='major', labelsize=fontsize)
plt.savefig("weak_scaling.png", dpi=300)
plt.clf()
