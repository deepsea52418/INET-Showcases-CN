具有故障保护功能的组播流
=================================================================

| `原文链接 <https://inet.omnetpp.org/docs/showcases/tsn/framereplication/multicastfailureprotection/doc/index.html>`__ 
| `讲解视频 <https://space.bilibili.com/35942145>`__

目标
-----
在此示例中，我们复制了 IEEE 802.1 CB 标准的多播流示例。

INET version: ``4.4``

Source files location:
`inet/showcases/tsn/framereplication/multicastfailureprotection <https://github.com/inet-framework/inet/tree/master/showcases/tsn/framereplication/manualconfiguration>`__

模型
------
在此配置中，我们使用 TSN 交换机网络。多播流通过网络从其中一个交换机发送到所有其他交换机。

网络如下：

.. image:: Pic/Network16.png
   :alt: Network16.png
   :align: center

配置如下：

.. code:: ini
    [General]
    network = MulticastFailureProtectionShowcase
    sim-time-limit = 10ms
    description = "Automatic multicast static stream redundancy configuration with failure protection"

    # disable automatic MAC forwarding table configuration
    *.macForwardingTableConfigurator.typename = ""

    # enable freme replication and elimination
    *.*.hasStreamRedundancy = true

    # all Ethernet interfaces have 100 Mbps speed
    *.*.eth[*].bitrate = 1Gbps

    # application
    *.a.numApps = 1
    *.a.app[0].typename = "EthernetApp"
    *.a.app[0].io.remoteAddress = "01:00:00:00:00:00"
    *.a.app[0].source.packetLength = 1200B
    *.a.app[0].source.productionInterval = 1ms

    # stream redundancy
    *.streamRedundancyConfigurator.typename = "StreamRedundancyConfigurator"

    # TSN configurator
    *.failureProtectionConfigurator.typename = "FailureProtectionConfigurator"
    *.failureProtectionConfigurator.gateScheduleConfiguratorModule = ""
    *.failureProtectionConfigurator.configuration = [{name: "S", application: "app[0]", source: "a", destination: "not a",
                                                    pcp: 0, packetFilter: "*", destinationAddress: "01:00:00:00:00:00",
                                                    packetLength: 1200B, packetInterval: 1ms, maxLatency: 100us,
                                                    linkFailureProtection: [{any: 1, of: "*->*"}]}]

    # visualizer
    *.visualizer.failureProtectionConfigurationVisualizer.displayTrees = true
    *.visualizer.failureProtectionConfigurationVisualizer.lineStyle = "dashed"
    *.visualizer.streamRedundancyConfigurationVisualizer.displayTrees = true
    *.visualizer.streamRedundancyConfigurationVisualizer.lineColor = "black"

结果
------
|  `omnetpp.ini <https://inet.omnetpp.org/docs/_downloads/fb143b69cd2bea899db2662743d7136f/omnetpp.ini>`__ 
|  `MulticastFailureProtectionShowcase.ned <https://inet.omnetpp.org/docs/_downloads/5480f44b6684b25103e5ae6c80088b1b/MulticastFailureProtectionShowcase.ned>`__

讨论
----------
如果您对这个示例有任何疑问或讨论，请在 `此页面 <https://github.com/inet-framework/inet/discussions/790>`__ 分享您的想法。
