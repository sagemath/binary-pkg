

bdist-sage-linux: 
	@echo "Sage Binary Packages for Generic Linux"
	$(MAKE) package-sage

bdist-sage-osx:
	@echo "Sage Binary Packages for OSX"
	$(MAKE) checkout-sage
	$(MAKE) build-sage
	$(MAKE) stage-sage PACKAGE="Full binary tarball"
	$(MAKE) dist-sage  PACKAGE="Full binary tarball"
	$(MAKE) stage-sage PACKAGE="OSX DMG image"
	$(MAKE) dist-sage  PACKAGE="OSX DMG image"
	$(MAKE) stage-sage PACKAGE="OSX mac app"
	$(MAKE) dist-sage  PACKAGE="OSX mac app"
