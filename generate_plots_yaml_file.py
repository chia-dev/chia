import argparse
from pathlib import Path

from blspy import PrivateKey, PublicKey

from src.util.config import config_path_for_filename, load_config, save_config
from src.util.default_root import DEFAULT_ROOT_PATH
from src.util.path import make_path_relative, mkdir, path_from_root

def main():
    """
    Script for creating plots.yaml from a directory (output file name ==> plots-generated.yaml).
    Copy script to ~/chia-blockchain/src/cmds
    Execute by running: python generate_plots_yaml_file.py 

    Without any parameters the default plots.yaml and keys.yaml locations will be used

    python generate_plots_yaml_file.py -d /mnt/bigdisk/plots             #will scan the specified drive and will create plots-generated.yaml

    python generate_plots_yaml_file.py -a True -d /mnt/bigdisk/plots     #will append entries to lots-generated.yaml, for 2nd, 3rd drives
    """
    root_path = DEFAULT_ROOT_PATH
    plot_config_filename = config_path_for_filename(root_path, "plots.yaml")
    key_config_filename = config_path_for_filename(root_path, "keys.yaml")

    parser = argparse.ArgumentParser(description="Chia plots.yaml generator")

    parser.add_argument("-a", "--append", help="Append to an existing output file", type=bool, default=False)

    new_plots_root = path_from_root(
        root_path,
        load_config(root_path, "config.yaml")
        .get("harvester", {})
        .get("new_plot_root", "plots"),
    )

    parser.add_argument(
        "-d",
        "--final_dir",
        help="Directory of plots",
        type=Path,
        default=Path(new_plots_root),
    )

    # We need the keys file, to access pool keys (if the exist), and the sk_seed.
    args = parser.parse_args()
    if not key_config_filename.exists():
        raise RuntimeError("Can not find keys.yaml.")

    # The seed is what will be used to generate a private key for each plot
    key_config = load_config(root_path, key_config_filename)
    sk_seed: bytes = bytes.fromhex(key_config["sk_seed"])

    pool_pk: PublicKey
        # Use the pool public key from the config, useful for solo farming
    pool_sk = PrivateKey.from_bytes(bytes.fromhex(key_config["pool_sks"][0]))
    pool_pk = pool_sk.get_public_key()

    paths = Path(args.final_dir)
    if not paths.exists():
        raise RuntimeError("Path does not exist.")

    if args.append:
        outfile = open(str(plot_config_filename)[0:-5] + "-generated.yaml","a+")        
    else:
        outfile = open(str(plot_config_filename)[0:-5] + "-generated.yaml","w+")
        outfile.write("plots:\r");

    pathlist = Path(args.final_dir).glob('*.dat')
    pathlist = sorted(pathlist)
    for path in pathlist:
        #get only th filename from the full path
        filename = path.name

        #split the filename into index, size and plot_seed
        tmp = filename.split('-')
        index = int(tmp[1]) 
        size = int(tmp[2])
        plot_seed = tmp[3]

        #remove the file extension
        plot_seed = plot_seed[0:-4]
        sk: PrivateKey = PrivateKey.from_seed(
            sk_seed + size.to_bytes(1, "big") + index.to_bytes(4, "big")
        )
        outfile.write("  " + str(path) + ":\r")
        outfile.write("    pool_pk: " + bytes(pool_pk).hex() + "\r")
        outfile.write("    sk: " + bytes(sk).hex() + "\r")

    outfile.close()
    print("plots-generated.yaml created in the config directory")
if __name__ == "__main__":
    main()
