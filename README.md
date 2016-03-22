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
The CO*N*cept environment really only cosists of three files:
* [Makefile](concept_environment/Makefile):   ...
* [pyxpp.py](concept_environment/pyxpp.py):   ...
* [commons.py](concept_environment/commons.py): ...
Other files in the [concept_environment](concept_environment) directory are
included for demonstration purposes only.


<a name="footnote">1</a>: <https://github.com/jmd-dk/concept>
