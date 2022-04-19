# `vibr`: Vibe Classification

CS6120 - Machine Learning Course Project

## Setup

Use the following commands for a standard enviornment install.

### Create a New Environment

```PowerShell
[frndlytm] PS vibr> conda env create -f environment.yml
[frndlytm] PS vibr> conda develop ./src
```

The first command creates a vibr environment in your `conda` envs. The second mounts `./src` in develop mode so that you can import from the packages inside it.

### Update an Existing Environment

After the environment is created, you can synchronize any future changes into your existing environment via the following command.

```PowerShell
[frndlytm] PS vibr> conda env create -f environment.yml
```

### Freezing an Existing Environment

After updating any packages, you _should_ freeze your changed environment to the `environment.yml` file via the following command.

```PowerShell
[frndlytm] PS vibr> conda env export > environment.yml
```

This is important to ensure we all stay synchonized and our code ports well.

### Clone related projects

The related projects are:

1. `musicnn` <https://github.com/jordipons/musicnn>
2. `listening-moods` <https://github.com/fdlm/listening-moods>

Getting these configured as submodules was stupidly difficult due to lfs size limitations on the `data` directories, so instead I have opted to include `musicnn` in `requirements.txt` for our usage, but also clone both of these projects in the parent directory of our `vibr`.

Specific installing instructions for each have been included.

#### `musicnn`

```PowerShell
[frndlytm] PS vibr> git clone git@github.com:jordipons/musicnn.git ../
```

#### `listening-moods`

First, clone the repo, which might yield the following error...

```PowerShell
[frndlytm] PS vibr> git clone git@github.com:fdlm/listening-moods.git ../
Cloning into 'listening-moods'...
remote: Counting objects: 100% (23/23), done.
Receiving objects: 100% (23/23), 3.77 MiB | 6.96 MiB/s, done.
Resolving deltas: 100% (4/4), done.
Updating files: 100% (14/14), done.
Downloading data/mcn_msd_big_source.npy (134 MB)
Error downloading object: data/mcn_msd_big_source.npy (fae4e8d): Smudge error: Error downloading data/mcn_msd_big_source.npy (fae4e8dd38a4136d4b87beed9c101445f5b7c01e67753d42893ebadf0f4e5dbd): batch response: This repository is over its data quota. Account responsible for LFS bandwidth should purchase more data packs to restore access.

Errors logged to .git\lfs\logs\20220227T114346.700646.log
error: external filter 'git-lfs filter-process' failed
fatal: data/mcn_msd_big_source.npy: smudge filter lfs failed
warning: Clone succeeded, but checkout failed.
You can inspect what was checked out with 'git status'
and retry with 'git restore --source=HEAD :/'
```

This is a known issue and can be resolved by donwloading a `data.tar.gz` via the README on the `listening-moods` repo and manually extracting it into the data directory.

## Maintenance

(Untested) We can maintain code-style configured in `pyproject.yaml` through:

```PowerShell
[frndlytm] PS vibr> ./scripts/notebook-format ./notebooks/notebook
```

## running on cluster

### useful commands

run model as batch script
```sh
$ cd {path to repo}/src/listening-moods
$ sbatch run.sh
```
doing interactive development (note: git does not on the compute node, only on the login node)
```sh
$ srun --pty bash 
```
to use vscode on cluster, see https://code.visualstudio.com/docs/remote/ssh-tutorial

to use jupyter notebooks on the cluster, see https://rc-docs.northeastern.edu/en/latest/using-ood/introduction.html

### using git lfs
download from website https://github.com/git-lfs/git-lfs/releases/tag/v3.1.2

```sh
$ wget https://github.com/git-lfs/git-lfs/releases/download/v3.1.2/git-lfs-linux-amd64-v3.1.2.tar.gz
```
extract file
```sh
$ tar -xf {path to git lfs}/git-lfs-linux-amd64-v3.1.2.tar.gz
```
add git lfs to path
```sh
$ PATH="{path to git lfs}/git-lfs-v3.1.2:$PATH"
```
using git-lfs executable as you would with fit lfs
```sh
$ cd {path to git lfs}/git-lfs-v3.1.2
$ ./git-lfs -h
```
