Virtual Machine Setup
=====================

Objective
---------

Set up virtual machines for the Open5GS core, gNB, and UE with appropriate resource allocations.

Minimum Requirements
--------------------

While Ubuntu can run with minimal resources, for optimal performance during this experiment, it's recommended to use the following VM specifications:

- **RAM:** 4 GB
- **CPU:** 4 CPUs
- **Disk Space:** 12 GB

Creating the Core VM
--------------------

1. **Follow the Quickstart Guide:**

   - Use the Open5GS Quickstart Guide to create a VM with the Core GUI:

     `Open5GS Quickstart Guide <https://open5gs.org/open5gs/docs/guide/01-quickstart/>`_

2. **Allocate Resources:**

   - Ensure the VM has at least the recommended specs.

3. **Setup Process:**

   - Take screenshots during the VM creation process if needed.

Creating the gNB and UE VMs
---------------------------

**Using OpenStack CLI:**

1. **Load OpenStack RC File:**

   - Source your OpenStack RC file to interact with the OpenStack environment.

2. **Create VMs for gNB and UE:**

   - Run the following command to create the gNB VM:

     .. code-block:: bash

        openstack --insecure server create --flavor 4cpu-6ram-16disk --image Ubuntu-20.04-ServerImage \\
        --nic port-id=`openstack --insecure port list | grep USRP-120 | awk '{print $2}'` \\
        --nic net-id=ff409397-4e45-4af9-afbe-00a979369aea --user-data cloud-config.yml \\
        --availability-zone radio USRP-120-gNB

   - Replace parameters as necessary for your environment.

3. **Create the UE VM via OpenStack GUI:**

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

2. **Apply Netplan Configuration:**

   .. code-block:: bash

      sudo netplan apply

3. **Verify Network Connectivity:**

   - Ping the USRP to ensure connectivity:

     .. code-block:: bash

        ping <USRP_IP_ADDRESS>

