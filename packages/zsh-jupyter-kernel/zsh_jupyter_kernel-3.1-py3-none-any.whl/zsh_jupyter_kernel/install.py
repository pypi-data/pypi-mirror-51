import argparse
import json
import os
import sys

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory

from .config import config

def install_my_kernel_spec(user = True, prefix = None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(config['kernel']['spec'], f, sort_keys = True)
        # TODO: Copy any resources

        KernelSpecManager().install_kernel_spec(td,
            kernel_name = 'zsh',
            user = user,
            prefix = prefix,
        )
        print("Installed Z shell Jupyter kernel spec with prefix " + prefix)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False # assume not an admin on non-Unix platforms

def main(argv = None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', action = 'store_true',
        help="Install to the per-user kernels registry. Default if not root.")
    ap.add_argument('--sys-prefix', action = 'store_true',
        help="Install to sys.prefix (e.g. a virtualenv or conda env)")
    ap.add_argument('--prefix',
        help="Install to the given prefix. "
             "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/")
    args = ap.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True

    install_my_kernel_spec(user = args.user, prefix = args.prefix)

if __name__ == '__main__':
    main(sys.argv[1:])
