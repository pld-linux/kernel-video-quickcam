
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d"\\"" -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		_rel	1

Summary:        kernel module for Logitech QuickCam USB cameras
Name:		kernel-video-quickcam
Version:	cvs20020222
Release:	%{_rel}@%{_kernel_ver_str}
License:        nVidia
Vendor:         nVidia Corp.
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
URL:            http://qce-ga.sourceforge.net/
Source0:        http://download.sourceforge.net/qce-ga/qce-ga-%{version}.tar.gz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers >= 2.2.0 }
PreReq:		/sbin/depmod
PreReq:         modutils >= 2.3.18-2
%{!?_without_dist_kernel:Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}}
Exclusivearch:  %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Logitech QuickCam USB cameras driver

%description -l pl
Sterownik do kamer USB Logitech QuickCam

%prep
%setup -q -n quickcam

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video
install mod_quickcam.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/quickcam.o

gzip -9nf README

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a


%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/video/*
