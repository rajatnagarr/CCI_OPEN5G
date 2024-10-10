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

2. **Add MongoDB Repository and Update:**

   - Add the MongoDB GPG key and repository:

     .. code-block:: bash

        curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
        echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
     - **Output:**

       .. image:: _static/image10.png
          :alt: Output of sudo apt update after adding MongoDB repository
          :align: center
          :width: 60%

     - Update the package list:

       .. code-block:: bash

          sudo apt update

3. **Install and Start MongoDB:**

   - Install MongoDB:

     .. code-block:: bash

        sudo apt install -y mongodb-org

   - Start and enable MongoDB service:

     .. code-block:: bash

        sudo systemctl start mongod
        sudo systemctl enable mongod

   - **Example Output:**

     .. image:: _static/image3.png
        :alt: Starting and enabling MongoDB service
        :align: center
        :width: 50%

     *Figure: Starting the MongoDB service.*

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

   - **Example Output:**

     .. image:: _static/image15.png
        :alt: Output of Open5GS test program
        :align: center
        :width: 60%

     *Figure: Running Open5GS test program to verify the build.*

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
      sudo iptables -I INPUT -i ogstun -j ACCEPT

   - **Example Output:**

     .. image:: _static/image17.png
        :alt: Configuring NAT with iptables
        :align: center
        :width: 80%

     *Figure: Configuring NAT rules using iptables.*

Start Open5GS Core
------------------

1. **Navigate to Open5GS Test Applications:**

   .. code-block:: bash

      cd ~/open5gs/build/tests/app

2. **Run the 5G Core:**

   .. code-block:: bash

      sudo ./5gc

   - **Example Output:**

     .. image:: _static/image28.png
        :alt: Output of running the Open5GS core
        :align: center
        :width: 80%

     *Figure: Open5GS core network services are running.*

Add UE to User Database
-----------------------

**Option 1: Using Database Scripts**

1. **Navigate to Database Scripts:**

   .. code-block:: bash

      cd ~/open5gs/misc/db

   - **Example:**

     .. image:: _static/image19.png
        :alt: Navigating to Open5GS database scripts directory
        :align: center
        :width: 50%

     *Figure: Navigating to the Open5GS database scripts directory.*

2. **Edit the User Registration Script:**

   - Open the `open5gs-dbctl` script or the appropriate script for adding subscribers.

3. **Add the srsUE Subscriber:**

   - Use the script to add a new subscriber with the `imsi`, `k`, `opc`, and other parameters matching your UE configuration.

**Option 2: Using the Open5GS WebUI**

1. **Install Prerequisites:**

   .. code-block:: bash

      sudo apt install -y ca-certificates curl gnupg
      sudo mkdir -p /etc/apt/keyrings
      curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
      NODE_MAJOR=20

   - **Example Output:**

     .. image:: _static/image5.png
        :alt: Installing Node.js prerequisites
        :align: center
        :width: 50%

     *Figure: Installing prerequisites for Node.js.*

2. **Add Node.js Repository and Install Node.js:**

   .. code-block:: bash

      echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
      sudo apt update
      sudo apt install -y nodejs

3. **Install Open5GS WebUI:**

   .. code-block:: bash

      curl -fsSL https://open5gs.org/open5gs/assets/webui/install | sudo -E bash -

   - **Output:**

     .. image:: _static/image13.png
        :alt: Installing Node.js
        :align: center
        :width: 60%

     *Figure: Adding Node.js repository and installing Node.js.*

4. **Start the WebUI:**

   - The WebUI should start automatically. If not, you can start it manually.

5. **Access the WebUI:**

   - Open a web browser and navigate to `http://localhost:3000`.

6. **Log In:**

   - Use the default credentials:

     - **Username:** admin
     - **Password:** 1423

7. **Add Subscriber Information:**

   - Navigate to the Subscriber menu.
   - Click the "+" button to add a new subscriber.
   - Fill in the required information:

     - **IMSI:** Must match the `imsi` in your UE configuration.
     - **Security Context:** Enter `K`, `OPc`, and `AMF` values matching your UE.
     - **APN:** Configure the Access Point Name as needed.

   - Click "SAVE" to add the subscriber.

   - **Example Screenshot:**

     .. image:: _static/image9.png
        :alt: Adding a subscriber in Open5GS WebUI
        :align: center
        :width: 60%

     *Figure: Adding a new subscriber in the Open5GS WebUI.*

   This process allows you to input subscriber details for your SIM cards, which will be stored in the Open5GS HSS (Home Subscriber Server) and UDR (Unified Data Repository) MongoDB database backend. If you're using test SIMs, the necessary details are usually printed on the card.

8. **Verify Subscriber Addition:**

   - Ensure the subscriber appears in the list with the correct details.

**Note:** Using the WebUI simplifies subscriber management and allows for easy modification of subscriber data.

Restart Open5GS Services
------------------------

After making changes to the configuration files or subscriber database, it's essential to restart the Open5GS services to apply the new settings.

1. **Restart Open5GS Daemons:**

   .. code-block:: bash

      sudo systemctl restart open5gs-amfd
      sudo systemctl restart open5gs-upfd

   - This ensures that the updated configurations take effect.

Configure Open5GS Settings
--------------------------

1. **Edit Configuration File:**

   - Navigate to the configuration directory:

     .. code-block:: bash

        cd ~/open5gs/build/configs

     - Edit the `sample.yaml` file:

       .. code-block:: bash

          sudo vi sample.yaml

       - **Example:**

         .. image:: _static/image26.png
            :alt: Editing the sample.yaml configuration file
            :align: center
            :width: 60%

         *Figure: Editing the Open5GS `sample.yaml` configuration file.*

2. **Update NGAP Server IP Address:**

   - Set the `ngap` server IP address to the machine IP address of your VM.

     - Example:

       .. code-block:: yaml

          amf:
            ngap:
              - addr: <CORE_VM_IP_ADDRESS>

3. **Save and Exit the Configuration File.**
