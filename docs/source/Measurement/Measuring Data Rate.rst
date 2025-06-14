测量数据速率
====================

目标
~~~~~

在这个例子中，我们探讨了网络节点中应用层、队列模块和过滤模块的数据速率统计。

INET版本：``4.4``  
源文件位置：`inet/showcases/measurement/datarate <https://github.com/inet-framework/inet/tree/master/showcases/measurement/datarate>`__

模型
~~~~~~

数据速率是通过在节点架构的某个位置观察数据包随时间的通过情况来测量的。例如，一个源应用模块会随时间产生数据包，这一过程本身就具有数据速率。同样地，队列模块会随时间将数据包入队和出队，这两个过程也分别具有自己的数据速率。这些数据速率之间的差异会导致队列长度随时间增长或减少。

以下是网络配置：

.. image:: Pic/Network.png
   :alt: Network.png
   :align: center

以下是配置：

.. code:: ini
   [General]
   network = DataRateMeasurementShowcase
   description = "Measure data rate in several modules throughout the network"
   sim-time-limit = 1s

   # 源应用，吞吐量约为 ~48Mbps
   *.source.numApps = 1
   *.source.app[0].typename = "UdpSourceApp"
   *.source.app[0].source.packetLength = 1200B
   *.source.app[0].source.productionInterval = exponential(200us)
   *.source.app[0].io.destAddress = "destination"
   *.source.app[0].io.destPort = 1000

   # 目的地应用
   *.destination.numApps = 1
   *.destination.app[0].typename = "UdpSinkApp"
   *.destination.app[0].io.localPort = 1000

   # 启用模块化以太网模型
   *.*.ethernet.typename = "EthernetLayer"
   *.*.eth[*].typename = "LayeredEthernetInterface"

   # 所有网络接口的数据速率
   *.*.eth[*].bitrate = 100Mbps

结果
~~~~~~

以下是结果：

.. image:: Pic/source_outgoing.png
   :alt: source_outgoing.png
   :align: center

.. image:: Pic/destination_incoming.png
   :alt: destination_incoming.png
   :align: center

.. image:: Pic/switch_incoming.png
   :alt: switch_incoming.png
   :align: center

.. image:: Pic/switch_outgoing.png
   :alt: switch_outgoing.png
   :align: center

源代码：
|  `omnetpp.ini <https://inet.omnetpp.org/docs/_downloads/62afefdbc85355a071521dba15a5c1c4/omnetpp.ini>`__  
|  `DataRateMeasurementShowcase.ned <https://inet.omnetpp.org/docs/_downloads/9bcf91bc421508497e77f913e673b3fe/DataRateMeasurementShowcase.ned>`__

讨论
----------
如果您对这个示例有任何疑问或讨论，请在 `此页面 <https://github.com/inet-framework/inet/discussions/TODO>`__ 分享您的想法。
