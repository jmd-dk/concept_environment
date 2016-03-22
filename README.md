## The CO*N*CEPT environment
The **CO*N*CEPT environment** is a programming environment, which makes writing
clean and efficient Cython code easy.
Originally developed for the CO*N*CEPT code<sup>[1](#footnote)</sup>.



### Installation
To install a seperate python distribution and setup the CO*N*CEPT environment,
simply run the [installer](installer) script. You can even invoke it directly
from a terminal, by running
```sh
bash <(wget -O- --no-ch bit.ly/concept_environment)
```

To use the CO*N*CEPT environment with a pre-installed Python distribution,
download the [Makefile](concept_environment/Makefile) and edit the `python`
and `python_libdir` definitions according to your Python distribution.


<a name="footnote">1</a>: <https://github.com/jmd-dk/concept>
