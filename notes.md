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




## TWEAKING THE CONDA ENV, GETTING REPO CODE

install a preq or two, setup remote repo, first commit
```
# create env
mamba create -n ChiltepinEPMT_env python=3.9.16

# activate env
mamba activate ChiltepinEPMT_env

# pip install prereq
python3 -m pip install --user boto3

# clone repo
git clone git@github.com:ilaflott/ExascaleWorkflowSandbox.git ChiltepinEPMT
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
	
```
