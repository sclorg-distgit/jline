%{?scl:%scl_package jline}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

%if 0%{?rhel}

%if 0%{?rhel} <= 6
  # EL 6
  %global custom_release 60
%else
  # EL 7
  %global custom_release 70
%endif

%else

%global custom_release 1

%endif

Name:             %{?scl_prefix}jline
Version:          2.13
# Release should be higher than el6 builds. Use convention
# 60.X where X is an increasing int. 60 for rhel-6. We use
# 70.X for rhel-7. For some reason we cannot rely on the
# dist tag.
Release:          %{custom_release}.1%{?dist}
Summary:          JLine is a Java library for handling console input
Group:            Development/Libraries
License:          BSD and ASL 2.0
URL:              https://github.com/jline/jline2

# git clone git://github.com/jline/jline2.git
# cd jline2/ && git archive --format=tar --prefix=jline-2.13/ jline-2.13 | xz > jline-2.13.tar.xz
Source0:          jline-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    %{?scl_prefix_maven}maven-local
BuildRequires:    %{?scl_prefix_maven}maven-compiler-plugin
BuildRequires:    %{?scl_prefix_maven}maven-jar-plugin
BuildRequires:    %{?scl_prefix_maven}maven-surefire-plugin
BuildRequires:    %{?scl_prefix_maven}maven-install-plugin
BuildRequires:    %{?scl_prefix_java_common}junit
%if 0%{?fedora} >= 23
BuildRequires:    %{?scl_prefix_java_common}powermock-junit4
BuildRequires:    %{?scl_prefix_java_common}easymock
BuildRequires:    %{?scl_prefix_java_common}powermock-api-easymock
%endif
BuildRequires:    %{?scl_prefix_java_common}jansi
BuildRequires:    %{?scl_prefix_maven}fusesource-pom
BuildRequires:    %{?scl_prefix_maven}maven-surefire-provider-junit

%description
JLine is a Java library for handling console input. It is similar
in functionality to BSD editline and GNU readline. People familiar
with the readline/editline capabilities for modern shells (such as
bash and tcsh) will find most of the command editing features of
JLine to be familiar.

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n jline-%{version}

# Remove maven-shade-plugin usage
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
# Remove animal sniffer plugin in order to reduce deps
%pom_remove_plugin "org.codehaus.mojo:animal-sniffer-maven-plugin"

# Remove unavailable and unneeded deps
%pom_xpath_remove "pom:build/pom:extensions"
%pom_xpath_remove "pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId = 'maven-site-plugin']"
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-site-plugin']"
%pom_xpath_remove "pom:distributionManagement"
%pom_xpath_remove "pom:profiles/pom:profile[pom:id = 'site-stage']"

# Do not import non-existing internal package
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Import-Package"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions" "<Import-Package>javax.swing;resolution:=optional,!org.fusesource.jansi.internal</Import-Package>"

# Let maven bundle plugin figure out the exports.
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Export-Package"
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%if 0%{?fedora} >= 23
%mvn_build
%else
%mvn_build -f
%endif
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc CHANGELOG.md README.md LICENSE.txt
%dir %{_javadir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Jun 23 2016 Severin Gehwolf <sgehwolf@redhat.com> 2.13-1
- Initial package.
