export REPO_ROOT:=$(shell git rev-parse --show-toplevel)
export TOOL:=$(REPO_ROOT)/tools/binary-pkg/activate


bootstrap:
	./tools/toolaid/bootstrap
	./tools/toolaid/bin/toolaid --build tools/binary-pkg.yaml



.PHONY: bootstrap shell test clean info

checkout-%: %.yaml
	$(TOOL) python -m binary_pkg.cmdline --config $^ --checkout

build-%: %.yaml
	$(TOOL) python -m binary_pkg.cmdline --config $^ --build

stage-%: %.yaml
	$(TOOL) python -m binary_pkg.cmdline --config $^ --stage

dist-%: %.yaml
	$(TOOL) python -m binary_pkg.cmdline --config $^ --dist


package-%: %.yaml
	$(MAKE) checkout-$*
	$(MAKE) build-$*
	$(MAKE) stage-$*
	$(MAKE) dist-$*


shell:
	$(TOOL) ipython

test:
	$(TOOL) python -m unittest discover

info:
	$(TOOL) python -m binary_pkg.os_information
	$(TOOL) python -m binary_pkg.cmdline --config sage.yaml --info

clean:
	rm -rf source build tmp dist

distclean: clean
	rm -rf tools/bootstrap tools/binary-pkg
	rm -rf tools/toolaid/bootstrap-files/hashdist
	rm -rf tools/toolaid/bootstrap-files/hashstack
