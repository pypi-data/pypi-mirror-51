# pinda

Pip-INstallable Dockerized Applications

*pinda* is designed to deliver dockerized versions of software packages that have a user interface that is as identical
as possible to what would be available if the package was installed in the conventional way.

For example, to install Gromacs version 2019:
```
% pinda install gromacs 2019
```
Once the installation is complete, you will find the 'gmx' command in your path.

## Installation:

Easiest via pip:
```
% pip install pinda
```

## Usage:

To see a list of packages available via *pinda*:
```
% pinda list
  ambertools 16         AmberTools version 16
  ambertools 18         AmberTools version 18
* gromacs    2019       Gromacs version 2019
  gromacs    2019-cuda  Gromacs version 2019 with CUDA support
* obabel     2.4.1      Open Babel version 2.4.1
  vina       1.1.2      AutoDock Vina and selected AutoDock Tools
%
```
Packages that you have already installed are asterisked.

To install a package:
```
% pinda install ambertools 18
%
```

To uninstall a package:
```
% pinda uninstall obabel 2.4.1
%
```

For detailed information on a package:
```
% pinda info ambertools 18

AmberTools version 18

This pinda distribution provides the following commands:

    "sander"      : the Amber/Ambertools "sander" command
    "amber-shell" : drops you into a bash shell from which all other
                    AmberTools commands are accessible (e.g. tleap).

For full license and usage information, please visit http://ambermd.org

%
```
## Limitations:

You need to have [Docker](http://docker.com) installed on your machine. The containerised versions of the applications can
only 'see' files that are in the directory a command in invoked from, or a subdirectory of this, so for example:
```
% gmx mdrun -s bpti.tpr # This is fine
% gmx mdrun -s ../bpti.tpr # This won't work
```

## Author:

Charlie Laughton charles.laughton@nottingham.ac.uk

## License:

BSD 3-clause
