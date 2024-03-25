基于令牌桶的监管
===================

| `原文链接 <https://inet.omnetpp.org/docs/showcases/tsn/streamfiltering/tokenbucket/doc/index.html>`__ 

目标
~~~~~

在此示例中，我们使用链式令牌桶演示每个流的监管，该令牌桶允许指定规定的或过量的信息速率和突发尺寸。


INET version: ``4.5``

源地址链接:
`inet/showcases/tsn/streamfiltering/tokenbucket <https://github.com/inet-framework/inet/tree/master/showcases/tsn/streamfiltering/tokenbucket>`__


模型
~~~~~~~~~

在下面的网络中有三个网络节点，client与server是TsnDevice模块，swith是TsnSwitch模块，他们之间的链接使用100Mbps EthernetLink通道

.. image:: C:/Users/yaanng2019/Desktop/INET/令牌桶/1.png
   :alt: 模型1.png
   :align: center

网络中有四个应用程序在客户端和服务器之间创建两个独立的数据流。 数据速率随着正弦曲线变化，平均数据速率为40 Mbps和20 Mbps。

.. code:: ini
   # client applications
   *.client.numApps = 2
   *.client.app[*].typename = "UdpSourceApp"
   *.client.app[0].display-name = "best effort"
   *.client.app[1].display-name = "video"
   *.client.app[*].io.destAddress = "server"
   *.client.app[0].io.destPort = 1000
   *.client.app[1].io.destPort = 1001

   # best-effort stream ~40Mbps
   *.client.app[0].source.packetLength = 1000B
   *.client.app[0].source.productionInterval = 200us + replaceUnit(sin(dropUnit(simTime() * 10)), "ms") / 20

   # video stream ~20Mbps
   *.client.app[1].source.packetLength = 500B
   *.client.app[1].source.productionInterval = 200us + replaceUnit(sin(dropUnit(simTime() * 20)), "ms") / 10

   # server applications
   *.server.numApps = 2
   *.server.app[*].typename = "UdpSinkApp"
   *.server.app[0].io.localPort = 1000
   *.server.app[1].io.localPort = 1001
   


这两个流有两个不同的流量类别：尽力而为和视频流。 桥接层通过 UDP 目标端口识别传出数据包。 客户端编码和开关使用IEEE 802.1Q PCP字段解码流。

.. code:: ini

   # enable outgoing streams
   *.client.hasOutgoingStreams = true

   # client stream identification
   *.client.bridging.streamIdentifier.identifier.mapping = [{stream: "best effort", packetFilter: expr(udp.destPort == 1000)},
                                                         {stream: "video", packetFilter: expr(udp.destPort == 1001)}]

   # client stream encoding
   *.client.bridging.streamCoder.encoder.mapping = [{stream: "best effort", pcp: 0},
                                                 {stream: "video", pcp: 4}]

   # disable forwarding IEEE 802.1Q C-Tag
   *.switch.bridging.directionReverser.reverser.excludeEncapsulationProtocols = ["ieee8021qctag"]

   # stream decoding
   *.switch.bridging.streamCoder.decoder.mapping = [{pcp: 0, stream: "best effort"},
                                                 {pcp: 4, stream: "video"}]


每个流的入口过滤将不同的流量类别分派到单独的计量和过滤路径。

.. code:: ini
   # enable ingress per-stream filtering
   *.switch.hasIngressTrafficFiltering = true

   # per-stream filtering
   *.switch.bridging.streamFilter.ingress.numStreams = 2
   *.switch.bridging.streamFilter.ingress.classifier.mapping = {"best effort": 0, "video": 1}
   *.switch.bridging.streamFilter.ingress.meter[0].display-name = "best effort"
   *.switch.bridging.streamFilter.ingress.meter[1].display-name = "video"

对两个流都使用单速率双色计量。 该计量器包含单个令牌桶并具有两个参数：承诺信息速率和承诺突发大小。 数据包被标记为绿色或红色，红色数据包被过滤器丢弃。

.. code:: ini
   *.switch.bridging.streamFilter.ingress.meter[*].typename = "SingleRateTwoColorMeter"
   *.switch.bridging.streamFilter.ingress.meter[0].committedInformationRate = 40Mbps
   *.switch.bridging.streamFilter.ingress.meter[1].committedInformationRate = 20Mbps
   *.switch.bridging.streamFilter.ingress.meter[0].committedBurstSize = 10kB
   *.switch.bridging.streamFilter.ingress.meter[1].committedBurstSize = 5kB

    
结果
~~~~~

第一个图显示了客户端中应用级输出流量的数据速率。两种传输类别的数据速率都随着正弦曲线变化。

.. image:: C:/Users/yaanng2019/Desktop/INET/令牌桶/2.png
   :alt: 图2.png
   :align: center

下图显示了尽力而为流量类别的流过滤操作。 传出数据速率等于传入的数据速率减去丢弃的数据速率。

.. image:: C:/Users/yaanng2019/Desktop/INET/令牌桶/3.png
   :alt: 图3.png
   :align: center

下图显示了视频流类别的流过滤的操作。 传出数据速率等于传入的数据速率减去丢弃的数据速率。

.. image:: C:/Users/yaanng2019/Desktop/INET/令牌桶/4.png
   :alt: 图4.png
   :align: center

下图显示了两个流的令牌桶中的令牌数量。 填充区域意味着令牌数量随着数据包通过而快速变化。 当线路接近最小值时，数据速率达到最大值。

.. image:: C:/Users/yaanng2019/Desktop/INET/令牌桶/5.png
   :alt: 图5.png
   :align: center

最后一张图显示了服务器中应用程序级输入流量的数据速率。 数据速率稍微低于相应流过滤的输出流量的数据速率。 原因是它们是在不同的协议层测量的。

.. image:: C:/Users/yaanng2019/Desktop/INET/令牌桶/6.png
   :alt: 图6.png
   :align: center




| 源代码：
|  `omnetpp.ini <https://inet.omnetpp.org/docs/_downloads/db63db0c5b52a24ae2ca9fb309d23235/omnetpp.ini>`__ 

讨论
----------
如果您对这个示例有任何疑问或讨论，请在 `此页面 <https://github.com/inet-framework/inet/discussions/795>`__ 分享您的想法。
