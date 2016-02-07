export REPO_ROOT:=$(shell git rev-parse --show-toplevel)
export TOOL:=$(REPO_ROOT)/tools/binary-pkg/activate


$(TOOL):
	./tools/toolaid/bootstrap
	./tools/bootstrap/bin/python3 ./tools/toolaid/bin/toolaid --build tools/binary-pkg.yaml


.PHONY: bootstrap shell test clean info

checkout-%: %.yaml $(TOOL)
	$(TOOL) python -m binary_pkg.cmdline --config $< --checkout

build-%: %.yaml $(TOOL)
	$(TOOL) python -m binary_pkg.cmdline --config $< --build

stage-%: %.yaml $(TOOL)
	$(TOOL) python -m binary_pkg.cmdline --config $< --stage --package "$(PACKAGE)"

dist-%: %.yaml $(TOOL)
	$(TOOL) python -m binary_pkg.cmdline --config $< --dist --package "$(PACKAGE)"


package-%: %.yaml
	$(MAKE) checkout-$*
	$(MAKE) build-$*
	$(MAKE) stage-$*
	$(MAKE) dist-$*


shell: $(TOOL)
	$(TOOL) ipython

test: $(TOOL)
	$(TOOL) python -m unittest discover

info: $(TOOL)
	$(TOOL) python -m binary_pkg.os_information
	$(TOOL) python -m binary_pkg.cmdline --config sage.yaml --info

transient: clean
	rm -rf /tmp/binary-pkg
	for d in source build staging dist ; do \
	    mkdir -p /tmp/binary-pkg/$$d && ln -s /tmp/binary-pkg/$$d $$d ; \
	done	
	@echo "--- Moved build directories to /tmp for development; Run make clean to switch back ---"

clean:
	rm -rf staging source build tmp dist

distclean: clean
	rm -rf tools/bootstrap tools/binary-pkg
	rm -rf tools/toolaid/bootstrap-files/hashdist
	rm -rf tools/toolaid/bootstrap-files/hashstack


include *.mk

