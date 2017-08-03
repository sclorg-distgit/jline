%{?scl:%scl_package jline}
%{!?scl:%global pkg_name %{name}}

Name:             %{?scl_prefix}jline
Version:          2.13
Release:          9.2%{?dist}
Summary:          JLine is a Java library for handling console input
License:          BSD
URL:              https://github.com/jline/jline2
BuildArch:        noarch

# git clone git://github.com/jline/jline2.git
# cd jline2/ && git archive --format=tar --prefix=jline-2.13/ jline-2.13 | xz > jline-2.13.tar.xz
Source0:          jline-%{version}.tar.xz

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.easymock:easymock)
BuildRequires:  %{?scl_prefix}mvn(org.fusesource.jansi:jansi)
BuildRequires:  %{?scl_prefix}mvn(org.powermock:powermock-api-easymock)
BuildRequires:  %{?scl_prefix}mvn(org.powermock:powermock-module-junit4)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.oss:oss-parent:pom:)

Provides: %{?scl_prefix}jline2 = %{version}-%{release}

%description
JLine is a Java library for handling console input. It is similar
in functionality to BSD editline and GNU readline. People familiar
with the readline/editline capabilities for modern shells (such as
bash and tcsh) will find most of the command editing features of
JLine to be familiar.

%package javadoc
Summary:          Javadocs for %{pkg_name}
Provides: %{?scl_prefix}jline2-javadoc = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n jline-%{version}

# Remove maven-shade-plugin usage
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
# Remove animal sniffer plugin in order to reduce deps
%pom_remove_plugin "org.codehaus.mojo:animal-sniffer-maven-plugin"

# Remove unavailable and unneeded deps
%pom_xpath_remove "pom:build/pom:extensions"
%pom_remove_plugin :maven-site-plugin

# Do not import non-existing internal package
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Import-Package"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions" "<Import-Package>javax.swing;resolution:=optional,org.fusesource.jansi,!org.fusesource.jansi.internal</Import-Package>"

# Be sure to export jline.internal, but not org.fusesource.jansi.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1317551
%pom_xpath_set "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Export-Package" "jline.*;-noimport:=true"

# For some reason these directories do not exist, failing compilation due to -Werror
mkdir -p target/generated-sources/annotations
mkdir -p target/generated-test-sources/test-annotations

# nondeterministic
find -name TerminalFactoryTest.java -delete

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 2.13-9.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 2.13-9.1
- Automated package import and SCL-ization

* Thu Feb 16 2017 Michael Simacek <msimacek@redhat.com> - 2.13-9
- Correct license tag to just BSD

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 2.13-7
- Remove BR on site-plugin

* Wed Jun 22 2016 Michael Simacek <msimacek@redhat.com> - 2.13-6
- Remove nondeterministic test

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.13-5
- Regenerate build-requires

* Thu May 05 2016 Michael Simacek <msimacek@redhat.com> - 2.13-4
- Try to eliminate test nondeterminism

* Mon Mar 14 2016 Severin Gehwolf <sgehwolf@redhat.com> - 2.13-3
- OSGi export jline.internal. Resolves RHBZ#1317551.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Severin Gehwolf <sgehwolf@redhat.com> - 2.13-1
- Update to upstream 2.13 release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Alexander Kurtakov <akurtako@redhat.com> 2.12.1-1
- Update to upstream 2.12.1 release.

* Mon Jan 26 2015 Mat Booth <mat.booth@redhat.com> - 2.10-15
- Fix FTBFS due to missing BR on site-plugin
- Fix directory ownership
- Fix bogus date in changelog

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-13
- Migrate BuildRequires from junit4 to junit

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-12
- Remove BuildRequires on maven-surefire-provider-junit4

* Tue Mar 11 2014 Michael Simacek <msimacek@redhat.com> - 2.10-11
- Drop manual requires

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.10-10
- Use Requires: java-headless rebuild (#1067528)

* Tue Oct 29 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.10-9
- Package jline 2.x as jline. Resolves RHBZ#1022915.
- Part of a large effort to make jline1 a compat package rather than jline2.
  See RHBZ#1022897.
- Switch to xmvn.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 1 2012 Alexander Kurtakov <akurtako@redhat.com> 1.0-1
- Update to 1.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.94-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Alexander Kurtakov <akurtako@redhat.com> 0.9.94-6
- Build with maven 3.x.

* Sat Oct 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.9.94-5
- BuildRequire maven2.

* Sat Oct 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.9.94-4
- Patch delete to actually behave as delete instead of backspace, include
  keybindings.properties in docs (#720170).
- Drop executable bit from jar.
- Crosslink with local javadocs.
- Include LICENSE.txt in -javadoc.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 18 2010 Mat Booth <fedora@matbooth.co.uk> - 0.9.94-2
- Remove pre-built Windows-only binary artifacts.
- Demo package was defined but never built for some reason.
- Don't also package jar in the javadoc package!
- Drop versioned java and javadocs.

* Sat Dec 18 2010 Mat Booth <fedora@matbooth.co.uk> - 0.9.94-1
- Remove bundled jars in %%prep phase.
- Tidy up spec file, fix some rpmlint warnings.
- Add pom and depmaps.

* Mon Mar  8 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:0.9.94-0.6
- Added missing Requires: jpackage-utils (%%{_javadir} and %%{_javadocdir})

* Tue Jan 12 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.9.94-0.5
- Fix BRs.
- Drop gcj_support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.94-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.94-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:9.94-0.2
- drop repotag

* Mon Mar 24 2008 Matt Wringe <mwringe@redhat.com> - 0:9.94-0jpp.1
- Update to 0.9.94 (BZ #436204)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:0.9.9-2jpp.1
- Autorebuild for GCC 4.3

* Tue Mar 06 2007 Matt Wringe <mwringe@redhat.com> - 0:0.9.9-1jpp.1
- Add option to build with ant.
- Fix various rpmlint issues
- Specify proper license

* Thu May 04 2006 Alexander Kurtakov <akurtkov at gmail.com> - 0:0.9.9-1jpp
- Upgrade to 0.9.9

* Thu May 04 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.9.5-1jpp
- Upgrade to 0.9.5
- First JPP-1.7 release

* Mon Apr 25 2005 Fernando Nasser <fnasser@redhat.com> - 0:0.9.1-1jpp
- Upgrade to 0.9.1
- Disable attempt to include external jars

* Mon Apr 25 2005 Fernando Nasser <fnasser@redhat.com> - 0:0.8.1-3jpp
- Changes to use locally installed DTDs
- Do not try and access sun site for linking javadoc

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:0.8.1-2jpp
- Rebuild with ant-1.6.2

* Mon Jan 26 2004 David Walluck <david@anti-microsoft.org> 0:0.8.1-1jpp
- release
