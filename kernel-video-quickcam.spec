#
# conditional build
# _without_dist_kernel          without distribution kernel
#
Summary:	Kernel module for Logitech QuickCam USB cameras
Summary(pl):	Modu³ j±dra do kamer USB Logitech QuickCam
Name:		kernel-video-quickcam
Version:	0.40c
%define	_rel	5
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://download.sourceforge.net/qce-ga/qce-ga-%{version}.tar.gz
URL:		http://qce-ga.sourceforge.net/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers >= 2.2.0 }
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires(post,postun):	modutils >= 2.3.18-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Logitech QuickCam USB cameras driver.

%description -l pl
Sterownik do kamer USB Logitech QuickCam.

%package -n kernel-smp-video-quickcam
Summary:	SMP kernel module for Logitech QuickCam USB cameras
Summary(pl):	Modu³ j±dra SMP do kamer USB Logitech QuickCam
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires(post,postun):	modutils >= 2.3.18-2

%description -n kernel-smp-video-quickcam
Logitech QuickCam USB cameras driver for SMP kernel.

%description -n kernel-smp-video-quickcam -l pl
Sterownik do kamer USB Logitech QuickCam dla j±dra SMP.

%package -n qce-qa
Summary:        Documentation and test program to Logitech QuickCam USB 
Summary(pl):    Dokumentacja i program testuj±cy do kamer Logitech QuickCam USB
Release:        %{_rel}
Group:          Base/Kernel
Requires:       %{name} = %{version}

%description -n qce-qa
Documentation and test program to Logitech QuickCam USB.

%description -n qce-qa -l pl
Dokumentacja i program testuj±cy do kamer Logitech QuickCam USB.

%prep
%setup -q -n qce-ga-%{version}

%build
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
install -D quickcam-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/quickcam.o
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
/lib/modules/%{_kernel_ver}/video/*

%files -n kernel-smp-video-quickcam
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/video/*

%files -n qce-qa
%defattr(644,root,root,755)
%doc README
%attr(755,root,users) /usr/sbin/testquickcam
