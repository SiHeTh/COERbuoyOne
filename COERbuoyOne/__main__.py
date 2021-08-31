import COERbuoy
from COERbuoy.simulation import start_simu, reg_wave, bretschneider_wave, decay_test
from COERbuoyOne.benchmark import run
import COERbuoy.GUI as GUIServer
import argparse
from argparse import RawTextHelpFormatter as tf;

parser=argparse.ArgumentParser(description="The COERbuoy1 benchmark tool",formatter_class=tf)
parser.add_argument("--regular_wave", nargs=4,type=str, metavar=('H','p','filename','ctrl'),
                    help="Create and run a regular wave.\nArguments:\n"
                    "H = wave height,\n"
                    "p = wave period,\n"
                    "filename = name of output file,\n"
                    "ctr = control command.\n"
                    "Example:\n--regular_wave 1 6 output.csv linear "
                    )
parser.add_argument("--bretschneider_wave", nargs=4,metavar=('Hs','Te','filename','ctrl'),
                    help="Create and run a bretschneider sea state.\nArguments:\n"
                    "Hs = significant wave height\n"
                    "Te = energy period,\n"
                    "filename = name of output file,\n"
                    "ctr = control command.\n"
                    "Example:\n--bretschneider_wave 1 6 output.csv linear "
                    )
parser.add_argument("--benchmark", action='store_true',
                    help="Run COERbuoy1 benchmark."
                    )
parser.add_argument("--GUI", action='store_true',
                    help="Start web server for GUI."
                    )
                    
#args=parser.parse_args(["--regular_wave","3","3","lin","lin"])
args=parser.parse_args()
print("Args:")
print(args)
print(args.benchmark)
if args.regular_wave != None:
    a=args.regular_wave;
    reg_wave(float(a[0]),float(a[1]),a[2],a[3])
elif args.bretschneider_wave != None:
    a=args.bretschneider_wave;
    bretschneider_wave(float(a[0]),float(a[1]),a[2],a[3])
elif args.benchmark:
    run()
elif args.GUI:
    GUIServer.run()
