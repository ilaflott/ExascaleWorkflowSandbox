




IN HOME AREA: get miniforge:
```
    cd ~
    wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
    chmod +x Miniforge3-Linux-x86_64.sh
    ./Miniforge3-Linux-x86_64.sh #follow prompt

	#now, put conda initialization in sep func call in my_bash_funcs.sh
	#but, without that, what happens in a conda init
	eval "$(/home/Ian.Laflotte/miniforge3/bin/conda shell.bash hook)"

	# create env
	mamba create -n ChiltepinEPMT_env python=3.9.15

	# to activate the env, gotta init mamba
    . "/home/Ian.Laflotte/miniforge3/etc/profile.d/mamba.sh"	

	# activate env
	mamba activate ChiltepinEPMT_env

	# pip install prereq
	python3 -m pip install --user boto3

	# clone repo
	git clone https://github.com/ilaflott/ExascaleWorkflowSandbox.git ChiltepinEPMT
	cd ChiltepinEPMT

	# new branch + checkout
	git branch feature/epmt_tests
	git checkout feature/epmt_tests


```
