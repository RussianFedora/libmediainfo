Name:           libmediainfo
Version:        0.7.65
Release:        1%{?dist}
Summary:        Supplies technical and tag information about a video or audio file
Summary(ru):    Предоставляет полную информацию о видео или аудио файле

Group:          System Environment/Libraries
License:        BSD
URL:            http://mediainfo.sourceforge.net/
Source0:        http://downloads.sourceforge.net/mediainfo/%{name}_%{version}.tar.bz2

BuildRequires:  libzen-devel >= 0.4.29
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
BuildRequires:  doxygen
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libcurl-devel
BuildRequires:  tinyxml2-devel

%description
MediaInfo supplies technical and tag information about a video or
audio file.

What information can I get from MediaInfo?
* General: title, author, director, album, track number, date, duration...
* Video: codec, aspect, fps, bitrate...
* Audio: codec, sample rate, channels, language, bitrate...
* Text: language of subtitle
* Chapters: number of chapters, list of chapters

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
* Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
* Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
* Subtitles: SRT, SSA, ASS, SAMI

This package contains the shared library for MediaInfo.

%description -l ru
MediaInfo предоставляет полную информацию о видео или аудио файле.

Какая информация может быть получена MediaInfo?
* Общее: title, author, director, album, track number, date, duration...
* Видео: codec, aspect, fps, bitrate...
* Аудио: codec, sample rate, channels, language, bitrate...
* Текст: язык субтитров
* Части: число частей, список частей

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

Какой формат (контейнер) поддерживает MediaInfo?
* Видео: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
* Аудио: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
* Субтитры: SRT, SSA, ASS, SAMI

Данный пакет содержит разделяемую библиотеку для MediaInfo.

%package        devel
Summary:        Include files and mandatory libraries for development
Summary(ru):    Пакет с файлами для разработки %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libzen-devel%{?_isa} >= 0.4.29

%description    devel
Include files and mandatory libraries for development.

%description    devel -l ru
Файлы для разработки %{name}.

%prep
%setup -q -n MediaInfoLib
cp           Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv           History_DLL.txt History.txt
sed -i 's/.$//' *.txt Source/Example/* 

find . -type f -exec chmod 644 {} ';'

pushd Project/GNU/Library
    autoreconf -i
popd

rm -rf Project/MSCS20*
rm -rf Source/ThirdParty/tinyxml2

%build
pushd Source/Doc/
    doxygen -u Doxyfile
    doxygen Doxyfile
popd
cp Source/Doc/*.html ./

pushd Project/GNU/Library
    %configure --enable-shared --disable-static --with-libcurl --enable-visibility
    make %{?_smp_mflags}
popd

%install
pushd Project/GNU/Library/
    %make_install
popd

# MediaInfoDLL headers and MediaInfo-config
install -dm 755 %{buildroot}%{_includedir}/MediaInfo
install -m 644 Source/MediaInfo/MediaInfo.h %{buildroot}%{_includedir}/MediaInfo
install -m 644 Source/MediaInfo/MediaInfoList.h %{buildroot}%{_includedir}/MediaInfo
install -m 644 Source/MediaInfo/MediaInfo_Const.h %{buildroot}%{_includedir}/MediaInfo
install -m 644 Source/MediaInfo/MediaInfo_Events.h %{buildroot}%{_includedir}/MediaInfo
install -dm 755 %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.cs %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.h %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL_Static.h %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.JNA.java %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.JNative.java %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL.py %{buildroot}%{_includedir}/MediaInfoDLL
install -m 644 Source/MediaInfoDLL/MediaInfoDLL3.py %{buildroot}%{_includedir}/MediaInfoDLL

sed -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/libmediainfo.pc
install -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -m 644 Project/GNU/Library/libmediainfo.pc %{buildroot}%{_libdir}/pkgconfig

rm -f %{buildroot}%{_libdir}/%{name}.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc History.txt License.html ReadMe.txt
%{_libdir}/%{name}.so.*

%files    devel
%doc Changes.txt Documentation.html Doc Source/Example
%{_includedir}/MediaInfo
%{_includedir}/MediaInfoDLL
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 12 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.65-1
- Update to 0.7.65

* Sat Nov 02 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.64-4
- Some small corrections in spec

* Wed Jul 31 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.64-3
- Corrected make flags and use install macros

* Tue Jul 30 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.64-2
- just rebuild

* Fri Jul 12 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.64-1
- update to 0.7.64

* Fri May 31 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.63-1
- update to 0.7.63

* Tue Apr 23 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.62-2
- Removed dos2unix from BR
- Correcting encoding for all files
- Corrected config and build
- Enable curl support

* Wed Mar 20 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.62-1
- update to 0.7.62

* Tue Oct 23 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.61-1
- Update to 0.7.61

* Mon Sep 03 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.60-1
- Update to 0.7.60

* Tue Jun 05 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.58-1
- Update to 0.7.58

* Fri May 04 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.57-1
- Update to 0.7.57

* Wed Apr 11 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.56-1
- Update to 0.7.56

* Tue Mar 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.54-1
- Update to 0.7.54

* Thu Feb 09 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.53-1
- Update to 0.7.53

* Thu Dec 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.52-1
- Update to 0.7.52

* Tue Nov 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.51-2
- Added description in russian language

* Mon Nov 14 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.51-1
- Update to 0.7.51

* Tue Sep 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.50-1
- Update to 0.7.50

* Mon Sep 19 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.49-1
- Update to 0.7.49

* Fri Aug 19 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.48-1
- Update to 0.7.48

* Tue Aug 09 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.47-2
- Removed 0 from name

* Fri Aug 05 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.7.47-1
- Initial release
