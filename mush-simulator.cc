
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mesh-module.h"
#include "ns3/internet-module.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/netanim-module.h" // For NetAnim

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("MeshTopologyExample");

int main(int argc, char *argv[])
{
    // Enable logging for debugging
    LogComponentEnable("MeshTopologyExample", LOG_LEVEL_INFO);

    // Create 4 nodes for the mesh network
    NodeContainer nodes;
    nodes.Create(4);

    // Set up the Wi-Fi channel and physical layer configuration
    YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default();
    YansWifiPhyHelper wifiPhy = YansWifiPhyHelper();
    wifiPhy.SetChannel(wifiChannel.Create());

    // Set up the mesh helper and configure the mesh protocol (e.g., IEEE 802.11s)
    MeshHelper mesh;
    mesh = MeshHelper::Default();
    mesh.SetStackInstaller("ns3::Dot11sStack");  // Set up for 802.11s mesh
    mesh.SetSpreadInterfaceChannels(MeshHelper::SPREAD_CHANNELS);
    mesh.SetMacType("RandomStart", TimeValue(Seconds(0.1)));
    mesh.SetNumberOfInterfaces(1);

    // Install the mesh network on the nodes
    NetDeviceContainer meshDevices = mesh.Install(wifiPhy, nodes);

    // Set up mobility model - give each node a static position
    MobilityHelper mobility;
    mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                  "MinX", DoubleValue(0.0),
                                  "MinY", DoubleValue(0.0),
                                  "DeltaX", DoubleValue(5.0),
                                  "DeltaY", DoubleValue(10.0),
                                  "GridWidth", UintegerValue(2),
                                  "LayoutType", StringValue("RowFirst"));
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(nodes);

    // Set up the Internet stack and assign IP addresses
    InternetStackHelper internetStack;
    internetStack.Install(nodes);
    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = address.Assign(meshDevices);

    // Print the IP address of each node
    for (uint32_t i = 0; i < nodes.GetN(); ++i)
    {
        Ptr<Ipv4> ipv4 = nodes.Get(i)->GetObject<Ipv4>();
        Ipv4Address ipAddr = ipv4->GetAddress(1, 0).GetLocal();
        NS_LOG_INFO("Node " << i << " has IP address: " << ipAddr);
    }

    // Enable NetAnim for visualization
    AnimationInterface anim("mesh-topology.xml");

    // Run the simulation for 10 seconds
    Simulator::Stop(Seconds(10.0));
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}

