'''
The MIT License (MIT)

Copyright (c) 2013 Patrick Olsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Author: Patrick Olsen
Email: patrickolsen@sysforensics.org
Twitter: @patrickrolsen
'''
import sys, os
import argparse
import glob
from Registry import Registry

parser = argparse.ArgumentParser(description='Parse the Windows registry for malware-ish related artifacts.')
parser.add_argument('-nt', '--ntuser', defaut='', help='Path to the NTUSER.DAT hive you want parsed.')
parser.add_argument('-sys', '--system', defaut='', help='Path to the SYSTEM hive you want parsed.')
parser.add_argument('-soft', '--software', defaut='', help='Path to the SOFTWARE hive you want parsed.')
parser.add_argument('-p', '--plugin', required=True, nargs='+', help='Specify plugins to run.')
parser.add_argument('-lp', '--listplugins', action='store_true', help='Lists the available plugins.')

args = parser.parse_args()

reg_nt = Registry.Registry(args.ntuser)
reg_soft = Registry.Registry(args.software)
reg_sys = Registry.Registry(args.system)

if args.listplugins:
    for plugs in glob.glob(os.path.join("plugins", "*.py")):
        if "None" in plugs:
            pass
        else:
            print plugs.replace("plugins/", "").replace(".py", "").strip()

def main():
    for plugin_name in args.plugin:
        sys.path.insert(0, 'plugins')
        module = __import__(plugin_name)
        module.getPlugin(reg_nt=reg_nt, reg_soft=reg_soft, reg_sys=reg_sys)
if __name__ == "__main__":
    main()