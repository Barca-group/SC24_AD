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

strong_scaling_perl = pd.DataFrame(pd.read_csv("strong_scaling_perl.csv"))
strong_scaling_front = pd.DataFrame(pd.read_csv("strong_scaling_front.csv"))
strong_scaling_front_big = pd.DataFrame(pd.read_csv("strong_scaling_front_34000.csv"))

perl_nodes = pd.Series(strong_scaling_perl["nodes"])
perl_times = pd.Series(strong_scaling_perl["time"])
front_nodes = pd.Series(strong_scaling_front["nodes"])
front_times = pd.Series(strong_scaling_front["time"])
front_big_nodes = pd.Series(strong_scaling_front_big["nodes"])
front_big_times = pd.Series(strong_scaling_front_big["time"])


def speedup(times, ps):
    return [
        times[0] / times[i] * ps[0]
        for i in range(len(times))
    ]

def plot_speedup(times, nodes, label, marker, text_offset, color):
    speedups = speedup(times, nodes)
    ax.plot(
        nodes, speedups, label=label, marker=marker, fillstyle="none", color=color
    )
    if not (type(text_offset) is list):
        text_offset = [text_offset] * len(nodes)

    for i in range(1, len(nodes)):
      ax.annotate(
          f"{round(speedups[i]/nodes[i]*100)}\\%",
          xy=(nodes[i], speedups[i]),
          xytext=text_offset[i-1],
          textcoords="offset pixels",
          color=color,
          fontsize=6,
      )


max_nodes = 18000
min_nodes = 30
fontsize = 7

fig, ax = plt.subplots()
ax.set_aspect(0.6)
ax.set_xscale("log", base=2)
ax.set_yscale("log", base=2)
plot_speedup(perl_times, perl_nodes, "Perlmutter $\\mathrm{\\mathsmaller{(C_8 H_9 N O_2)_{160}}}$", "o", (20, -30), '#1da563')
plot_speedup(front_times, front_nodes, "Frontier $\\mathrm{\\mathsmaller{(C H_4 N_2 O)_{24000}}}$", "^", (-70, 10), '#6396c5')
plot_speedup(front_big_times, front_big_nodes, "Frontier $\\mathrm{\\mathsmaller{(C H_4 N_2 O)_{34000}}}$", "x", [(-40, 30), (10, -35)], '#de4343')
ax.plot([min_nodes, max_nodes], [min_nodes, max_nodes], label="Ideal", linestyle="dashdot", color="grey")
ax.legend(fontsize=fontsize)

ax.set_xlabel("Number of Nodes", fontsize=fontsize)
ax.set_ylabel("Strong speedup", fontsize=fontsize)
ax.set_xlim(min_nodes, max_nodes)
ax.set_ylim(min_nodes, max_nodes)
all_ps = [2**i for i in range(6, 13)]
all_ps.append(9400)
p_labels = [str(i) for i in all_ps]
ax.set_xticks(all_ps)
ax.set_xticklabels(p_labels, fontsize=fontsize)
ax.set_yticks(all_ps)
ax.set_yticklabels(p_labels, fontsize=fontsize)
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
plt.savefig("strong_scaling.png", dpi=300)
plt.clf()