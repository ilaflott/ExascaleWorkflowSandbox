import os
from datetime import datetime as dt
import parsl
from parsl.app.app import bash_app
import pytest
import re

import chiltepin.config

# Compile the hello MPI program with environment passed in
@bash_app(executors=["compute"])
def compile_mpi_hello(
    dirpath,
    stdout=None,
    stderr=None,
    env="",
    parsl_resource_specification={},
):
    return """
    {}
    cd {}
    $CHILTEPIN_MPIF90 -o mpi_hello.exe mpi_hello.f90
    """.format(
        env, dirpath
    )


# Run the hello MPI program with environment passed in
@bash_app(executors=["compute"])
def run_mpi_hello(
    dirpath, stdout=None, stderr=None, env="", parsl_resource_specification={}
):
    return """
    {}
    cd {}
    $PARSL_MPI_PREFIX ./mpi_hello.exe
    #$PARSL_SRUN_PREFIX ./mpi_hello.exe
    """.format(
        env, dirpath
    )


# Compile the pi approximation MPI program with environment passed in
@bash_app(executors=["compute"])
def compile_mpi_pi(
    dirpath,
    stdout=None,
    stderr=None,
    env="",
    parsl_resource_specification={},
):
    return """
    {}
    cd {}
    $CHILTEPIN_MPIF90 -o mpi_pi.exe mpi_pi.f90
    """.format(
        env, dirpath
    )


# Run the pi approximation MPI program with environment passed in
@bash_app(executors=["compute"])
def run_mpi_pi(
    dirpath, stdout=None, stderr=None, env="", parsl_resource_specification={}
):
    return """
    {}
    cd {}
    echo PARSL_MPIEXEC_PREFIX=$PARSL_MPIEXEC_PREFIX
    echo PARSL_SRUN_PREFIX=$PARSL_SRUN_PREFIX
    echo PARSL_APRUN_PREFIX=$PARSL_APRUN_PREFIX
    echo PARSL_MPI_PREFIX=$PARSL_MPI_PREFIX
    echo PARSL_MPI_NODELIST=$PARSL_MPI_NODELIST
    echo PARSL_WORKER_POOL_ID=$PARSL_WORKER_POOL_ID
    echo PARSL_WORKER_BLOCK_ID=$PARSL_WORKER_BLOCK_ID
    $PARSL_MPI_PREFIX ./mpi_pi.exe
    #$PARSL_SRUN_PREFIX ./mpi_pi.exe
    """.format(
        env, dirpath
    )


# Set up fixture to initialize and cleanup Parsl
@pytest.fixture(scope="module")
def load_config(config_file, request):
    yaml_config = chiltepin.config.parse_file(config_file)
    config, environment = chiltepin.config.factory(yaml_config)
    parsl.load(config)
    request.addfinalizer(parsl.clear)
    return {"config": config, "environment": environment}


def test_compile_mpi_hello(load_config):
    shared_dir = "./"
    c = compile_mpi_hello(
        dirpath=shared_dir,
        stdout=(os.path.join(shared_dir, "parsl_htex_mpi_hello_compile.out"), "w"),
        stderr=(os.path.join(shared_dir, "parsl_htex_mpi_hello_compile.err"), "w"),
        env=load_config["environment"],
        parsl_resource_specification={"RANKS_PER_NODE": 1, "NUM_NODES": 1},
    ).result()
    assert c == 0
    assert os.path.isfile("mpi_hello.exe")
    assert os.stat("parsl_htex_mpi_hello_compile.out").st_size == 0


def test_run_mpi_hello(load_config):
    shared_dir = "./"
    # Remove any previous output if necessary
    if os.path.exists("parsl_htex_mpi_hello_run.out"):
        os.remove("parsl_htex_mpi_hello_run.out")
    if os.path.exists("parsl_htex_mpi_hello_run.err"):
        os.remove("parsl_htex_mpi_hello_run.err")
    hello = run_mpi_hello(
        dirpath=shared_dir,
        stdout=os.path.join(shared_dir, "parsl_htex_mpi_hello_run.out"),
        stderr=os.path.join(shared_dir, "parsl_htex_mpi_hello_run.err"),
        env=load_config["environment"],
        parsl_resource_specification={"RANKS_PER_NODE": 2, "NUM_NODES": 3},
    ).result()
    assert hello == 0
    with open("parsl_htex_mpi_hello_run.out", "r") as f:
        for line in f:
            assert re.match(r"Hello world from host \S+, rank \d+ out of 6", line)


def test_compile_mpi_pi(load_config):
    shared_dir = "./"
    c = compile_mpi_pi(
        dirpath=shared_dir,
        stdout=(os.path.join(shared_dir, "parsl_htex_mpi_pi_compile.out"), "w"),
        stderr=(os.path.join(shared_dir, "parsl_htex_mpi_pi_compile.err"), "w"),
        env=load_config["environment"],
        parsl_resource_specification={"RANKS_PER_NODE": 1, "NUM_NODES": 1},
    ).result()
    assert c == 0
    assert os.path.isfile("mpi_pi.exe")
    assert os.stat("parsl_htex_mpi_pi_compile.out").st_size == 0


def test_run_mpi_pi(load_config):
    shared_dir = "./"
    # Remove any previous output if necessary
    if os.path.exists("parsl_htex_mpi_pi1_run.out"):
        os.remove("parsl_htex_mpi_pi1_run.out")
    if os.path.exists("parsl_htex_mpi_pi1_run.err"):
        os.remove("parsl_htex_mpi_pi1_run.err")
    if os.path.exists("parsl_htex_mpi_pi2_run.out"):
        os.remove("parsl_htex_mpi_pi2_run.out")
    if os.path.exists("parsl_htex_mpi_pi2_run.err"):
        os.remove("parsl_htex_mpi_pi2_run.err")
    cores_per_node = load_config["config"].executors[1].provider.cores_per_node
    pi1 = run_mpi_pi(
        dirpath=shared_dir,
        stdout=os.path.join(shared_dir, "parsl_htex_mpi_pi1_run.out"),
        stderr=os.path.join(shared_dir, "parsl_htex_mpi_pi1_run.err"),
        env=load_config["environment"],
        parsl_resource_specification={"RANKS_PER_NODE": cores_per_node, "NUM_NODES": 2},
    )
    pi2 = run_mpi_pi(
        dirpath=shared_dir,
        stdout=os.path.join(shared_dir, "parsl_htex_mpi_pi2_run.out"),
        stderr=os.path.join(shared_dir, "parsl_htex_mpi_pi2_run.err"),
        env=load_config["environment"],
        parsl_resource_specification={"RANKS_PER_NODE": cores_per_node, "NUM_NODES": 1},
    )
    assert pi1.result() == 0
    assert pi2.result() == 0
    # Extract the hostnames used by pi1
    with open("parsl_htex_mpi_pi1_run.out", "r") as f:
        pi1_hosts = []
        for line in f:
            if re.match(r"Host ", line):
                pi1_hosts.append(line.split()[1])
    # Extract the hostnames used by pi2
    with open("parsl_htex_mpi_pi2_run.out", "r") as f:
        pi2_hosts = []
        for line in f:
            if re.match(r"Host ", line):
                pi2_hosts.append(line.split()[1])
    # Verify each pi test ran on a different set of nodes
    assert set(pi1_hosts).intersection(pi2_hosts) == set()

    # Verify pi tests un concurrently
    start_time = []
    end_time = []
    files = ["parsl_htex_mpi_pi1_run.out", "parsl_htex_mpi_pi2_run.out"]
    for f in files:
        with open(f, "r") as pi:
            for line in pi:
                if re.match(r"Start Time ", line):
                    line = line.strip().lstrip("Start Time = ")
                    start_time.append(dt.strptime(line, "%d/%m/%Y %H:%M:%S"))
                if re.match(r"End Time ", line):
                    line = line.strip().lstrip("End Time = ")
                    end_time.append(dt.strptime(line, "%d/%m/%Y %H:%M:%S"))
    assert start_time[0] < end_time[1] and start_time[1] < end_time[0]
