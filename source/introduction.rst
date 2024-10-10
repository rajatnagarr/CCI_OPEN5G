Introduction
============

This documentation provides a comprehensive guide to setting up an Open5GS core network and integrating it with srsRAN to create a 5G standalone network. By following this guide, you will:

- Create virtual machines (VMs) for the core network, gNB, and UE.
- Install and configure Open5GS Core with GUI support.
- Set up srsRAN for the gNB and UE.
- Connect the UE to the network and perform end-to-end testing.

**Prerequisites:**

- Basic knowledge of Linux command-line operations.
- Access to an OpenStack environment or virtualization platform.
- Internet connectivity for downloading required packages and repositories.

**Overview of 5G SA Core Functions**

The 5G Standalone (SA) Core comprises several key functions that work together to provide 5G network services. Here is an overview of these core functions:

1. **NRF - NF Repository Function**

   Imagine the NRF as the library catalog for the 5G SA Core. It's responsible for maintaining a directory of all available network functions (NFs). Other core components register with the NRF and use it to discover and communicate with their peers.

2. **SCP - Service Communication Proxy**

   The SCP acts as a communication mediator, ensuring different core functions can interact seamlessly. It ensures that messages are correctly translated and transmitted between various NFs.

3. **AMF - Access and Mobility Management Function**

   The AMF manages connections and mobility. It coordinates how devices connect and move within the network, much like an air traffic controller. When gNBs (5G base stations) need to establish connections, they reach out to the AMF.

4. **UDM - Unified Data Management**

   The UDM serves as the memory bank, storing subscriber profiles and authentication vectors. It securely houses subscriber information, ensuring secure and authorized access to the network.

5. **AUSF - Authentication Server Function**

   The AUSF collaborates closely with the UDM to generate authentication credentials. It ensures that only authorized users gain entry to the network.

6. **UDR - Unified Data Repository**

   The UDR complements the UDM by providing a comprehensive data repository. It stores historical data, usage patterns, and network statistics for analysis and decision-making.

7. **PCF - Policy and Charging Function**

   The PCF enforces policies and charging rules, managing the allocation of network resources to ensure fair usage and efficient resource utilization. It also handles charging for services.

8. **NSSF - Network Slice Selection Function**

   The NSSF is responsible for selecting the appropriate "slice" of the network for different applications and services. It ensures the network is tailored to meet specific requirements, such as low latency or high bandwidth.

9. **BSF - Binding Support Function**

   The BSF enables efficient indirect communication between various core functions, ensuring that messages reach their intended recipients even if they don't have direct connections.

10. **SMF - Session Management Function**

    The SMF orchestrates and manages sessions within the 5G network. It sets up data paths, allocates resources, and ensures that data flows smoothly between devices and services.

11. **UPF - User Plane Function**

    The UPF represents the highway of data transmission in the 5G SA Core. It carries user data packets between the gNB and the external Wide Area Network (WAN), efficiently routing data to its destination.

**How the Core Functions Collaborate**

- **Initialization:** When a 5G device connects to the network, it communicates with the gNB, which establishes a connection with the AMF.
- **Authentication and Authorization:** The AMF checks with the AUSF and UDM for subscriber credentials. Once authenticated, the device gains access.
- **Session Management:** The SMF manages session setup, data paths, and resource allocation.
- **Policy Enforcement:** The PCF enforces policies to ensure data usage aligns with subscriber plans and network policies.
- **Data Transmission:** The UPF routes user data packets efficiently between the gNB and external networks.
- **Network Slicing:** The NSSF selects the appropriate network slice to optimize performance based on application requirements.
- **Communication Mediation:** The SCP ensures messages are correctly translated and transmitted between various core functions.

Throughout this process, the SCP acts as the communication bridge, facilitating interaction between the different network functions.

**Note:** Understanding these components and their interactions is crucial for setting up and troubleshooting a 5G SA network.
