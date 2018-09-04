import os
from pprint import pprint
import mpi4py.rc
mpi4py.rc.initialize = False
import sys
import argparse
from numpy import float64
from skopt.benchmarks import branin


NDIM = 2

here = os.path.dirname(os.path.abspath(__file__))
top = os.path.dirname(os.path.dirname(os.path.dirname(here)))
sys.path.append(top)
BNAME = os.path.splitext(os.path.basename(__file__))[0]

from deephyper.benchmarks import util
from deephyper.benchmarks import keras_cmdline

def run(param_dict):
    x = [param_dict[f'x{i}'] for i in range(1, 1+NDIM)]
    assert len(x) == NDIM and all(type(xi) in [float,float64] for xi in x), f"expected {NDIM} input-dimension of floats; got {len(x)}; types are {[type(xi) for xi in x]}"
    pprint(x)
    result = branin(x)
    print("OUTPUT:", result)
    return result


def augment_parser(parser):
    for i in range(1, NDIM+1):
        parser.add_argument(f'--x{i}', type=float, default=2.0+i)
    return parser

if __name__ == "__main__":
    parser = keras_cmdline.create_parser()
    parser = augment_parser(parser)
    cmdline_args = parser.parse_args()
    param_dict = vars(cmdline_args)
    run(param_dict)