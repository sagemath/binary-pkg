Name:           sagemath
Version:	7.1.beta1
Release:	1%{?dist}
Summary:	Sage Mathematical Software System
Group:		Applications/Engineering
License:	GPLv3+
URL:		http://www.sagemath.org
Source0:	sage-7.1.beta1-Fedora_23-x86_64.tar.bz2

BuildRequires:  python
Requires:	m4 git gcc gcc-c++ gcc-gfortran libgfortran perl-ExtUtils-MakeMaker python openssl 

%description

%prep
%autosetup -n SageMath


%build
./relocate-once.py --destination /opt/SageMath

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt
cp -rap  %{_builddir}/SageMath %{buildroot}/opt/

%files
/opt/SageMath

%doc

%changelog

