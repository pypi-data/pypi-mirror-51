BPH PAL (Bluepill Hat Protocol Abstraction Layer)
================================

## Description

Provides both a simple shell interface, some useful CLI commands and a bootloader for the BPH.
Simplifies dealing with pinouts with a json config file.
Simplifies installation with a pip package.

### bph_pal installation
To install bph_pal use the python3 pip package.

`pip3 install bph_pal`

### Usage of bph_pal

To use the CLI calls check the help.

`python3 -m bph_pal -h`


For using the interactive shell, for example when testing.

`bph_shell`

For bootloading PHiLIP the port should be specified on the Raspberry Pi if another board is plugged in.

`bootload_philip -p /dev/ttyAMA0 -e -w -v -pv <PHiLIP_VERSION>`

The `-h` can also be used to see optional parameters.
