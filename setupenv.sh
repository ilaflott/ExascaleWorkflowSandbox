#!/bin/bash

#setup script for this project specifically

# init conda env
__init_miniforge_mamba

# FYI above equiv to...
#eval "$(/home/Ian.Laflotte/miniforge3/bin/conda shell.bash hook)"
#. "/home/Ian.Laflotte/miniforge3/etc/profile.d/mamba.sh"

# activate env
mamba activate ChiltepinEPMT_env

# activate spack env
cd install
. spack/share/spack/setup-env.sh
spack env activate chiltepin
