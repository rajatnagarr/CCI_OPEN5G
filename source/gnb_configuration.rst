Configuring the gNB
===================

Prepare the gNB VM
------------------

1. **Configure Network Settings:**

   - Perform the same netplan configuration as done for the UE to ensure the gNB VM has a connection to the USRP.

2. **Update and Upgrade System Packages:**

   .. code-block:: bash

      sudo sed -i -e 's|disco|focal|g' /etc/apt/sources.list
      sudo apt update && sudo apt upgrade -y

3. **Install Required Packages:**

   .. code-block:: bash

      sudo apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev \\
      libyaml-cpp-dev libgtest-dev libdw-dev binutils-dev libdwarf-dev libelf-dev

Install UHD
-----------

1. **Clone UHD Repository:**

   .. code-block:: bash

      git clone https://github.com/EttusResearch/uhd.git

2. **Checkout Specific Version:**

   .. code-block:: bash

      cd uhd
      git checkout v3.15.0.0

3. **Build and Install UHD:**

   .. code-block:: bash

      cd host
      mkdir build
      cd build
      cmake ..
      make
      sudo make install
      sudo ldconfig

4. **Verify UHD Installation:**

   .. code-block:: bash

      uhd_find_devices

Install srsRAN gNB
------------------

1. **Clone srsRAN Project Repository:**

   .. code-block:: bash

      git clone https://github.com/srsran/srsRAN_Project.git

2. **Build and Install srsRAN:**

   .. code-block:: bash

      cd srsRAN_Project
      mkdir build
      cd build
      cmake ../
      make -j`nproc`
      sudo make install
      sudo ldconfig

Configure srsENB (gNB)
----------------------

1. **Navigate to Configuration Directory:**

   .. code-block:: bash

      cd ~/srsRAN_Project/configs

2. **Copy and Edit Configuration File:**

   - Create a copy of the existing `n310.conf` file for ease of use:

     .. code-block:: bash

        cp n310.conf my_gnb.conf

   - Open `my_gnb.conf` for editing:

     .. code-block:: bash

        sudo vi my_gnb.conf

3. **Update Configuration Settings:**

   - **AMF Settings:**

     - Set the `amf_addr` to the IP address of your Open5GS core VM.

   - **RU_SDR Settings:**

     - Adjust gain values to be greater than 0.

   - **Cell Configuration:**

     - Change the `cell_id`, `mcc`, and `mnc` to unique values to avoid conflicts.

4. **Adjust System Buffers:**

   .. code-block:: bash

      sudo sysctl -w net.core.rmem_max=24862979
      sudo sysctl -w net.core.wmem_max=24862979

5. **Save and Close the Configuration File.**

Start the gNB
-------------

1. **Run srsENB with the Custom Configuration:**

   .. code-block:: bash

      sudo srseNB --enb.config_file=~/srsRAN_Project/configs/my_gnb.conf

   - Monitor the logs to ensure the gNB starts successfully and connects to the Open5GS core.

