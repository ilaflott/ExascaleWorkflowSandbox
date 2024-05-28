## SETUP I DID

get miniforge, init conda/mamba, create env
```
cd ~
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
chmod +x Miniforge3-Linux-x86_64.sh
./Miniforge3-Linux-x86_64.sh #follow prompt

#now, put conda initialization in sep func call in my_bash_funcs.sh
#but, without that, what happens in a conda init
eval "$(/home/Ian.Laflotte/miniforge3/bin/conda shell.bash hook)"

# init mamba
. "/home/Ian.Laflotte/miniforge3/etc/profile.d/mamba.sh"

# point envs and pkgs dirs to location with larger quota
echo "pkgs_dirs:"                                      >> /home/$USER/miniforge3/.condarc
echo "  - /collab1/data/Ian.Laflotte/miniforge3/pkgs"  >> /home/$USER/miniforge3/.condarc
echo "envs_dirs:"									   >> /home/$USER/miniforge3/.condarc
echo "  - /collab1/data/Ian.Laflotte/miniforge3/envs"  >> /home/$USER/miniforge3/.condarc

```




## CREATE/TWEAK THE CONDA ENV

create env, install a preq or two
```
# create env
mamba create -n ChiltepinEPMT_env python=3.9.16

# activate env
mamba activate ChiltepinEPMT_env
```

##  GETTING CHILTEPIN REPO CODE
setup remote repo, first commit
```
# clone repo
cd /collab1/data/Ian.Laflotte/Working
git git@github.com:ilaflott/ExascaleWorkflowSandbox.git ChiltepinEPMT
cd ChiltepinEPMT

# new branch + checkout, add these notes and setupenv script for sanity
git branch feature/epmt_tests
git checkout feature/epmt_tests
git add setupenv.sh notes.md
git commit -a
git push
```


## INSTALLATION

now the fun begins. following the README.md instructions.
```
# pip install prereq
python3 -m pip install --user boto3

# spack things. according to README, mainly for Flux
# Flux which is being removed from recent commit notes
# going with it for now anyways.
cd install
./install.sh
```

the build appears to complete successfully, some warnings or "errors",
but i do not think these are showstoppers yet, as the build continues
```
# worrisome warnings...
...
Collecting pyzmq==25.1.2
  Downloading pyzmq-25.1.2-cp310-cp310-manylinux_2_28_x86_64.whl (1.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 5.8 MB/s eta 0:00:00
Installing collected packages: pyzmq, dill
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
globus-compute-sdk 2.20.0 requires dill==0.3.5.1; python_version < "3.11", but you have dill 0.3.8 which is incompatible.
Successfully installed dill-0.3.8 pyzmq-25.1.2

[notice] A new release of pip is available: 23.1.2 -> 24.0
[notice] To update, run: pip install --upgrade pip
...
...
...
Installing collected packages: greenlet, sqlalchemy, parsl
  Attempting uninstall: parsl
    Found existing installation: parsl 2024.3.18
    Uninstalling parsl-2024.3.18:
      Successfully uninstalled parsl-2024.3.18
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
globus-compute-endpoint 2.20.0 requires parsl==2024.3.18, but you have parsl 2024.3.4 which is incompatible.
Successfully installed greenlet-3.0.3 parsl-2024.3.4 sqlalchemy-1.4.52

[notice] A new release of pip is available: 23.1.2 -> 24.0
[notice] To update, run: pip install --upgrade pip
...
```


this set of steps seems to go just fine. 
```
# now, activating the spack env...
cd install # if not already in install dir...
. spack/share/spack/setup-env.sh
spack env activate chiltepin
```

now we do a local install for tests at least...
```
cd <repository root>
pip install -e .

```