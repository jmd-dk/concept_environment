## The CO*N*CEPT environment
The **CO*N*CEPT environment** is a programming environment, which makes writing
clean and efficient Cython code easy.
Originally developed for the CO*N*CEPT code<sup>[1](#footnote)</sup>.



### Installation
To install a seperate python distribution and setup the CO*N*CEPT environment,
simply run the [installer](installer) script. You can even invoke it directly
from a terminal, by running
```
bash <(wget -O- --no-ch bit.ly/concept_environment)
```

To use the CO*N*CEPT environment with a pre-installed Python distribution,
download the files in the [concept_environment](concept_environment) directory
and edit the `python` variable in the [Makefile](concept_environment/Makefile),
so that it points to the Python interpreter of your Python distribution.

### Usage
The CO*N*CEPT environment really only cosists of three files:
* [Makefile](concept_environment/Makefile): Controls the entire build process
* [pyxpp.py](concept_environment/pyxpp.py): Responsible for compiling CO*N*CEPT cython code into normal cython code
* [commons.py](concept_environment/commons.py): Implements global definitions used by compilable modules. These definitions come in two forms; actual cython constructs or dummy-emulations of cython constructs used when running in pur Python (non-compield) mode.

Other files in the [concept_environment](concept_environment) directory are
included for demonstration purposes only.

To compile a Python `.py` module into a shared object `.so` file,
you need to add the module name to the `pyfiles` variable in the [Makefile](concept_environment/Makefile).
You should also declare any dependencies in the `Additional dependencies`
section of the [Makefile](concept_environment/Makefile).

<a name="footnote">1</a>: <https://github.com/jmd-dk/concept>
