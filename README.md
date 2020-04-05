# PLOTS.YAML Generator for Chia Blockchain

Script for creating Chia Blockchain plots.yaml files.

Instead of copying plots.yaml entries manually from your Plotting machines to your Farmers/Harvesters this script will scan a directory and generate a plots.yaml file for you.

The generated file will be called plots-generated.yaml and will be located in the default config directory.
** Remember to rename plots-generated.yaml to plots.yaml **

Copy script to `~/chia-blockchain/src/cmds`

Execute by running: 
```
python generate_plots_yaml_file.py 
```
Without any parameters the default plots.yaml and keys.yaml locations will be used

Specifying an output directory
```
    python generate_plots_yaml_file.py -d /mnt/bigdisk/plots
```    
This command will scan the specified drive and will create plots-generated.yaml

Appending entries for 2nd, 3rd hard disks
```
    python generate_plots_yaml_file.py -d /mnt/disk1/plots
    python generate_plots_yaml_file.py -a True -d /mnt/disk2/plots
    python generate_plots_yaml_file.py -a True -d /mnt/disk3/plots
```    
This command will append entries to lots-generated.yaml, for 2nd, 3rd drives

