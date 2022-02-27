#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Readonly
%define		pnam	XS
Summary:	Readonly::XS - Companion module for Readonly.pm, to speed up read-only scalar variables
Name:		perl-Readonly-XS
Version:	1.05
Release:	14
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Readonly/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	df71f29abfcbd14c963f912d6d6ded6b
URL:		http://search.cpan.org/dist/Readonly-XS/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Readonly >= 1.02
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Readonly module (q.v.) is an effective way to create
non-modifiable variables. However, it's relatively slow.

The reason it's slow is that is implements the read-only-ness of
variables via tied objects. This mechanism is inherently slow. Perl
simply has to do a lot of work under the hood to make tied variables
work.

This module corrects the speed problem, at least with respect to
scalar variables. When Readonly::XS is installed, Readonly uses it to
access the internals of scalar variables. Instead of creating a scalar
variable object and tying it, Readonly simply flips the SvREADONLY bit
in the scalar's FLAGS structure.

Readonly arrays and hashes are not sped up by this, since the
SvREADONLY flag only works for scalars. Arrays and hashes always use
the tie interface.

Why implement this as a separate module? Because not everyone can use
XS. Not everyone has a C compiler. Also, installations with a
statically-linked perl may not want to recompile their perl binary
just for this module. Rather than render Readonly.pm useless for these
people, the XS portion was put into a separate module.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorarch}/Readonly/
%{perl_vendorarch}/Readonly/*.pm
%dir %{perl_vendorarch}/auto/Readonly
%dir %{perl_vendorarch}/auto/Readonly/XS
%attr(755,root,root) %{perl_vendorarch}/auto/Readonly/XS/*.so
%{_mandir}/man3/*
