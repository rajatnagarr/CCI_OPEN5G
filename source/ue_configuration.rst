Configuring the UE
==================

Install Dependencies
--------------------

1. **Update Package Lists:**

   .. code-block:: bash

      sudo apt update

   **Note:** If you encounter issues with `sudo apt update`, run:

   .. code-block:: bash

      sudo sed -i -e 's|disco|focal|g' /etc/apt/sources.list
      sudo apt update

2. **Install Required Packages:**

   .. code-block:: bash

      sudo apt install -y cmake git libboost-all-dev libusb-1.0-0-dev libudev-dev libncurses5-dev libuhd-dev uhd-host

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

     .. image:: _static/image29.png
        :alt: Output of uhd_find_devices command
        :align: center
        :width: 80%

     *Figure: Output showing the connected USRP devices.*

Install srsRAN 4G Suite
-----------------------

1. **Clone srsRAN Repository:**

   .. code-block:: bash

      git clone https://github.com/srsran/srsRAN_4G.git

2. **Build and Install srsRAN:**

   .. code-block:: bash

      cd srsRAN_4G
      mkdir build
      cd build

      # If you encounter compiler issues:
      sudo apt install gcc-10 g++-10
      export CC=$(which gcc-10)
      export CXX=$(which g++-10)

      cmake .. -DCMAKE_BUILD_TYPE=Release
      make -j$(nproc)
      sudo make install
      sudo ldconfig

Configure srsUE
---------------

1. **Install Configuration Files:**

   .. code-block:: bash

      sudo srsran_install_configs.sh service

   - **Example Output:**

     .. image:: _static/image23.png
        :alt: Output of srsran_install_configs.sh service
        :align: center
        :width: 80%

     *Figure: Output showing the installation of srsRAN configuration files.*

   - **Note:** The configuration files are typically installed in `/etc/srsran`.

2. **Edit `ue.conf`:**

   The following changes need to be made to the UE configuration file to allow it to connect to the gNB in SA mode.

   - **RF Settings:**

     - Under the `[rf]` section, update the parameters to configure the B210 optimally:

       .. code-block:: ini

          [rf]
          freq_offset = 0
          tx_gain = 50
          rx_gain = 40
          srate = 23.04e6
          nof_antennas = 1

          device_name = uhd
          #device_args = sync=external       # If using a reference clock, uncomment this line.
          time_adv_nsamples = 300

   - **Disable LTE Carrier:**

     - In the `[rat.eutra]` section, disable the LTE carrier to force the UE to use a 5G NR carrier:

       .. code-block:: ini

          [rat.eutra]
          dl_earfcn = 2850
          nof_carriers = 0

   - **Configure 5G SA Mode:**

     - In the `[rat.nr]` section, configure the settings for 5G SA mode operation:

       .. code-block:: ini

          [rat.nr]
          bands = 3
          nof_carriers = 1
          max_nof_prb = 106
          nof_prb = 106

     - **Note:** The `max_nof_prb` and `nof_prb` parameters should be adapted based on the bandwidth (BW) used:

       +--------+--------+
       | **BW** | **PRBs** |
       +========+========+
       |   5    |   25   |
       +--------+--------+
       |   10   |   52   |
       +--------+--------+
       |   15   |   79   |
       +--------+--------+
       |   20   |  106   |
       +--------+--------+

   - **Set Release and UE Category:**

     - In the `[rrc]` section:

       .. code-block:: ini

          [rrc]
          release = 15
          ue_category = 4

   - **USIM Credentials:**

     - Note that the following (default) USIM credentials are used in the `[usim]` section:

       .. code-block:: ini

          [usim]
          mode = soft
          algo = milenage
          opc  = 63BFA50EE6523365FF14C1F45F88737D
          k    = 00112233445566778899aabbccddeeff
          imsi = 001010123456780
          imei = 353490069873319

   - **APN Configuration:**

     - Enable the APN with the following settings in the `[nas]` section:

       .. code-block:: ini

          [nas]
          apn = srsapn
          apn_protocol = ipv4

   - **Note:** Ensure that the `imsi`, `k`, `opc`, and other parameters match those configured in the Open5GS subscriber database. Use unique values to avoid conflicts with other users.

Adjust System Buffers
---------------------

1. **Increase System Buffer Sizes:**

   .. code-block:: bash

      sudo sysctl -w net.core.rmem_max=24862979
      sudo sysctl -w net.core.wmem_max=24862979

**Note:** We will not run the UE for now since there is no network for it to attach to.

