# O3CPU Power Model for gem5

This repository contains a power modeling framework for the O3CPU in the [gem5 simulator](https://www.gem5.org/). It parses simulation statistics, integrates activation energy data from McPAT and CACTI, and reports per-component and per-pipeline-stage power breakdowns.

## 🚀 Project Overview

The goal of this project is to extend the gem5 simulation platform with a detailed and realistic **power model for the O3CPU**, enabling researchers to evaluate **power-performance tradeoffs** and analyze energy consumption trends across workloads.

Unlike the existing power model for MinorCPU, this project targets the **more complex O3CPU**, which features dynamic scheduling, speculation, and deeper pipelines.

## 🧱 Core Features

- **Hierarchy-based power modeling** based on gem5's O3CPU pipeline stages
- **Stat parsing** from gem5 simulation outputs
- **Component-level energy modeling** using McPAT and CACTI
- **Workload segmentation support** using `m5_dump_reset_stats()`
- **Python implementation** for flexible analysis and reporting

## 📊 Power Estimation Flow

1. **Extract component activity counts** from gem5 stats
2. **Multiply by per-activation energy values** from McPAT/CACTI
3. **Divide by simulation time** to get power (Watts)
4. **Group results** by pipeline stages and components
5. **Plot and analyze** power trends across workloads

## 🧪 Workloads Tested

| Workload        | Power (W) |
|------------------|------------|
| DAXPY            | 1.54       |
| SAXPY            | 1.47       |
| IAX              | 3.71       |
| Sieve            | 3.35       |
| Random Branches  | 4.09       |

Trends matched expectations — integer-heavy workloads showed higher branch predictor power; random branch behavior caused high fetch-stage power.

### 📉 Known Limitations

- **Static power is not modeled** — only dynamic power based on activation energy is considered.
- **SIMD/vector instructions are not included**, as McPAT lacks support and gem5 stats lack the granularity to distinguish them.
- **Average power only** — the model reports mean power over the simulation or region; no peak or temporal granularity.
- **McPAT cannot distinguish between single (float) and double precision (double) operations**, leading to identical power estimates for workloads with different precision levels.
- **External toolchain** — the power model is implemented as a standalone Python script and not integrated directly into gem5, making automation less seamless.


## 👥 Contributors

- Kaushik Shroff  
- Ian Hogenkamp

Spring 2025 — University of Wisconsin–Madison  
Course: Advanced Computer Architecture (ECE 752)



# The gem5 Simulator

This is the repository for the gem5 simulator. It contains the full source code
for the simulator and all tests and regressions.

The gem5 simulator is a modular platform for computer-system architecture
research, encompassing system-level architecture as well as processor
microarchitecture. It is primarily used to evaluate new hardware designs,
system software changes, and compile-time and run-time system optimizations.

The main website can be found at <http://www.gem5.org>.

## Testing status

**Note**: These regard tests run on the develop branch of gem5:
<https://github.com/gem5/gem5/tree/develop>.

[![Daily Tests](https://github.com/gem5/gem5/actions/workflows/daily-tests.yaml/badge.svg?branch=develop)](https://github.com/gem5/gem5/actions/workflows/daily-tests.yaml)
[![Weekly Tests](https://github.com/gem5/gem5/actions/workflows/weekly-tests.yaml/badge.svg?branch=develop)](https://github.com/gem5/gem5/actions/workflows/weekly-tests.yaml)
[![Compiler Tests](https://github.com/gem5/gem5/actions/workflows/compiler-tests.yaml/badge.svg?branch=develop)](https://github.com/gem5/gem5/actions/workflows/compiler-tests.yaml)

## Getting started

A good starting point is <http://www.gem5.org/about>, and for
more information about building the simulator and getting started
please see <http://www.gem5.org/documentation> and
<http://www.gem5.org/documentation/learning_gem5/introduction>.

## Building gem5

To build gem5, you will need the following software: g++ or clang,
Python (gem5 links in the Python interpreter), SCons, zlib, m4, and lastly
protobuf if you want trace capture and playback support. Please see
<http://www.gem5.org/documentation/general_docs/building> for more details
concerning the minimum versions of these tools.

Once you have all dependencies resolved, execute
`scons build/ALL/gem5.opt` to build an optimized version of the gem5 binary
(`gem5.opt`) containing all gem5 ISAs. If you only wish to compile gem5 to
include a single ISA, you can replace `ALL` with the name of the ISA. Valid
options include `ARM`, `NULL`, `MIPS`, `POWER`, `RISCV`, `SPARC`, and `X86`
The complete list of options can be found in the build_opts directory.

See https://www.gem5.org/documentation/general_docs/building for more
information on building gem5.

## The Source Tree

The main source tree includes these subdirectories:

* build_opts: pre-made default configurations for gem5
* build_tools: tools used internally by gem5's build process.
* configs: example simulation configuration scripts
* ext: less-common external packages needed to build gem5
* include: include files for use in other programs
* site_scons: modular components of the build system
* src: source code of the gem5 simulator. The C++ source, Python wrappers, and Python standard library are found in this directory.
* system: source for some optional system software for simulated systems
* tests: regression tests
* util: useful utility programs and files

## gem5 Resources

To run full-system simulations, you may need compiled system firmware, kernel
binaries and one or more disk images, depending on gem5's configuration and
what type of workload you're trying to run. Many of these resources can be
obtained from <https://resources.gem5.org>.

More information on gem5 Resources can be found at
<https://www.gem5.org/documentation/general_docs/gem5_resources/>.

## Getting Help, Reporting bugs, and Requesting Features

We provide a variety of channels for users and developers to get help, report
bugs, requests features, or engage in community discussions. Below
are a few of the most common we recommend using.

* **GitHub Discussions**: A GitHub Discussions page. This can be used to start
discussions or ask questions. Available at
<https://github.com/orgs/gem5/discussions>.
* **GitHub Issues**: A GitHub Issues page for reporting bugs or requesting
features. Available at <https://github.com/gem5/gem5/issues>.
* **Jira Issue Tracker**: A Jira Issue Tracker for reporting bugs or requesting
features. Available at <https://gem5.atlassian.net/>.
* **Slack**: A Slack server with a variety of channels for the gem5 community
to engage in a variety of discussions. Please visit
<https://www.gem5.org/join-slack> to join.
* **gem5-users@gem5.org**: A mailing list for users of gem5 to ask questions
or start discussions. To join the mailing list please visit
<https://www.gem5.org/mailing_lists>.
* **gem5-dev@gem5.org**: A mailing list for developers of gem5 to ask questions
or start discussions. To join the mailing list please visit
<https://www.gem5.org/mailing_lists>.

## Contributing to gem5

We hope you enjoy using gem5. When appropriate we advise sharing your
contributions to the project. <https://www.gem5.org/contributing> can help you
get started. Additional information can be found in the CONTRIBUTING.md file.
