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

   - **Example Output:**

     .. image:: _static/image25.png
        :alt: Output of uhd_find_devices command on gNB VM
        :align: center
        :width: 50%

     *Figure: Output showing the connected USRP devices on the gNB VM.*

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

   - Use the provided configuration files for the appropriate USRP model.

   - For example, if you are using the X310 USRP, copy and edit the `gnb_rf_x310_fdd_n3_20mhz.yml` file:

     .. code-block:: bash

        cp gnb_rf_x310_fdd_n3_20mhz.yml my_gnb.yml
    - **Example:**

       .. image:: _static/image21.png
          :alt: Editing the my_gnb.yml configuration file
          :align: center
          :width: 80%

     - Open `my_gnb.yml` for editing:

       .. code-block:: bash

          sudo vi x310.yml

     - **Example:**

       .. image:: _static/image27.png
          :alt: Editing the my_gnb.yml configuration file
          :align: center
          :width: 80%

       *Figure: Editing the gNB configuration file `my_gnb.yml`.*

3. **Update Configuration Settings:**

   - **AMF Settings:**

     - Set the `amf_addr` to the IP address of your Open5GS core VM.

   - **RU_SDR Settings:**

     - Adjust gain values to be greater than 0.

   - **Cell Configuration:**

     - Change the `cell_id`, `mcc`, and `mnc` to unique values to avoid conflicts with other users.

       **Note:** Using unique identifiers prevents interference and conflicts, especially if multiple users are conducting experiments simultaneously.

4. **Adjust System Buffers:**

   .. code-block:: bash

      sudo sysctl -w net.core.rmem_max=24862979
      sudo sysctl -w net.core.wmem_max=24862979

5. **Save and Close the Configuration File.**

Start the gNB
-------------

1. **Run srsENB with the Custom Configuration:**

   .. code-block:: bash

      sudo srseNB --enb.config_file=~/srsRAN_Project/configs/my_gnb.yml

   - Monitor the logs to ensure the gNB starts successfully and connects to the Open5GS core.

**Note:** Ensure that the Open5GS core is running before starting the gNB.

Verify Connectivity
-------------------

- **Ping Test:**

  - From the gNB VM, ping the Open5GS core to verify network connectivity.

    .. code-block:: bash

       ping <CORE_VM_IP_ADDRESS>

- **Check Logs:**

  - Monitor the gNB logs for successful connection messages to the AMF.

**Additional Tips:**

- **Read Official Documentation:**

  - Refer to the srsRAN and Open5GS official documentation to ensure configurations are correct.

- **Avoid Common Mistakes:**

  - Double-check IP addresses, port settings, and configuration parameters to prevent common errors.

