#
# conditional build
# _without_dist_kernel          without distribution kernel
#
Summary:        kernel module for Logitech QuickCam USB cameras
Summary(pl):	Modu� j�dra do kamer USB Logitech QuickCam
Name:		kernel-video-quickcam
Version:	0.40c
%define	_rel	4
Release:	%{_rel}@%{_kernel_ver_str}
License:        GPL
Group:		Base/Kernel
Source0:        http://download.sourceforge.net/qce-ga/qce-ga-%{version}.tar.gz
URL:            http://qce-ga.sourceforge.net/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers >= 2.2.0 }
PreReq:		/sbin/depmod
PreReq:         modutils >= 2.3.18-2
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Logitech QuickCam USB cameras driver.

%description -l pl
Sterownik do kamer USB Logitech QuickCam.

%package -n kernel-smp-video-quickcam
Summary:        kernel module for Logitech QuickCam USB cameras
Summary(pl):    Modu� j�dra do kamer USB Logitech QuickCam
Release:        %{_rel}@%{_kernel_ver_str}
Group:          Base/Kernel
PreReq:         /sbin/depmod
PreReq:         modutils >= 2.3.18-2
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-video-quickcam
Logitech QuickCam USB cameras driver for SMP kernel.

%description -n kernel-smp-video-quickcam -l pl
Sterownik do kamer USB Logitech QuickCam dla j�dra SMP.

%prep
%setup -q -n qce-ga-%{version}

%build

#%{__make}
#cd testquickcam
#%{__make}

%{__make} \
        CC=%{kgcc} \
        INCLUDES="%{rpmcflags} -I. -D__KERNEL_SMP=1 -D__SMP__ -I%{_kernelsrcdir}/include"
mv -f mod_quickcam.o  quickcam-smp.o
#%{__make} clean
%{__make} \
        CC=%{kgcc} \
        INCLUDES="%{rpmcflags} -I.  -I%{_kernelsrcdir}/include"
mv -f mod_quickcam.o quickcam.o

cd testquickcam 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

#install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video
install -D quickcam-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/quickcam-smp.o
install -D quickcam.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/quickcam.o

install -d $RPM_BUILD_ROOT/usr/sbin
install testquickcam/testquickcam $RPM_BUILD_ROOT/usr/sbin

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-video-quickcam
/sbin/depmod -a

%postun -n kernel-smp-video-quickcam
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}/video/*
%attr(755,root,users) /usr/sbin/testquickcam

%files -n kernel-smp-video-quickcam
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}smp/video/*
%attr(755,root,users) /usr/sbin/testquickcam
