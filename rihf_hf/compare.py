import re
from typing import Optional
import typer
from pathlib import Path
import json
from copy import deepcopy
from matplotlib import ticker

import pandas as pd
import matplotlib.pyplot as plt
import scienceplots


app = typer.Typer()
legend_fontsize = 11
axis_fontsize = 12

@app.command()
def generate_plots(csv_file: Path):
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=["GPU type", "#GPU", "Calc type", "Topology"])
    df = df[df["Calc type"].isin(["RIMP2 Gradient", "RIHF + RIMP2 Gradient"])]

    gpu_types = df["GPU type"].unique()
    for gpu_type in gpu_types:
        if (gpu_type != "A100"):
            continue
        gpu_df = df[df["GPU type"] == gpu_type]
        gpu_nums = gpu_df["#GPU"].unique()
        for gpu_num in gpu_nums:
            gpu_num_df = gpu_df[gpu_df["#GPU"] == gpu_num].copy()
            gpu_num_df["Topology"] = gpu_num_df["Topology"].apply(lambda x: 75 * x + 25)

            # gpu_num_df = gpu_num_df.set_index(["Calc type"])

            plt.style.use(["science"])

            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.set_aspect(0.16)
            ax.set_xscale("log")
            ax.set_yscale("log")
            # ax.set_xticks([200, 400, 600, 800])
            ax.xaxis.set_major_locator(ticker.FixedLocator([200, 400, 600, 800]))
            ax.xaxis.set_minor_locator(ticker.FixedLocator([]))
            ax.xaxis.set_major_formatter(
                ticker.FuncFormatter(lambda val, pos: f"{int(val)}")
            )

            secax = ax.secondary_xaxis(
                "top", functions=(lambda x: (x - 25) / 75, lambda x: x * 75 + 25)
            )
            secax.xaxis.set_major_formatter(
                ticker.FuncFormatter(
                    lambda val, pos: f"gly\\textsubscript{{{val:.0f}}}"
                )
            )
            secax.xaxis.set_major_locator(ticker.FixedLocator([2, 4, 6, 8, 10]))
            secax.xaxis.set_minor_locator(ticker.FixedLocator([]))
            ax.tick_params(axis="x", which="both", bottom=True, top=False)
            secax.tick_params(axis="x", which="minor", bottom=False, top=False)

            grouped = gpu_num_df.groupby("Calc type")
            for name, group in grouped:
                ax.plot(
                    group["Topology"],
                    group["Time"],
                    label="HF + RIMP2 Gradient" if name == "RIMP2 Gradient" else name,
                    marker="o" if name == "RIMP2 Gradient" else "^",
                    fillstyle="none",
                    color="#1da563" if name == "RIMP2 Gradient" else "#6396c5",
                )

            for i, row in gpu_num_df.iterrows():
                if (
                    row["Calc type"] == "RIHF + RIMP2 Gradient"
                    and row["Topology"] > 150
                ):
                    speedup = 1 / (
                        row["Time"]
                        / gpu_num_df[
                            (gpu_num_df["Calc type"] == "RIMP2 Gradient")
                            & (gpu_num_df["Topology"] == row["Topology"])
                        ]["Time"].values[0]
                    )
                    ax.text(
                        row["Topology"] * 1.1,
                        row["Time"] * 0.9,
                        f"${{{speedup:.1f}}}\\times$",
                        fontsize=9,
                        ha="left",
                        va="top",
                    )

            ax.set_ylabel("Time (s)", fontsize=axis_fontsize)
            ax.set_xlabel("Number of basis functions", fontsize=axis_fontsize)
            ax.set_xlim(150, 1100)
            ax.legend(fontsize=legend_fontsize)
            ax.tick_params(axis='both', which='major', labelsize=axis_fontsize)
            secax.tick_params(axis='both', which='major', labelsize=axis_fontsize)
            plt.savefig(f"time_{gpu_num}_{gpu_type}.png", dpi=300)
            plt.close()


if __name__ == "__main__":
    app()
