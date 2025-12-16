import matplotlib.pyplot as plot
import pandas as pd

tables_path = "../data/tables/"
graph_path = "../data/graphs/"

chem_data = pd.read_csv(tables_path + "Chemical_Industry.csv")
chem_data = chem_data.apply(pd.to_numeric, errors="coerce")

total_data = pd.read_csv(tables_path + "Total_Industry.csv")
total_data = total_data.apply(pd.to_numeric, errors="coerce")

metallurgy_data = pd.read_csv(tables_path + "Metal_Industry.csv")
metallurgy_data = metallurgy_data.apply(pd.to_numeric, errors="coerce")

def main():
    plot_chem()
    plot_metallurgy()
    plot_chem_and_metallurgy_of_total_pie()
    plot_metals_produced_by_electrolysis_pie()

def plot_chem():
    plot.title("Экспорт химической индустрии")
    plot.xlabel("Год")
    plot.ylabel("Продажи, млн. долларов")
    plot.plot(chem_data["Год"], chem_data["Экспорт_млн_долл"])
    plot.savefig(graph_path + "chem.png")
    plot.clf()

def plot_metallurgy():
    plot.plot(metallurgy_data["Год"], metallurgy_data["Экспорт_млн_долл"])
    plot.title("Экспорт металлургической индустрии")
    plot.xlabel("Год")
    plot.ylabel("Продажи, млн. долларов")
    plot.figtext(0.5, 0.1, "", ha="center")
    plot.savefig(graph_path + "metallurgy.png")
    plot.clf()

def plot_chem_and_metallurgy_of_total_pie():
    chem = chem_data.loc[chem_data["Год"] == 2017,
                                 "Экспорт_млн_долл"].iloc[0]
    metals = metallurgy_data.loc[metallurgy_data["Год"] == 2017,
                                 "Экспорт_млн_долл"].iloc[0]
    total = total_data.loc[total_data["Год"] == 2017,
                                 "Экспорт_млн_долл"].iloc[0]

    labels = ["Химический сектор", "Металлургия", "Другое"]
    colors = ["cyan", "silver", "gray"]
    plot.figure(figsize=(10, 6))
    plot.pie([chem, metals, total], colors=colors, labels=labels)
    plot.title("Доля промышленности, связанной с электрохимией в экспорте (2019 г.)")
    plot.figtext(0.5, 0.07, "Металлургия и химическая промышленность отвечают за 17% экспорта РФ.\n"
                           "Мой проект поможет оптимизировать производственные процессы "
                            "или найти новые пути синтеза в этих секторах.", ha="center", fontdict={"fontsize":11})
    plot.savefig(graph_path + "economy.png")
    plot.clf()


def plot_metals_produced_by_electrolysis_pie():
    labels = ["Металлы, обрабатываемые другими способами", "Аллюминий", "Никель", "Медь", "Золото"]
    sales_2019 = metallurgy_data[metallurgy_data["Год"] == 2019].iloc[0]
    sales_2019 = sales_2019.drop("Год")

    sales_2019.iloc[0] = sales_2019.iloc[0] - sales_2019.iloc[1:].sum()

    colors = ["brown", "gray", "black", "orange", "yellow"]
    plot.figure(figsize=(10, 6))
    plot.pie(sales_2019, labels=labels, colors=colors, startangle=45)

    plot.title("Доля металлов, обрабатываемых электрохимически (2019 г.)")
    plot.figtext(0.5, 0.07, "Около половины экспортируемого металла "
                            "электрохимически обрабатывается.\n"
                            "Мой проект способен понизить порог входа в металлургию "
                            "за счет упрощения систем очистки.", ha="center", fontdict={"fontsize": 11})

    plot.savefig(graph_path + "electrolysis_in_metallurgy.png")
    plot.clf()

if __name__ == "__main__":
    main()