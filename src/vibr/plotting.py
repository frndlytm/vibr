import matplotlib.pyplot as plt
import pandas as pd

def plot(dfs, metric, num_units, dropout, lr, df_names=['train', 'validate'], xlabel="Epoch", save_path=""):
    for idx, df in enumerate(dfs):
        plt.plot(df.index, df[metric], label=df_names[idx])
    plt.xlabel(xlabel)
    plt.ylabel(metric)
    plt.title(f'# units ={num_units}, dropout = {dropout}, learning rate = {lr}')
    plt.legend()
    plt.savefig(save_path + "_" + metric + ".png")
    plt.close("all")

def plot_result(log_path, num_units, dropout, lr, save_path):
    df = pd.read_json(log_path, lines=True)
    df_train = df[df.step == 'train'].reset_index(drop=True)
    df_validate = df[df.step == 'validate'].reset_index(drop=True)
    plot([df_train], 'accuracy', num_units, dropout, lr, df_names=['train'], save_path=save_path)
    plot([df_train, df_validate], "loss", num_units, dropout, lr, save_path=save_path)
    plot([df_train, df_validate], "f1", num_units, dropout, lr, save_path=save_path)
    plot([df_train, df_validate], "recall", num_units, dropout, lr, save_path=save_path)
    plot([df_train, df_validate], "precision", num_units, dropout, lr, save_path=save_path)