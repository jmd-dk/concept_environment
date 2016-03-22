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



###################################################
# Modules which should be cythonized and compiled #
###################################################
pyfiles = commons fibonacci main



##########################
# The Python interpreter #
##########################
python = $(firstword $(shell ls ../python/bin/python*))



########################################
# Settings for compilation and linking #
########################################
# Function which takes in a quoted argument. If this argument is
# a path (perhaps prefixed with e.g. -I) and it is located near this
# Makefile, the return value is the relative path. Otherwise, the
# return value is just the untouched argument.
# A backslash will be placed before spaces.
sensible_path = $(shell $(python) -c "import os;                                                  \
                                      path = $1;                                                  \
                                      prefix = ([''] + [prefix for prefix in                      \
                                                        ('-I', '-L', '-Wl,-rpath=')               \
                                                        if path.startswith(prefix)]               \
                                                )[-1];                                            \
                                      abspath = path[len(prefix):];                               \
                                      relpath = os.path.relpath(abspath, '.');                    \
                                      path = abspath if relpath.startswith('../..') else relpath; \
                                      path = prefix + path;                                       \
                                      path = path.replace(' ', chr(92) + ' ');                    \
                                      path = path.replace(2*chr(92), chr(92));                    \
                                      print(path);                                                \
                                      "                                                           \
                  )
# Function which eliminates duplicates
uniq = $(if $1,$(firstword $1) $(call uniq,$(filter-out $(firstword $1),$1)))
# The python configuration script
python_config = $(python)-config
# Options passed when cythonizing .pyx files
python_version_major = $(shell $(python) -c "import sys; print(sys.version_info.major)")
cythonflags = -$(python_version_major) -a
# Includes
python_incl = $(shell $(python_config) --includes)
includes    = $(python_incl)
# Compiler options
python_cc         = $(shell $(python) -c "import sysconfig;                      \
                                          print(sysconfig.get_config_var('CC')); \
                                          "                                      \
                      )
CC                = $(call uniq, $(foreach flag, $(python_cc),                   \
                                                 $(call sensible_path,'$(flag)') \
                                   )                                             \
                      )
unwanted_warnings = unreachable-code \
                    uninitialized    \
                    unused-result    \
                    unused-but-set-variable
python_cflags     = $(filter-out $(addprefix -W,$(unwanted_warnings)), \
                                 $(shell $(python_config) --cflags))
other_cflags      = -O3                  \
                    -pthread             \
                    -std=c99             \
                    -fno-strict-aliasing \
                    -fPIC                \
                    -Wall                \
                    -Wextra              \
                    $(addprefix -Wno-,$(unwanted_warnings))
CFLAGS            = $(call uniq, $(foreach flag, $(python_cflags)                \
                                                 $(other_cflags)                 \
                                                 $(includes)                     \
                                                 ,                               \
                                                 $(call sensible_path,'$(flag)') \
                                   )                                             \
                      )
# Libraries to link
python_libdir = $(shell $(python) -c "import sysconfig;                          \
                                      print(sysconfig.get_config_var('LIBDIR')); \
                                      "                                          \
                  )
python_libs   = -L$(python_libdir) -Wl,-rpath=$(python_libdir) $(shell $(python_config) --libs)
other_libs    = -Wl,-O3
LDLIBS        = $(call uniq, $(foreach flag, $(python_libs)                   \
                                             $(other_libs)                    \
                                             ,                                \
                                              $(call sensible_path,'$(flag)') \
                               )                                              \
                  )
# Linker options
python_ldflags = $(shell $(python_config) --ldflags)
other_ldflags  = -shared
LDFLAGS        = $(call uniq, $(foreach flag, $(python_ldflags)               \
                                              $(other_ldflags)                \
                                              ,                               \
                                              $(call sensible_path,'$(flag)') \
                                )                                             \
                   )



###################
# Primary targets #
###################
# The below targets are responsible for the
# .py --> (.pyx --> .pxd) --> .c --> .o --> .so build chain. For each
# module, a heading are printed at the beginning of its build process.
# The 'build_status' variable is used as a flag, controlling these
# headings.

# ANSI/VT100 escape sequences
esc         = \x1b
esc_normal  = $(esc)[0m
esc_bold    = $(esc)[1m
esc_yellow  = $(esc)[93m
esc_heading = $(esc_bold)$(esc_yellow)
# Function which prints out the headings
define heading
$(python) -c "print('\n' if '$(build_status)' and '$(build_status)' != 'running' else '', \
                    end='');                                                              \
              print('$(esc_heading)Building the $(basename $@) module$(esc_normal)\n'     \
                    if '$(build_status)' != 'running' else '',                            \
                    end='');                                                              \
              "
endef

# Make everything
all: $(addsuffix .so, $(pyfiles))
	@# This suppresses "make: Nothing to be done for `all'."
.PHONY: all

# Link object filed into shared object Python modules
$(addsuffix .so, $(pyfiles)): %.so: %.o
	@$(call heading)
	$(CC) $< -o $@ $(LDFLAGS) $(LDLIBS)
	$(eval build_status = finsihed)

# Compile c source files into object files
$(addsuffix .o, $(pyfiles)): %.o: %.c
	@$(call heading)
	$(eval build_status = running)
	$(CC) $(CFLAGS) -c -o $@ $<

# Cythonize .pyx and .pxd files into C source files
# (and also produce the annotated .html file).
$(addsuffix .c, $(pyfiles)): %.c: %.pyx %.pxd
	@$(call heading)
	$(eval build_status = running)
	$(python) -m cython $(cythonflags) $<
# Same as above (for explicit builds of html)
$(addsuffix .html, $(pyfiles)): %.html: %.pyx %.pxd
	$(python) -m cython $(cythonflags) $<

# Write .pxd files from .pyx files using the pyxpp script
$(addsuffix .pxd, $(pyfiles)): %.pxd: %.pyx pyxpp.py
	@$(call heading)
	$(eval build_status = running)
	$(python) -B pyxpp.py $<

# Write .pyx files from .py files using the pyxpp script
$(addsuffix .pyx, $(pyfiles)): %.pyx: %.py pyxpp.py $(MAKEFILE_LIST)
	@$(call heading)
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

