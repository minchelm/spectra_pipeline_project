import matplotlib.pyplot as plt

# dictionary of lab reference spectra minerals and their classifications
mineral_dictionary = {
    "SAPONITE": "Clays",
    "SMECTITE": "Clays",
    "NONTRONITE": "Clays",
    "SERPENTINE": "Clays",
    "MONTMORILLONITE": "Clays",
    "KAOLINITE": "Clays",
    "GYPSUM": "Sulfates",
    "JAROSITE": "Sulfates",
    "KIESERITE": "Sulfates",
    "SZOMOLNOKITE": "Sulfates",
    "CALCITE": "Carbonates",
    "MAGNESITE": "Carbonates",
    "PYROXENE": "Silicates",
    "PLAGIOCLASE": "Silicates",
    "QUARTZ": "Silicates",
    "FAYALITE": "Silicates",
    "FORSTERITE": "Silicates",
    "OLIVINE": "Silicates",
    "HEMATITE": "Oxides",
    "GOETHITE": "Oxides",
}
# list of classifications
identities = []
for mineral in mineral_dictionary:
    identities.append(mineral_dictionary[mineral])
identities = list(set(identities))


def pipeline_plotting(df_lab, df_crism, df_ratio):
    plotting(df_lab, df_crism, df_ratio)
    plt.show()


def plotting(df_lab, df_crism, df_ratio):
    figures = []
    for column in df_crism:
        y_max = 0
        y_min = 100
        if column != "Wavelength":
            fig, axes = plt.subplots(
                nrows=6, ncols=1, figsize=(8, 6), sharex=True
            )
            fig.suptitle("CRISM + CRISM Ratioed by 10, CRISM #" + column)

            if column != "Wavelength":
                axes[0].plot(
                    df_crism["Wavelength"], df_crism[column], "k", label=column
                )
                axes[0].plot(
                    df_ratio["Wavelength"],
                    df_ratio[column],
                    "k:",
                    label=column + " ratioed",
                )
                if max(df_crism[column]) > y_max:
                    y_max = max(df_crism[column])
                if min(df_crism[column]) < y_min:
                    y_min = min(df_crism[column])
                if max(df_ratio[column]) > y_max:
                    y_max = max(df_ratio[column])
                if min(df_ratio[column]) < y_min:
                    y_min = min(df_ratio[column])
                axes[0].set_ylim(y_min * 0.999, y_max * 1.001)
            axes_idx = 1
            mineral_idx = 1
            offset = 0

            for identity in identities:
                y_max = 0
                y_min = 100
                for column in df_lab.columns:
                    if column == "Wavelength":
                        continue
                    mineral_type = mineral_dictionary[column]
                    if mineral_type == identity:
                        color = plt.cm.viridis(
                            mineral_idx / (len(mineral_dictionary) - 1)
                        )
                        axes[axes_idx].plot(
                            df_lab["Wavelength"],
                            df_lab[column] + offset,
                            color=color,
                            label=column,
                        )
                        if max(df_lab[column] + offset) > y_max:
                            y_max = max(df_lab[column] + offset)
                        if min(df_lab[column] + offset) < y_min:
                            y_min = min(df_lab[column] + offset)
                        if max(df_lab[column] + offset) > y_max:
                            y_max = max(df_lab[column] + offset)
                        if min(df_lab[column] + offset) < y_min:
                            y_min = min(df_lab[column] + offset)
                        offset -= df_lab[column] * 0.01
                        mineral_idx += 1
                axes[axes_idx].set_ylim(y_min * 0.99, y_max * 1.01)
                axes_idx += 1
            for ax in axes:
                ax.legend(loc="upper right", fontsize=4)
                ax.set_xlim(
                    min(df_crism["Wavelength"]), max(df_crism["Wavelength"])
                )
            plt.ylabel("Reflectance")
            plt.xlabel("Wavelength (um)")
            figures.append(fig)
    return figures
