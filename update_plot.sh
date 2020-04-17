#!/bin/bash
cd ~
source ./chia-blockchain/activate


/bin/echo -e "\e[1;36m >> Updating generate_plots_yaml_file.py from GITHUB"
cd /home/ryan/chia-blockchain/src/cmds
rm generate_plots_yaml_file.py
wget https://raw.githubusercontent.com/chia-dev/chia/master/generate_plots_yaml_file.py

python generate_plots_yaml_file.py -d ~/.chia/beta-1.0b3/plots
