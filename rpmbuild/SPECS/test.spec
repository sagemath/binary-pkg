Name:           packaging-test
Version:	7.1.beta1
Release:	1%{?dist}
Summary:	Sage Mathematical Software System
Group:		Applications/Engineering
License:	GPLv3+
URL:		http://www.sagemath.org
Source0:	test-1.0-Fedora_23-x86_64.tar.bz2

BuildRequires:  python
Requires:	m4 git gcc gcc-c++ gcc-gfortran libgfortran perl-ExtUtils-MakeMaker python openssl 

%description

%prep
%autosetup -n PackagingTest


%build
./relocate-once.py --destination /opt/PackagingTest

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt
cp -rap  %{_builddir}/PackagingTest %{buildroot}/opt/

%files
/opt/PackagingTest

%doc

%changelog

