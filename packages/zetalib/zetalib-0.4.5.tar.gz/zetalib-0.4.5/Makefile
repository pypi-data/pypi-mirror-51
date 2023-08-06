# This Makefile is for convenience as a reminder and shortcut for the most used commands

# Package folder
PACKAGE = zetalib
#
# change to your sage command if needed
SAGE = sage

CC = gcc
CFLAGS = -O2 -Wall -Wstrict-overflow=5 -s -z defs -shared -fPIC -lc -lgmp -lz

CCVERSION = $(shell $(CC) --version 2>/dev/null)
SAGEROOT = $(shell $(SAGE) --root 2>/dev/null)

ifneq ($(SAGEROOT),)
	CFLAGS += -I $(SAGEROOT)/local/include -L $(SAGEROOT)/local/lib
ifeq ($(CCVERSION),)
	CC = $(SAGEROOT)/local/bin/gcc
	CCVERSION = $(shell $(CC) --version 2>/dev/null)
endif
endif

all: install test

install: build
	$(SAGE) -pip install --upgrade --no-index -v .

build: $(PACKAGE)/crunch.so $(PACKAGE)/addmany.so

build_wheel:
	$(SAGE) setup.py bdist_wheel

uninstall:
	$(SAGE) -pip uninstall $(PACKAGE)

develop:
	$(SAGE) -pip install --upgrade -e .

test:
	$(SAGE) setup.py test

coverage:
	$(SAGE) -coverage $(PACKAGE)/*

doc:
	cd docs && $(SAGE) -sh -c "make html"

doc-pdf:
	cd docs && $(SAGE) -sh -c "make latexpdf"

# TODO: Is this the correct way to cythonize addmany.pyx?
$(PACKAGE)/addmany.so: $(PACKAGE)/addmany.pyx
	$(SAGE) -python setup.py build_ext --inplace

$(PACKAGE)/crunch.so: $(PACKAGE)/crunch.c
ifeq ($(CCVERSION),)
	@echo "No C compiler found. Try manually setting 'CC'."
	@exit 1
endif

	cd $(PACKAGE) && $(CC) $(CFLAGS) crunch.c -o crunch.so -lgmp -lz

clean: clean-doc clean-build

clean-build:
	cd $(PACKAGE) && rm -f *.so addmany.c

clean-doc:
	cd docs && $(SAGE) -sh -c "make clean"

.PHONY: all install build build_wheel develop test coverage clean clean-doc clean-build doc doc-pdf
