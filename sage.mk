

bdist-sage-linux: 
	@echo "Sage Binary Packages for Generic Linux"
	$(MAKE) package-sage

bdist-sage-macos:
	@echo "Sage Binary Packages for macOS"
	$(MAKE) checkout-sage
	$(MAKE) build-sage
	$(MAKE) stage-sage PACKAGE="Full binary tarball"
	$(MAKE) dist-sage  PACKAGE="Full binary tarball"
	$(MAKE) stage-sage PACKAGE="macOS disk image"
	$(MAKE) dist-sage  PACKAGE="macOS disk image"
	$(MAKE) stage-sage PACKAGE="macOS app"
	$(MAKE) dist-sage  PACKAGE="macOS app"
