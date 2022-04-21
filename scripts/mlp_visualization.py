import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

vibr_dir = ""    # change to vibr directory
df_2_20 = pd.read_json(vibr_dir + 'vibr/models/2-20-0.25-0.0004-100-2000-4-100/model-name-1650420642919/model-name-1650420642919.log.jsonl', lines=True)
df_2_40 = pd.read_json(vibr_dir +'vibr/models/2-40-0.25-0.0004-100-2000-4-100/model-name-1650420644785/model-name-1650420644785.log.jsonl', lines=True)
df_2_200 = pd.read_json(vibr_dir +'vibr/models/2-200-0.25-0.0004-100-2000-4-100/model-name-1650420647090/model-name-1650420647090.log.jsonl', lines=True)
df_2_400 = pd.read_json(vibr_dir + 'vibr/models/2-400-0.25-0.0004-100-2000-4-100/model-name-1650420650121/model-name-1650420650121.log.jsonl', lines=True)
df_2_2000 = pd.read_json(vibr_dir +'vibr/models/2-2000-0.25-0.0004-100-2000-4-100/model-name-1650420662342/model-name-1650420662342.log.jsonl', lines=True)
df_2_4000 = pd.read_json(vibr_dir +'vibr/models/2-4000-0.25-0.0004-100-2000-4-100/model-name-1650420668771/model-name-1650420668771.log.jsonl', lines=True)
df_4_20 = pd.read_json(vibr_dir +'vibr/models/4-20-0.25-0.0004-100-2000-4-100/model-name-1650420674909/model-name-1650420674909.log.jsonl', lines=True)
df_4_40 = pd.read_json(vibr_dir +'vibr/models/4-40-0.25-0.0004-100-2000-4-100/model-name-1650420680050/model-name-1650420680050.log.jsonl', lines=True)
df_4_200 = pd.read_json(vibr_dir +'vibr/models/4-200-0.25-0.0004-100-2000-4-100/model-name-1650420690811/model-name-1650420690811.log.jsonl', lines=True)
df_4_400 = pd.read_json(vibr_dir +'vibr/models/4-400-0.25-0.0004-100-2000-4-100/model-name-1650420693579/model-name-1650420693579.log.jsonl', lines=True)
df_4_2000 = pd.read_json(vibr_dir +'vibr/models/4-2000-0.25-0.0004-100-2000-4-100/model-name-1650420700388/model-name-1650420700388.log.jsonl', lines=True)
df_4_4000 = pd.read_json(vibr_dir +'vibr/models/4-4000-0.25-0.0004-100-2000-4-100/model-name-1650420709689/model-name-1650420709689.log.jsonl', lines=True)
df_8_20 = pd.read_json(vibr_dir +'vibr/models/8-20-0.25-0.0004-100-2000-4-100/model-name-1650421235073/model-name-1650421235073.log.jsonl', lines=True)
df_8_40 = pd.read_json(vibr_dir +'vibr/models/8-40-0.25-0.0004-100-2000-4-100/model-name-1650421311759/model-name-1650421311759.log.jsonl', lines=True)
df_8_200 = pd.read_json(vibr_dir +'vibr/models/8-200-0.25-0.0004-100-2000-4-100/model-name-1650421326227/model-name-1650421326227.log.jsonl', lines=True)
df_8_400 = pd.read_json(vibr_dir +'vibr/models/8-400-0.25-0.0004-100-2000-4-100/model-name-1650421329394/model-name-1650421329394.log.jsonl', lines=True)
df_8_2000 = pd.read_json(vibr_dir +'vibr/models/8-2000-0.25-0.0004-100-2000-4-100/model-name-1650421329394/model-name-1650421329394.log.jsonl', lines=True)
df_8_4000 = pd.read_json(vibr_dir +'vibr/models/8-4000-0.25-0.0004-100-2000-4-100/model-name-1650421346115/model-name-1650421346115.log.jsonl', lines=True)

metric = "loss"
fig, ax = plt.subplots(3, 6, figsize=(30, 15))
min_ylim = 1
max_ylim = 0
for i, layer in enumerate([2, 4, 8]):
    for j, units in enumerate([20, 40, 200, 400, 2000, 4000]):
        df = eval(f"df_{layer}_{units}")
        df_train = df[df['step']=="train"].reset_index(drop=True)
        df_validate = df[df['step']=="validate"].reset_index(drop=True)
        ax[i, j].plot(df_train.index, df_train[metric], label="train")
        ax[i, j].plot(df_validate.index, df_validate[metric], label="validate")
        ax[i, j].set_title(f"layer = {layer}, units = {units}")
        bottom, top = ax[i, j].get_ylim()
        if bottom < min_ylim: 
            min_ylim = bottom
        if top > max_ylim:
            max_ylim = top
plt.setp(ax, ylim=(min_ylim, max_ylim))
fig.suptitle(metric)
plt.savefig("loss_curve.png")




metric = "loss"
fig, ax = plt.subplots(1,2, figsize=(15, 4))

layer_lst = [2, 4, 8]
units_lst = [20, 40, 200, 400, 2000, 4000]
heat_train = np.zeros((len(layer_lst), len(units_lst)))
heat_validate = np.zeros((len(layer_lst), len(units_lst)))

for i, layer in enumerate(layer_lst):
    for j, units in enumerate(units_lst):
        df = eval(f"df_{layer}_{units}")
        df_train = df[df['step']=="train"].reset_index(drop=True)
        df_validate = df[df['step']=="validate"].reset_index(drop=True)
        heat_train[i, j] = df_train[metric].iloc[-1]
        heat_validate[i, j] = df_validate[metric].iloc[-1]

c = ax[0].pcolor(heat_train)
c.set_clim(vmin=min(np.min(heat_train), np.min(heat_validate)), vmax=max(np.max(heat_train), np.max(heat_validate)))
ax[0].set_title('train')
fig.colorbar(c, ax=ax[0])
ax[0].set_yticks(np.arange(heat_train.shape[0])+0.5, minor=False)
ax[0].set_xticks(np.arange(heat_train.shape[1])+0.5, minor=False)
ax[0].invert_yaxis()
ax[0].xaxis.tick_top()

ax[0].set_xticklabels(units_lst, minor=False)
ax[0].set_yticklabels(layer_lst, minor=False)

c = ax[1].pcolor(heat_validate)
ax[1].set_title('test')
fig.colorbar(c, ax=ax[1])
ax[1].set_yticks(np.arange(heat_validate.shape[0])+0.5, minor=False)
ax[1].set_xticks(np.arange(heat_validate.shape[1])+0.5, minor=False)
ax[1].invert_yaxis()
ax[1].xaxis.tick_top()

ax[1].set_xticklabels(units_lst, minor=False)
ax[1].set_yticklabels(layer_lst, minor=False)

c.set_clim(vmin=min(np.min(heat_train), np.min(heat_validate)), vmax=max(np.max(heat_train), np.max(heat_validate)))

fig.suptitle(metric)
fig.tight_layout()
plt.savefig("heatmap.png")