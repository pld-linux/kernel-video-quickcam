# $Revision 1.8  2002/08/11 08:34:40 $

# conditional build
# _without_dist_kernel          without distribution kernel

%define		_rel	1

Summary:        kernel module for Logitech QuickCam USB cameras
Summary(pl):	Modu³ j±dra do kamer USB Logitech QuickCam
Name:		kernel-video-quickcam
Version:	0.40c
Release:	%{_rel}@%{_kernel_ver_str}
License:        GPL
Group:		Base/Kernel
Source0:        http://download.sourceforge.net/qce-ga/qce-ga-%{version}.tar.gz
URL:            http://qce-ga.sourceforge.net/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers >= 2.4.0 }
PreReq:		/sbin/depmod
PreReq:         modutils >= 2.3.18-2
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Logitech QuickCam USB cameras driver.

%description -l pl
Sterownik do kamer USB Logitech QuickCam.

%prep
%setup -q -n qce-ga-%{version}

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
