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

   - The configuration files are typically installed in `/etc/srsran`.

2. **Edit `ue.conf`:**

   - Open the `ue.conf` file:

     .. code-block:: bash

        sudo vi /etc/srsran/ue.conf

   - Make the following changes to allow it to connect to the gNB in SA mode:

     - **RF Settings:**
       - Set the appropriate frequency bands.
     - **USIM Settings:**
       - Update `imsi`, `k`, `opc`, and `ue_ambr` with unique values.
       - **Note:** Use different values to avoid conflicts with other users.

   - Refer to the srsUE documentation for detailed configuration options:

     `srsUE Configuration Guide <https://docs.srsran.com/projects/project/en/latest/tutorials/source/srsUE/source/index.html>`_

3. **Adjust System Buffers:**

   .. code-block:: bash

      sudo sysctl -w net.core.rmem_max=24862979
      sudo sysctl -w net.core.wmem_max=24862979

**Note:** We will not run the UE for now since there is no network for it to attach to.

