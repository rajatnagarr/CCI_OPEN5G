Troubleshooting and Common Issues
=================================

Issue with `sudo apt update`
----------------------------

**Problem:**

- Running `sudo apt update` results in errors due to incorrect distribution codename.

**Solution:**

- Replace `disco` with `focal` in your sources list:

  .. code-block:: bash

     sudo sed -i -e 's|disco|focal|g' /etc/apt/sources.list
     sudo apt update

Compiler Issues When Building srsRAN
------------------------------------

**Problem:**

- The compiler version is not correct, leading to build errors.

**Solution:**

- Install the correct compiler versions and set them:

  .. code-block:: bash

     sudo apt install gcc-10 g++-10
     export CC=$(which gcc-10)
     export CXX=$(which g++-10)
     cmake .. -DCMAKE_BUILD_TYPE=Release
     make -j$(nproc)
     sudo make install
     sudo ldconfig

UE Cannot Attach to Network
---------------------------

**Problem:**

- The UE is unable to attach to the network.

**Solutions:**

- **Check UE Configuration:**

  - Ensure the `ue.conf` file has the correct `imsi`, `k`, and `opc` values matching those in the Open5GS subscriber database.

- **Verify Network Connectivity:**

  - Ping the gNB and Open5GS core from the UE VM to ensure network paths are open.

- **Adjust System Buffers:**

  - Ensure the buffer sizes are set correctly:

    .. code-block:: bash

       sudo sysctl -w net.core.rmem_max=24862979
       sudo sysctl -w net.core.wmem_max=24862979

gNB Fails to Connect to Open5GS Core
------------------------------------

**Problem:**

- The gNB is unable to establish a connection with the Open5GS core.

**Solutions:**

- **Check gNB Configuration:**

  - Verify that the `amf_addr` in the gNB configuration file points to the correct IP address of the Open5GS core.

- **Firewall Settings:**

  - Ensure that no firewalls are blocking the required ports between the gNB and the core.

- **Verify AMF Configuration:**

  - Confirm that the `ngap` address in the Open5GS `sample.yaml` configuration matches the core's IP address.

General Tips
------------

- **Consult Official Documentation:**

  - Refer to the official srsRAN and Open5GS documentation to verify configurations.

- **Unique Identifiers:**

  - Use unique `imsi`, `k`, `opc`, `mcc`, `mnc`, and `cell_id` values to prevent conflicts with other users.

- **Logs and Debugging:**

  - Check logs on the UE, gNB, and core for error messages that can provide clues.

- **System Resources:**

  - Ensure that your VMs have sufficient resources and that CPU performance settings are applied.

- **Avoid Common Mistakes:**

  - Double-check IP addresses, port settings, and configuration parameters to prevent common errors.
