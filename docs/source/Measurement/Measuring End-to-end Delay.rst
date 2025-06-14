测量端到端延迟
===================

目标
~~~~~

在这个示例中，我们探索了应用程序的端到端延迟统计信息。

INET 版本: ``4.4``

源文件位置:
`inet/showcases/measurement/endtoenddelay <https://github.com/inet-framework/inet/tree/master/showcases/measurement/endtoenddelay>`__

模型
~~~~~~~~~~

端到端延迟是从数据包离开源应用程序的那一刻，到同一数据包到达目标应用程序的那一刻进行测量的。

端到端延迟通过统计信息进行测量。该统计信息衡量数据包的生命周期，即从源应用程序创建数据包到目标应用程序删除数据包的时间，统计名称为 ``meanBitLifeTimePerPacket``。

.. note::
   `meanBit` 部分指的是统计信息是按每比特定义的，结果是数据包中所有比特的每比特值的平均值。当网络中没有数据包流或分片时，数据包的比特会一起传输，因此它们具有相同的生命周期值。

模拟使用了一个包含两个主机（标准主机）的网络，通过 100Mbps 以太网连接：

.. image:: PicNetwork1.png
   :alt: Network1.png
   :align: center

我们在源主机的 UDP 应用程序中配置数据包源，随机生成 1200 字节的数据包，周期大约为 100 微秒。这大约对应 96 Mbps 的流量。以下是配置：

.. code:: ini
   [General]
   network = EndToEndDelayMeasurementShowcase
   description = "Measure packet end-to-end delay"
   sim-time-limit = 1s

   # 源应用程序 ~96Mbps 吞吐量
   *.source.numApps = 1
   *.source.app[0].typename = "UdpSourceApp"
   *.source.app[0].source.packetLength = 1200B
   *.source.app[0].source.productionInterval = exponential(100us)
   *.source.app[0].io.destAddress = "destination"
   *.source.app[0].io.destPort = 1000

   # 目标应用程序
   *.destination.numApps = 1
   *.destination.app[0].typename = "UdpSinkApp"
   *.destination.app[0].io.localPort = 1000

   # 启用模块化以太网模型
   *.*.ethernet.typename = "EthernetLayer"
   *.*.eth[*].typename = "LayeredEthernetInterface"

   # 所有网络接口的数据速率
   *.*.eth[*].bitrate = 100Mbps

结果
~~~~~~~~~~

流量大约为 96 Mbps，但周期是随机的。因此，流量可能会超过以太网链路的 100Mbps 容量。这可能导致数据包在源主机的队列中积累，从而增加端到端延迟（默认情况下队列长度没有限制）。

我们显示了端到端延迟，并以向量和直方图的形式绘制了统计数据：``meanBitLifeTimePerPacket``。

.. image:: PicEndToEndDelayHistogram.png
   :alt: EndToEndDelayHistogram.png
   :align: center

.. image:: PicEndToEndDelayVector.png
   :alt: EndToEndDelayVector.png
   :align: center

在模拟的末尾，延迟的上升是由于数据包在队列中的积累。

源代码：
|  `omnetpp.ini <https://inet.omnetpp.org/docs/_downloads/b095997b285307bb4860015e5926fab9/omnetpp.ini>`__ 
|  `EndToEndDelayMeasurementShowcase.ned <https://inet.omnetpp.org/docs/_downloads/50d12ffd3159497c2e6e96b998129ab4/EndToEndDelayMeasurementShowcase.ned>`__

讨论
----------
如果您对这个示例有任何疑问或讨论，请在 `此页面 <https://github.com/inet-framework/inet/discussions/TODO>`__ 分享您的想法。
