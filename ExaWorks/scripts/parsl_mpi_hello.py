#!/bin/env python3

import parsl
from parsl.app.app import python_app, bash_app
from parsl.config import Config
from parsl.channels import LocalChannel
from parsl.providers import SlurmProvider
from parsl.executors import HighThroughputExecutor
from parsl.launchers import SimpleLauncher
from parsl.addresses import address_by_hostname
from parsl.data_provider.files import File

# Update to import config for your machine
config = Config(
    executors=[
        HighThroughputExecutor(
            label="hera_htex",
            address=address_by_hostname(),
            max_workers=40,
            provider=SlurmProvider(
                channel=LocalChannel(),
                nodes_per_block=2,
                init_blocks=1,
                partition='hera',
                scheduler_options='#SBATCH -A gsd-hpcs',
                walltime='00:10:00',
                launcher=SimpleLauncher(),
                worker_init='''
. /scratch2/BMC/gsd-hpcs/Christopher.W.Harrop/opt/spack/share/spack/setup-env.sh
ls -l $(which python3)
spack env activate flux
ls -l $(which python3)
module load intel/2022.3.0
module load impi/2022.3.0
ls -l $(which python3)
env &> /scratch2/BMC/gsd-hpcs/Christopher.W.Harrop/SENA/ExascaleWorkflowSandbox/ExaWorks/scripts/env.init
module list
''',
            ),
        )
    ],
)


import os

parsl.load(config)

remote = False
shared_dir = '/scratch2/BMC/gsd-hpcs/Christopher.W.Harrop/SENA/ExascaleWorkflowSandbox/ExaWorks/scripts'

@bash_app
def compile_app(dirpath, stdout=None, stderr=None, compiler="mpiifort -fc=ifx"):
#    """Compile mpi app using site-specific compiler.
#    E.g.,  midway compiler = mpicc, Cori compiler= cc
#    """
    return '''cd {0}; env &> ./env.compile; {1} -o mpi_hello.exe mpi_hello.f90'''.format(dirpath, compiler)

@bash_app
def mpi_hello(dirpath, app="mpi_hello.exe", nproc=40, outputs=[]):
#    """Call compiled mpi executable with local mpilib.
#    Works natively for openmpi mpiexec, mpirun, orterun, oshrun, shmerun
#    mpiexec is default"""
#    import os
#    if launcher == "mpirun" :
#        return "mpirun -np {} {} &> {};".format(nproc, os.path.join(dirpath,app), outputs[0])
#    elif launcher == "srun" :
    return "env &> env.srun; srun -n {} {} &> {};".format(nproc, app, outputs[0])

# complile the app and wait for it to complete (.result())
compile_app(dirpath=shared_dir,
            stdout=os.path.join(shared_dir, "mpi_apps.compile.out"),
            stderr=os.path.join(shared_dir, "mpi_apps.compile.err",),
           ).result()

# run the mpi app
hello = mpi_hello(dirpath=shared_dir,
                  outputs=[File(os.path.join(shared_dir, "hello.txt"))])

output_file = hello.outputs[0].result()

## if running remotely using SSH, copy the file back to the host
#if remote:
#    dfk.executor.execution_provider.channel.pull_file(output_file, '.')

# read the result file
#with open(output_file, 'r') as f:
#     print(f.read())

parsl.clear()
