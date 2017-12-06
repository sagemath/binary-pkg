export REPO_ROOT:=$(shell git rev-parse --show-toplevel)
export CONDA:=$(REPO_ROOT)/tools/bootstrap/miniconda/bin/conda
export TOOL:=$(REPO_ROOT)/tools/binary-pkg/bin


$(CONDA):
	./tools/bootstrap/bootstrap.sh

$(TOOL): $(CONDA)
	$(CONDA) env create -p tools/binary-pkg -f tools/binary-pkg.yaml

install-tools: $(TOOL)

install-clean:
	rm -rf tools/binary-pkg
	rm -rf tools/bootstrap/miniconda

.PHONY: install-tools install-clean

checkout-%: %.yaml $(TOOL)
	$(TOOL)/python -m binary_pkg.cmdline --config $< --checkout

build-%: %.yaml $(TOOL)
	$(TOOL)/python -m binary_pkg.cmdline --config $< --build

stage-%: %.yaml $(TOOL)
	$(TOOL)/python -m binary_pkg.cmdline --config $< --stage --package "$(PACKAGE)"

dist-%: %.yaml $(TOOL)
	$(TOOL)/python -m binary_pkg.cmdline --config $< --dist --package "$(PACKAGE)"


package-%: %.yaml
	$(MAKE) checkout-$*
	$(MAKE) build-$*
	$(MAKE) stage-$*
	$(MAKE) dist-$*


shell: $(TOOL)
	$(TOOL)/ipython

test: $(TOOL)
	$(TOOL)/python -m unittest discover

info: $(TOOL)
	$(TOOL)/python -m binary_pkg.os_information
	$(TOOL)/python -m binary_pkg.cmdline --config sage.yaml --info

transient: clean
	rm -rf /tmp/binary-pkg
	for d in source build staging dist ; do \
	    mkdir -p /tmp/binary-pkg/$$d && ln -s /tmp/binary-pkg/$$d $$d ; \
	done	
	@echo "--- Moved build directories to /tmp for development; Run make clean to switch back ---"

clean:
	rm -rf staging source build tmp dist

distclean: clean install-clean

.PHONY: shell test info transient clean distclean


include *.mk

