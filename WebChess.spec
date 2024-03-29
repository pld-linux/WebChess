Summary:	A great persistant online chess game
Summary(pl.UTF-8):	Wspaniała internetowa gra w szachy
Name:		WebChess
Version:	0.9.0
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/webchess/%{name}_%{version}.zip
# Source0-md5:	e1a0dc90959a4e8475854a6e7fb4f0b9
Source1:	%{name}.conf
URL:		http://webchess.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	webserver
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webchessdir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
A great persistant online chess game using PHP/MySQL on the backend
and HTML/JavaScript on the front-end, which includes move validation,
CHECK checking, pawn promotion and undo. It also has a login system
which allows multiple simultaneous games.

%description -l pl.UTF-8
Wspaniała internetowa gra w szachy, używająca PHP/MySQL po stronie
backendu i HTML/JavaScript po stronie interfejsu użytkownika. Zawiera
kontrolę ruchów, sprawdzanie szachu, promocję pionów oraz cofanie. Ma
także system logowania, który pozwala na wiele jednoczesnych gier.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_webchessdir} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

cp -af images javascript *.php *.css chess.inc $RPM_BUILD_ROOT%{_webchessdir}
rm -f $RPM_BUILD_ROOT%{_webchessdir}/config.php

install config.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_webchessdir}/config.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
%service -q httpd reload

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		%service -q httpd reload
	fi
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%doc docs/*
%dir %{_webchessdir}
%{_webchessdir}/images
%{_webchessdir}/javascript
%{_webchessdir}/chess.inc
%{_webchessdir}/*.php
%{_webchessdir}/*.css
