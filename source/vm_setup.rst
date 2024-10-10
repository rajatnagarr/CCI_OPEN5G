Virtual Machine Setup
=====================

Objective
---------

Set up virtual machines for the Open5GS core, gNB, and UE with appropriate resource allocations.

Minimum Requirements
--------------------

While Ubuntu can run with minimal resources (e.g., 512 MB RAM, 700 MHz single-core CPU, 3-4 GB disk space), for optimal performance during this experiment, it's recommended to use the following VM specifications:

- **RAM:** 4 GB
- **CPU:** 4 CPUs
- **Disk Space:** 12 GB

**Note:** Allocating sufficient resources ensures better performance, especially when running network functions.

Creating the Core VM
--------------------

1. **Follow the Quickstart Guide:**

   - Use the Open5GS Quickstart Guide to create a VM with the Core GUI:

     `Open5GS Quickstart Guide <https://open5gs.org/open5gs/docs/guide/01-quickstart/>`_

   - Alternatively, follow the steps in the "Setting Up the Open5GS Core" section.

2. **Allocate Resources:**

   - Ensure the VM has at least the recommended specs (4 CPUs, 4 GB RAM, 12 GB disk).

3. **Setup Process:**

   - The desktop image does not need to be deployed via CLI. You can use the OpenStack console or your virtualization platform's GUI.
   - Take screenshots during the VM creation process if needed.

Creating the gNB and UE VMs
---------------------------

1. **Create the gNB VM via CLI:**

   - Using your OpenStack RC file, create the gNB VM:

     .. code-block:: bash

        openstack --insecure server create --flavor 4cpu-6ram-16disk --image Ubuntu-20.04-ServerImage \\
        --nic port-id=`openstack --insecure port list | grep USRP-120 | awk '{print $2}'` \\
        --nic net-id=<NETWORK_ID> --user-data cloud-config.yml \\
        --availability-zone radio gNB-VM

   - **Note:** Replace `<NETWORK_ID>` and other parameters as necessary for your environment.

   - **Example of Command Execution:**

     .. image:: _static/image20.png
        :alt: OpenStack gNB VM Creation Command
        :align: center
        :width: 80%

     *Figure: Screenshot of the command executed in the terminal to create the gNB VM.*

   - This VM will be used to install and run the srsRAN gNB. Refer to the srsRAN Installation Guide for detailed instructions:

     `srsRAN Installation Guide <https://docs.srsran.com/projects/project/en/latest/user_manuals/source/installation.html>`_

2. **Create the UE VM via OpenStack GUI:**

   - Go to the OpenStack dashboard.
   - Launch a new instance for the UE VM.
   - Name it appropriately and select the compute availability zone.
   - Use the same settings as for the gNB VM.

Configuring Network Settings
----------------------------

**For both gNB and UE VMs:**

1. **Edit Netplan Configuration:**

   - Open the netplan configuration file:

     .. code-block:: bash

        sudo vi /etc/netplan/50-cloud-init.yaml

   - Update the file with the necessary network configurations. Here is an example:

     .. code-block:: yaml

        network:
          version: 2
          renderer: networkd
          ethernets:
            ens3:
              dhcp4: true
            ens4:
              dhcp4: false
              addresses: [192.168.10.2/24]

     - Replace `ens3` and `ens4` with your network interfaces.

   - **Example Netplan Configuration:**

     .. image:: _static/image24.png
        :alt: Netplan Configuration Example
        :align: center
        :width: 50%

     *Figure: Sample netplan configuration file for setting up network interfaces.*

2. **Apply Netplan Configuration:**

   .. code-block:: bash

      sudo netplan apply

3. **Verify Network Connectivity:**

   - Ping the USRP to ensure connectivity:

     .. code-block:: bash

        ping <USRP_IP_ADDRESS>
