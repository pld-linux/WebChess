Summary:	A great persistant online chess game
Summary(pl):	Wspania³a internetowa gra w szachy
Name:		WebChess
Version:	0.9.0
Release:	1
License:	GNU General Public License (GPL)
Group:		Webaplications
######		Unknown group!
Source0:	http://voxel.dl.sourceforge.net/sourceforge/webchess/%{name}_%{version}.zip
# Source0-md5:	e1a0dc90959a4e8475854a6e7fb4f0b9
Requires:	php-mysql
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webchessdir	/home/services/httpd/html/WebChess

%description
A great persistant online chess game using PHP/MySQL on the backend
and HTML/JavaScript on the front-end, which includes move validation,
CHECK checking, pawn promotion and undo. It also has a login system
which allows multiple simultaneous games.

%description -l pl
Wspania³a internetowa gra w szachy, oparta na PHP/MySQL i
HTML/JavaScript. Posiada wiele ciekawych funkcji oraz system
logowania, który zapewnia gre zespo³ow±

%prep
%setup -q -c %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_webchessdir}

cp -af images javascript *.php *.css chess.inc	  $RPM_BUILD_ROOT%{_webchessdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %{_webchessdir}
%{_webchessdir}/images/
%{_webchessdir}/javascript/
%{_webchessdir}/chess.inc
%{_webchessdir}/*.php
%{_webchessdir}/*.css
