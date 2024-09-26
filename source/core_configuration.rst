Setting Up the Open5GS Core
===========================

Install Dependencies
--------------------

1. **Update System Packages:**

   .. code-block:: bash

      sudo sed -i -e 's|disco|focal|g' /etc/apt/sources.list
      sudo apt update && sudo apt upgrade -y

2. **Install Required Packages:**

   .. code-block:: bash

      sudo apt install -y python3-pip python3-setuptools python3-wheel ninja-build build-essential \\
      flex bison git cmake libsctp-dev libgnutls28-dev libgcrypt-dev libssl-dev libidn11-dev \\
      libmongoc-dev libbson-dev libyaml-dev libnghttp2-dev libmicrohttpd-dev libcurl4-gnutls-dev \\
      libnghttp2-dev libtins-dev libtalloc-dev meson libtool libdw-dev binutils-dev libdwarf-dev \\
      doxygen libmbedtls-dev libfftw3-dev libgtest-dev libyaml-cpp-dev libsctp-dev \\
      libboost-program-options-dev libconfig++-dev ca-certificates curl

Install MongoDB
---------------

1. **Remove Existing MongoDB Installations:**

   .. code-block:: bash

      sudo apt-get purge -y mongodb-org*
      sudo rm -rf /var/log/mongodb
      sudo rm -rf /var/lib/mongodb
      sudo rm -f /etc/apt/sources.list.d/mongodb-org-6.0.list
      sudo rm -f /usr/share/keyrings/mongodb-server-6.0.gpg
      sudo apt-get purge -y mongo-tools mongodb-clients mongodb-server
      sudo apt-get autoremove -y
      sudo rm -rf /etc/apt/trusted.gpg.d/mongodb-*

2. **Install MongoDB 6.0:**

   .. code-block:: bash

      curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
      echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
      sudo apt update
      sudo apt install -y mongodb-org
      sudo systemctl start mongod
      sudo systemctl enable mongod

Set Up TUN Device
-----------------

1. **Configure TUN Interface:**

   .. code-block:: bash

      sudo ip tuntap add name ogstun mode tun
      sudo ip addr add 10.45.0.1/16 dev ogstun
      sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
      sudo ip link set ogstun up

Clone and Build Open5GS
-----------------------

1. **Clone Open5GS Repository:**

   .. code-block:: bash

      git clone https://github.com/open5gs/open5gs
      cd open5gs

2. **Compile Open5GS with Meson:**

   .. code-block:: bash

      meson build --prefix=`pwd`/install
      ninja -C build

3. **Run Test Programs:**

   .. code-block:: bash

      ./build/tests/registration/registration

4. **Install Open5GS:**

   .. code-block:: bash

      cd build
      sudo ninja install

Post-Installation Configuration
-------------------------------

**Perform the following steps whenever you restart your 5G Core VM:**

1. **Set CPU Performance Mode:**

   .. code-block:: bash

      echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor >/dev/null

2. **Adjust System Buffers:**

   .. code-block:: bash

      sudo sysctl -w net.core.wmem_max=33554432
      sudo sysctl -w net.core.rmem_max=33554432
      sudo sysctl -w net.core.wmem_default=33554432
      sudo sysctl -w net.core.rmem_default=33554432

3. **Set Up TUN Interface:**

   .. code-block:: bash

      sudo ip tuntap add name ogstun mode tun
      sudo ip addr add 10.45.0.1/16 dev ogstun
      sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
      sudo ip link set ogstun up

4. **Enable IP Forwarding:**

   .. code-block:: bash

      sudo sysctl -w net.ipv4.ip_forward=1
      sudo sysctl -w net.ipv6.conf.all.forwarding=1

5. **Configure NAT with iptables:**

   .. code-block:: bash

      sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
      sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE

Start Open5GS Core
------------------

1. **Navigate to Open5GS Test Applications:**

   .. code-block:: bash

      cd ~/open5gs/build/tests/app

2. **Run the 5G Core:**

   .. code-block:: bash

      sudo ./5gc

   - You should see logs indicating that the core network services are running.

Add UE to User Database
-----------------------

1. **Navigate to Database Scripts:**

   .. code-block:: bash

      cd ~/open5gs/misc/db

2. **Edit the User Registration Script:**

   - Open the `open5gs-dbctl` script or the appropriate script for adding subscribers.

3. **Add the srsUE Subscriber:**

   - Use the script to add a new subscriber with the `imsi`, `k`, `opc`, and other parameters matching your UE configuration.

Configure Open5GS Settings
--------------------------

1. **Edit Configuration File:**

   - Navigate to the configuration directory:

     .. code-block:: bash

        cd ~/open5gs/build/configs

   - Open the `sample.yaml` file:

     .. code-block:: bash

        sudo vi sample.yaml

2. **Update NGAP Server IP Address:**

   - Set the `ngap` server IP address to the machine IP address of your VM.

   - Example:

     .. code-block:: yaml

        amf:
          ngap:
            - addr: <CORE_VM_IP_ADDRESS>

3. **Save and Exit the Configuration File.**

