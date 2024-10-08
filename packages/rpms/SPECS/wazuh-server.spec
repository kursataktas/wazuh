%if %{_debugenabled} == yes
  %global _enable_debug_package 0
  %global debug_package %{nil}
  %global __os_install_post %{nil}
  %define __strip /bin/true
%endif

%if %{_isstage} == no
  %define _rpmfilename %%{NAME}_%%{VERSION}-%%{RELEASE}_%%{ARCH}_%{_hashcommit}.rpm
%else
  %define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%endif

Summary:     Wazuh helps you to gain security visibility into your infrastructure by monitoring hosts at an operating system and application level. It provides the following capabilities: log analysis, file integrity monitoring, intrusions detection and policy and compliance monitoring
Name:        wazuh-server
Version:     %{_version}
Release:     %{_release}
License:     GPL
Group:       System Environment/Daemons
Source0:     %{name}-%{version}.tar.gz
URL:         https://www.wazuh.com/
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:      Wazuh, Inc <info@wazuh.com>
Packager:    Wazuh, Inc <info@wazuh.com>
Requires(pre):    /usr/sbin/groupadd /usr/sbin/useradd
Requires(postun): /usr/sbin/groupdel /usr/sbin/userdel
AutoReqProv: no

Requires: coreutils
BuildRequires: coreutils glibc-devel automake autoconf libtool policycoreutils-python curl perl

ExclusiveOS: linux

%define _source_payload w9.xzdio
%define _binary_payload w9.xzdio
%define _unpackaged_files_terminate_build 0

%description
Wazuh helps you to gain security visibility into your infrastructure by monitoring
hosts at an operating system and application level. It provides the following capabilities:
log analysis, file integrity monitoring, intrusions detection and policy and compliance monitoring

# Don't generate build_id links to prevent conflicts with other
# packages.
%global _build_id_links none

%prep
%setup -q
%build
%install
# Clean BUILDROOT
rm -fr %{buildroot}
echo 'VCPKG_ROOT="/root/vcpkg"' > ./etc/preloaded-vars.conf
echo 'USER_LANGUAGE="en"' > ./etc/preloaded-vars.conf
echo 'USER_NO_STOP="y"' >> ./etc/preloaded-vars.conf
echo 'USER_INSTALL_TYPE="server"' >> ./etc/preloaded-vars.conf
echo 'USER_DIR="%{_localstatedir}"' >> ./etc/preloaded-vars.conf
echo 'USER_DELETE_DIR="y"' >> ./etc/preloaded-vars.conf
echo 'USER_UPDATE="n"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_EMAIL="n"' >> ./etc/preloaded-vars.conf
echo 'USER_WHITE_LIST="n"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_SYSLOG="y"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_AUTHD="y"' >> ./etc/preloaded-vars.conf
echo 'USER_SERVER_IP="MANAGER_IP"' >> ./etc/preloaded-vars.conf
echo 'USER_CA_STORE="/path/to/my_cert.pem"' >> ./etc/preloaded-vars.conf
echo 'USER_GENERATE_AUTHD_CERT="y"' >> ./etc/preloaded-vars.conf
echo 'USER_AUTO_START="n"' >> ./etc/preloaded-vars.conf
echo 'USER_CREATE_SSL_CERT="n"' >> ./etc/preloaded-vars.conf
echo 'DOWNLOAD_CONTENT="y"' >> ./etc/preloaded-vars.conf
export VCPKG_ROOT="/root/vcpkg"
export PATH="${PATH}:${VCPKG_ROOT}"
scl enable devtoolset-11 ./install.sh

# Create directories
#mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}.ssh

# Copy the installed files into RPM_BUILD_ROOT directory
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}tmp/
cp -pr %{_localstatedir}tmp/wazuh-server ${RPM_BUILD_ROOT}%{_localstatedir}tmp/
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin
cp -p %{_localstatedir}usr/bin/wazuh-engine ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin/
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}run/wazuh-server
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}var/lib/wazuh-server


#sed -i "s:WAZUH_HOME_TMP:%{_localstatedir}:g" src/init/templates/ossec-hids-rh.init
#install -m 0755 src/init/templates/ossec-hids-rh.init ${RPM_BUILD_ROOT}%{_initrddir}/wazuh-server

#mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/
#sed -i "s:WAZUH_HOME_TMP:%{_localstatedir}:g" src/init/templates/wazuh-server.service
#install -m 0644 src/init/templates/wazuh-server.service ${RPM_BUILD_ROOT}/usr/lib/systemd/system/

# Add configuration scripts
# mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/
# cp gen_ossec.sh ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/
# cp add_localfiles.sh ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/

# Templates for initscript
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/src/init
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/etc/templates/config/generic
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/etc/templates/config/centos
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/etc/templates/config/rhel
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/etc/templates/config/suse
#mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/etc/templates/config/sles

# install -m 0640 src/init/*.sh ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/src/init

# Add installation scripts
# cp src/VERSION ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/src/
# cp src/REVISION ${RPM_BUILD_ROOT}%{_localstatedir}/packages_files/manager_installation_scripts/src/

exit 0

%pre

# Create the wazuh group if it doesn't exists
if command -v getent > /dev/null 2>&1 && ! getent group wazuh > /dev/null 2>&1; then
  groupadd -r wazuh
elif ! getent group wazuh > /dev/null 2>&1; then
  groupadd -r wazuh
fi

# Create the wazuh user if it doesn't exists
if ! getent passwd wazuh > /dev/null 2>&1; then
  useradd -g wazuh -G wazuh -d %{_localstatedir} -r -s /sbin/nologin wazuh
fi

# Stop the services to upgrade the package
if [ $1 = 2 ]; then
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 && systemctl is-active --quiet wazuh-server > /dev/null 2>&1; then
    systemctl stop wazuh-server.service > /dev/null 2>&1
    touch %{_localstatedir}/tmp/wazuh.restart
  # Check for SysV
  elif command -v service > /dev/null 2>&1 && service wazuh-server status 2>/dev/null | grep "is running" > /dev/null 2>&1; then
    service wazuh-server stop > /dev/null 2>&1
    touch %{_localstatedir}/tmp/wazuh.restart
  fi

fi

%post

%define _vdfilename vd_1.0.0_vd_4.10.0.tar.xz

# Fresh install code block
if [ $1 = 1 ]; then
  . %{_localstatedir}/packages_files/manager_installation_scripts/src/init/dist-detect.sh
fi

if [[ -d /run/systemd/system ]]; then
  rm -f %{_initrddir}/wazuh-server
fi

# CentOS
if [ -r "/etc/centos-release" ]; then
  if grep -q "AlmaLinux" /etc/centos-release; then
    DIST_NAME=almalinux
  elif grep -q "Rocky" /etc/centos-release; then
    DIST_NAME=almalinux
  else
    DIST_NAME="centos"
  fi
  DIST_VER=`sed -rn 's/.* ([0-9]{1,2})\.*[0-9]{0,2}.*/\1/p' /etc/centos-release`
# RedHat
elif [ -r "/etc/redhat-release" ]; then
  if grep -q "AlmaLinux" /etc/redhat-release; then
    DIST_NAME=almalinux
  elif grep -q "Rocky" /etc/redhat-release; then
    DIST_NAME=almalinux
  elif grep -q "CentOS" /etc/redhat-release; then
      DIST_NAME="centos"
  else
      DIST_NAME="rhel"
  fi
  DIST_VER=`sed -rn 's/.* ([0-9]{1,2})\.*[0-9]{0,2}.*/\1/p' /etc/redhat-release`
elif [ -r "/etc/os-release" ]; then
  . /etc/os-release
  DIST_NAME=$ID
  DIST_VER=$(echo $VERSION_ID | sed -rn 's/[^0-9]*([0-9]+).*/\1/p')
  if [ "X$DIST_VER" = "X" ]; then
      DIST_VER="0"
  fi
  if [ "$DIST_NAME" = "amzn" ] && [ "$DIST_VER" != "2" ] && [ "$DIST_VER" != "2023" ]; then
      DIST_VER="1"
  fi
  DIST_SUBVER=$(echo $VERSION_ID | sed -rn 's/[^0-9]*[0-9]+\.([0-9]+).*/\1/p')
  if [ "X$DIST_SUBVER" = "X" ]; then
      DIST_SUBVER="0"
  fi
else
  DIST_NAME="generic"
  DIST_VER=""
fi

# Delete the installation files used to configure the manager
rm -rf %{_localstatedir}/packages_files

# Remove unnecessary files from default group
rm -f %{_localstatedir}/etc/shared/default/*.rpmnew

# Remove old ossec user and group if exists and change ownwership of files

if getent group ossec > /dev/null 2>&1; then
  find %{_localstatedir}/ -group ossec -user root -print0 | xargs -0 chown root:wazuh > /dev/null 2>&1 || true
  if getent passwd ossec > /dev/null 2>&1; then
    find %{_localstatedir}/ -group ossec -user ossec -print0 | xargs -0 chown wazuh:wazuh > /dev/null 2>&1 || true
    userdel ossec > /dev/null 2>&1
  fi
  if getent passwd ossecm > /dev/null 2>&1; then
    find %{_localstatedir}/ -group ossec -user ossecm -print0 | xargs -0 chown wazuh:wazuh > /dev/null 2>&1 || true
    userdel ossecm > /dev/null 2>&1
  fi
  if getent passwd ossecr > /dev/null 2>&1; then
    find %{_localstatedir}/ -group ossec -user ossecr -print0 | xargs -0 chown wazuh:wazuh > /dev/null 2>&1 || true
    userdel ossecr > /dev/null 2>&1
  fi
  if getent group ossec > /dev/null 2>&1; then
    groupdel ossec > /dev/null 2>&1
  fi
fi

%preun

if [ $1 = 0 ]; then

  # Stop the services before uninstall the package
  # Check for systemd
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 && systemctl is-active --quiet wazuh-server > /dev/null 2>&1; then
    systemctl stop wazuh-server.service > /dev/null 2>&1
  # Check for SysV
  elif command -v service > /dev/null 2>&1 && service wazuh-server status 2>/dev/null | grep "is running" > /dev/null 2>&1; then
    service wazuh-server stop > /dev/null 2>&1
  fi
fi

%postun

# If the package is been uninstalled
if [ $1 = 0 ];then
  # Remove the wazuh user if it exists
  if getent passwd wazuh > /dev/null 2>&1; then
    userdel wazuh >/dev/null 2>&1
  fi
  # Remove the wazuh group if it exists
  if command -v getent > /dev/null 2>&1 && getent group wazuh > /dev/null 2>&1; then
    groupdel wazuh >/dev/null 2>&1
  elif getent group wazuh > /dev/null 2>&1; then
    groupdel wazuh >/dev/null 2>&1
  fi

  # Remove lingering folders and files
  rm -rf %{_localstatedir}tmp/wazuh-server
  rm -rf %{_localstatedir}usr/bin/wazuh-engine
  rm -rf %{_localstatedir}run/wazuh-server
  rm -rf %{_localstatedir}var/lib/wazuh-server
fi

# posttrans code is the last thing executed in a install/upgrade
%posttrans
if [ -f %{_sysconfdir}/systemd/system/wazuh-server.service ]; then
  rm -rf %{_sysconfdir}/systemd/system/wazuh-server.service
  systemctl daemon-reload > /dev/null 2>&1
fi

if [ -f %{_localstatedir}/tmp/wazuh.restart ]; then
  rm -f %{_localstatedir}/tmp/wazuh.restart
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 ; then
    systemctl daemon-reload > /dev/null 2>&1
    systemctl restart wazuh-server.service > /dev/null 2>&1
  else command -v service > /dev/null 2>&1 ; then
    service wazuh-server restart > /dev/null 2>&1
  fi
fi

# Remove groups backup files
rm -rf %{_localstatedir}/backup/groups

%triggerin -- glibc

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,wazuh)
%dir %attr(750, root, wazuh) %{_localstatedir}run/wazuh-server
%dir %attr(750, root, wazuh) %{_localstatedir}var/lib/wazuh-server
%attr(750, root, wazuh) %{_localstatedir}usr/bin/wazuh-engine
%attr(640, root, wazuh) %{_localstatedir}tmp/wazuh-server/vd_1.0.0_vd_4.10.0.tar.xz

#%config(missingok) %{_initrddir}/wazuh-server
#%attr(640, root, wazuh) %verify(not md5 size mtime) %ghost %{_sysconfdir}/ossec-init.conf
#/usr/lib/systemd/system/wazuh-server.service
#%dir %attr(750, root, wazuh) %{_localstatedir}
#%dir %attr(750, root, wazuh) %{_localstatedir}/api
#%dir %attr(770, root, wazuh) %{_localstatedir}/api/configuration
#%attr(660, root, wazuh) %config(noreplace) %{_localstatedir}/api/configuration/api.yaml
#%dir %attr(770, root, wazuh) %{_localstatedir}/api/configuration/security
#%dir %attr(770, root, wazuh) %{_localstatedir}/api/configuration/ssl
#%dir %attr(750, root, wazuh) %{_localstatedir}/api/scripts
#%attr(640, root, wazuh) %{_localstatedir}/api/scripts/*.py
#%dir %attr(750, root, wazuh) %{_localstatedir}/bin
#%attr(750, root, wazuh) %{_localstatedir}/bin/wazuh-apid
#%attr(750, root, wazuh) %{_localstatedir}/bin/wazuh-clusterd
#%attr(750, root, wazuh) %{_localstatedir}/bin/rbac_control
#%attr(660, wazuh, wazuh) %config(noreplace) %{_localstatedir}/etc/shared/default/*
#%dir %attr(770, root, wazuh) %{_localstatedir}/etc/rootcheck
#%attr(660, root, wazuh) %{_localstatedir}/etc/rootcheck/*.txt
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework/python
#%{_localstatedir}/framework/python/*
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework/scripts
#%attr(640, root, wazuh) %{_localstatedir}/framework/scripts/*.py
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework/wazuh
#%attr(640, root, wazuh) %{_localstatedir}/framework/wazuh/*.py
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster
#%attr(640, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster/*.py
#%attr(640, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster/*.json
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster/hap_helper
#%attr(640, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster/hap_helper/*.py
#%dir %attr(750, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster/dapi
#%attr(640, root, wazuh) %{_localstatedir}/framework/wazuh/core/cluster/dapi/*.py
#%dir %attr(750, root, wazuh) %{_localstatedir}/lib
#%{_localstatedir}/lib/libpython3.10.so.1.0
#%attr(750, root, root) %config(missingok) %{_localstatedir}/packages_files/manager_installation_scripts/src/REVISION
#%attr(750, root, root) %config(missingok) %{_localstatedir}/packages_files/manager_installation_scripts/src/VERSION
#%dir %attr(750, root, root) %config(missingok) %{_localstatedir}/packages_files/manager_installation_scripts/src/init/
#%attr(750, root, root) %config(missingok) %{_localstatedir}/packages_files/manager_installation_scripts/src/init/*
#%attr(750, wazuh, wazuh) %config(missingok) %{_localstatedir}/tmp/%{_vdfilename}
#%dir %attr(750, root, wazuh) %{_localstatedir}/ruleset
#%dir %attr(1770, root, wazuh) %{_localstatedir}/tmp
#%dir %attr(750, root, wazuh) %{_localstatedir}/var

%changelog
* Mon Jun 2 2025 support <info@wazuh.com> - 5.0.0
- More info: https://documentation.wazuh.com/current/release-notes/release-5-0-0.html
