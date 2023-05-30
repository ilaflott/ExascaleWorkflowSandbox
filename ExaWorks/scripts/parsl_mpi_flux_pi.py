#!/bin/env python3

import parsl
from parsl.app.app import python_app, bash_app
from parsl.config import Config
from parsl.channels import LocalChannel
from parsl.providers import SlurmProvider
from parsl.executors import FluxExecutor
from parsl.launchers import SrunLauncher
from parsl.launchers import SimpleLauncher
from parsl.addresses import address_by_hostname
from parsl.data_provider.files import File

# Update to import config for your machine
config = Config(
    executors=[
        FluxExecutor(
            label="hera_flux",
#            address=address_by_hostname(),
#            max_workers=40,
#            flux_executor_kwargs = {},
#            flux_path = None,
            launch_cmd='{flux} start -v 3 {python} {manager} {protocol} {hostname} {port}',
            provider=SlurmProvider(
                scheduler_options='#SBATCH --export=ALL',
                channel=LocalChannel(),
                nodes_per_block=2,
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
                partition='hera',
                account='gsd-hpcs',
                walltime='00:10:00',
#                launcher=SrunLauncher(),
                launcher=SimpleLauncher(),
                parallelism=2,
                worker_init='''
. /scratch2/BMC/gsd-hpcs/Christopher.W.Harrop/opt/spack/share/spack/setup-env.sh
spack env activate flux
module load intel/2022.3.0
module load impi/2022.3.0
module list
env &> env.init
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
def compile_app(dirpath, stdout=None, stderr=None):#, parsl_resource_specification={'tasks': 1}):
#    """Compile mpi app using site-specific compiler.
#    E.g.,  midway compiler = mpicc, Cori compiler= cc
#    """
    return '''
    cd {dirpath}
    env &> compile.env
    module load intel/2022.3.0 impi/2022.3.0
    hostname &>> {stdout}
    mpiifort -fc=ifx -o mpi_pi.exe mpi_pi.f90
'''.format(dirpath=dirpath, stdout=stdout)

@bash_app
def compute_pi(dirpath, app="./mpi_pi.exe", outputs=[]):#, parsl_resource_specification={'num_tasks': 40}):
#    """Call compiled mpi executable with local mpilib.
#    Works natively for openmpi mpiexec, mpirun, orterun, oshrun, shmerun
#    mpiexec is default"""
    return '''
    cd {dirpath}
    env &> compute_pi.env
    module load intel/2022.3.0 impi/2022.3.0
    hostname &> {stdout}
    mpirun -np 80 {app} &>> {stdout}
'''.format(dirpath=dirpath, app=app, stdout=outputs[0])

# complile the app and wait for it to complete (.result())
compile_app(dirpath=shared_dir,
            stdout=os.path.join(shared_dir, "mpi_pi.compile.out"),
            stderr=os.path.join(shared_dir, "mpi_pi.compile.err",),
           ).result()

# run the mpi app
#mpi_pi1 = compute_pi(dirpath=shared_dir,
#                     outputs=[File(os.path.join(shared_dir, "mpi_pi1.txt"))])#, parsl_resource_specification={'num_tasks': 40, 'num_nodes': 1})
#mpi_pi2 = compute_pi(dirpath=shared_dir,
#                     outputs=[File(os.path.join(shared_dir, "mpi_pi2.txt"))], parsl_resource_specification={'tasks': 80, 'nodes': 2})

#hello2 = mpi_hello(dirpath=shared_dir,
#                   outputs=[File(os.path.join(shared_dir, "hello2.txt"))], parsl_resource_specification={'tasks': 80})
#
#hello3 = mpi_hello(dirpath=shared_dir,
#                   outputs=[File(os.path.join(shared_dir, "hello3.txt"))], parsl_resource_specification={'tasks': 80})
#
#output_file1 = mpi_pi1.outputs[0].result()
#output_file2 = mpi_pi2.outputs[0].result()
#output_file2 = hello2.outputs[0].result()
#output_file3 = hello3.outputs[0].result()
                        
parsl.clear()
