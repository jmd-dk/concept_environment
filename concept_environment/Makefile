# This file is part of the CO𝘕CEPT environment, the programming environment
# which makes writing clean and efficient Cython code easy.
# The CO𝘕CEPT environment can be viewed as a standalone application,
# but is really a small part of the larger CO𝘕CEPT code,
# the cosmological 𝘕-body code in Python. The CO𝘕CEPT environment
# and CO𝘕CEPT therefore share the same copyright. For this copyright,
# confront the header of e.g.
# https://raw.githubusercontent.com/jmd-dk/concept/master/installer
# Copyright © 2015-2016 Jeppe Mosgaard Dakin.
#
# The auther of the CO𝘕CEPT environment can be contacted at
# dakin(at)phys.au.dk
# The latest version of the CO𝘕CEPT environment is available at
# https://github.com/jmd-dk/concept_environment/



# Use the bash shell
SHELL = /usr/bin/env bash



##############################
# Specification of filenames #
##############################
# Modules which should be cythonized and compiled
pyfiles = commons fibonacci main



########################################
# Settings for compilation and linking #
########################################
# Python information
python               = $(firstword $(shell ls ../python/bin/python*))
python_libdir        = ../python/lib
# Options passed when cythonizing .pyx files
python_version_major = $(shell $(python) -c "import sys; print(sys.version_info.major)")
cythonflags = -$(python_version_major) -a
# Includes
python_incl = $(shell $(python)-config --includes)
includes    = $(python_incl)
# Compiler options
CC                = $(shell $(python) -c "import sysconfig; print(sysconfig.get_config_vars()['CC'])")
python_cflags     = $(shell $(python)-config --cflags)
unwanted_warnings = unreachable-code \
                    uninitialized    \
                    unused-result    \
                    unused-but-set-variable
other_cflags      = -O3 -pthread -std=c99 -fno-strict-aliasing -fPIC -Wextra $(addprefix -Wno-,$(unwanted_warnings))
CFLAGS            = $(filter-out $(addprefix -W,$(unwanted_warnings)),$(python_cflags) $(other_cflags) $(includes))
# Libraries to link
python_libs = -L$(python_libdir) -Wl,"-rpath=$(python_libdir)" $(shell $(python)-config --libs)
LDLIBS      = $(python_libs) -Wl,-O3
# Linker options
python_ldflags = $(shell $(python)-config --ldflags)
other_ldflags  = -shared
LDFLAGS        = $(python_ldflags) $(other_ldflags)



###################
# Primary targets #
###################
# The below targets are responsible for the
# .py --> (.pyx --> .pxd) --> .c --> .o --> .so build chain. For each
# module, a heading are printed at the beginning of its build process.
# The 'build_status' variable is used as a flag, controlling these
# headings.

# ANSI/VT100 escape sequences
esc=\x1b
esc_normal=$(esc)[0m
esc_bold=$(esc)[1m
esc_yellow=$(esc)[93m
esc_heading=$(esc_bold)$(esc_yellow)

# Make everything
all: $(addsuffix .so, $(pyfiles))
.PHONY: all

# Link object filed into shared object Python modules
$(addsuffix .so, $(pyfiles)): %.so: %.o
	@$(python) -c "from __future__ import print_function; print('\n$(esc_heading)Building the $(basename $@) module$(esc_normal)\n' if '$(build_status)' != 'running' else '', end='')"
	$(eval build_status = running)
	$(CC) $< -o $@ $(LDFLAGS) $(LDLIBS)
	$(eval build_status = finsihed)

# Compile c source files into object files
$(addsuffix .o, $(pyfiles)): %.o: %.c
	@$(python) -c "from __future__ import print_function; print('\n$(esc_heading)Building the $(basename $@) module$(esc_normal)\n' if '$(build_status)' != 'running' else '', end='')"
	$(eval build_status = running)
	$(CC) $(CFLAGS) -c -o $@ $<

# Cythonize .pyx and .pxd files into c source files
$(addsuffix .c, $(pyfiles)): %.c: %.pyx %.pxd
	@$(python) -c "from __future__ import print_function; print('\n$(esc_heading)Building the $(basename $@) module$(esc_normal)\n' if '$(build_status)' != 'running' else '', end='')"
	$(eval build_status = running)
	$(python) -m cython $(cythonflags) $<

# Write .pxd files from .pyx files using the pyxpp script
$(addsuffix .pxd, $(pyfiles)): %.pxd: %.pyx pyxpp.py
	@$(python) -c "from __future__ import print_function; print('\n$(esc_heading)Building the $(basename $@) module$(esc_normal)\n' if '$(build_status)' != 'running' else '', end='')"
	$(eval build_status = running)
	$(python) -B pyxpp.py $<

# Write .pyx files from .py files using the pyxpp script
$(addsuffix .pyx, $(pyfiles)): %.pyx: %.py pyxpp.py
	@$(python) -c "from __future__ import print_function; print('\n$(esc_heading)Building the $(basename $@) module$(esc_normal)\n' if '$(build_status)' != 'running' else '', end='')"
	$(eval build_status = running)
	$(python) -B pyxpp.py $<



###########################
# Additional dependencies #
###########################
# Add any additional target dependencies here.
# - Every cimport function in a .py leads to a dependency of the
#   form .c: imported_module.pxd
fibonacci.c: commons.pxd
main.c:      commons.pxd fibonacci.pxd



##################
# Cleanup target #
##################
.PHONY: clean
# Remove all compiled files
clean:
	$(RM) $(foreach ext,pyx pxd c o so html,$(addsuffix .$(ext), $(pyfiles)))
	$(RM) *.pyc
	$(RM) -r __pycache__
