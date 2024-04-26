帧抢占
======

目标
----

以太网帧抢占是802.1Qbu标准中规定的一项功能，它允许高优先级帧在以太网的媒体访问控制（MAC）层中中断低优先级帧的传输。这对于需要对高优先级帧进行低延迟传输的时间敏感的应用程序非常有用。例如，在时间敏感网络（TSN）应用中，高优先级帧可能包含必须尽可能少延迟传递的时间敏感数据。帧抢占可以帮助确保这些高优先级帧优先于低优先级帧传输，从而减少它们的传输延迟。

在本展示中，我们将演示以太网帧抢占并检查它可以提供的延迟减少。通过本展示，您将了解帧抢占的工作原理以及如何在以太网中应用来提高时间敏感应用的性能。

| INET版本：``4.3``
| 源文件位置：`inet/showcases/tsn/framepreemption <https://github.com/inet-framework/inet/tree/master/showcases/tsn/framepreemption>`__

模型
----

概览
~~~~

在时间敏感的网络应用中，以太网抢占可以显著降低延迟。 当低优先级数据传输，高优先级帧的可进行传输的时候， 以太网MAC可以中断低优先级帧的传输，并开始发送高优先级帧。当高优先级帧完成时，MAC 可以继续从中断的位置传输低优先级帧，最终发送低优先级帧在两个（或更多）片段中帧。

抢占是INET组合以太网模型的一个特性。它使用INET的数据包流API，因此数据包传输表示为可中断的流。抢占需要:ned:`LayeredEthernetInterface`，它包含一个MAC层和一个PHY层，如下图所示：

.. figure:: media/LayeredEthernetInterface2.png
   :align: center

要启用抢占，需要用 :ned:`EthernetPreemptingMacLayer` 和 :ned:`EthernetPreemptingPhyLayer` 替换默认的子模块 :ned:`EthernetMacLayer` 和 :ned:`EthernetPhyLayer`。

:ned:`EthernetPreemptingMacLayer` 包含两个子模块，这两个子模块本身代表以太网MAC层，一个是可抢占的（:ned:`EthernetFragmentingMacLayer`）和一个快速MAC层（:ned:`EthernetStreamingMacLayer`），每个都有自己的帧队列：

.. figure:: media/mac.png
   :align: center


2024。4.26校对书签


:ned:`EthernetPreemptingMacLayer` 使用节点内数据包流。离散数据包
从高层进入MAC模块，但离开子MAC层（快速和可抢占）时
作为数据包流。数据包以流的形式离开MAC层，并通过
PHY层和链接以此种形式表示。

在抢占的情况下，数据包最初从可抢占的子MAC层流出。
当快速MAC接收到数据包时，``scheduler`` 会通知 ``preemptingServer``。
``preemptingServer`` 停止可抢占流，发送完整的快速流，
然后最终恢复可抢占流。

PHY层插入帧间隙。

.. **待办事项** `其他地方？` 注意，任何时候只能有一个帧被抢占分片。

:ned:`EthernetPreempt

配置
~~~~~~~~

模拟使用以下网络：

.. figure:: media/network.png
   :align: center

它包含两个通过100Mbps以太网连接的 :ned:`StandardHost` 和一个 :ned:`PcapRecorder` 用来记录PCAP追踪；``host1`` 定期为 ``host2`` 生成数据包。

我们主要想比较端到端延迟，因此我们在以下三种配置中运行模拟，使用相同数据包长度的低优先级和高优先级流量：

- ``FifoQueueing``: 基线配置；不使用优先级队列或抢占。
- ``PriorityQueueing``: 在以太网MAC中使用优先级队列，以降低高优先级帧的延迟。
- ``FramePreemption``: 对高优先级帧使用抢占，极大地降低延迟，确保上限。

此外，我们展示了使用更真实的流量：长时间且频繁的低优先级帧与短暂、不频繁的高优先级帧的优先队列和抢占。这些模拟是上述三种配置的扩展，定义在 ini 文件中，以 ``Realistic`` 前缀命名。

在``General``配置中，主机被配置为使用分层以太网模型而不是默认模型，必须禁用：

.. literalinclude:: ../omnetpp.ini
   :start-at: encap.typename
   :end-at: LayeredEthernetInterface
   :language: ini

我们还想记录PCAP追踪，以便在Wireshark中检查流量。我们启用PCAP记录，并设置PCAP记录器来转储以太网PHY帧，因为抢占在PHY头中是可见的：

.. literalinclude:: ../omnetpp.ini
   :start-at: recordPcap
   :end-at: fcsMode
   :language: ini

这是``host1``中流量生成的配置：

.. literalinclude:: ../omnetpp.ini
   :start-at: numApps
   :end-at: app[1].io.destPort
   :language: ini

在``host1``中有两个 :ned:`UdpApp`，一个生成背景流量（低优先级）另一个生成高优先级流量。UDP应用为数据包加上VLAN标签，以太网MAC使用标签中的VLAN ID来分类流量为高低优先级。

我们设置了高比特率的背景流量（96 Mbps）和较低比特率的高优先级流量（9.6 Mbps）；两者都使用1200B的数据包。它们的总和故意高于100 Mbps链路容量（我们希望队列不为空）；超额的数据包将被丢弃。

.. literalinclude:: ../omnetpp.ini
   :start-at: app[0].source.packetLength
   :end-at: app[1].source.productionInterval
   :language: ini

``FifoQueueing`` 配置不使用抢占或优先级队列，该配置仅限制 :ned:`EthernetMac` 的队列长度为4。

在所有三种情况下，队列需要短小以减少排队时间对测量延迟的影响。然而，如果它们太短，可能会太频繁地为空，这会使优先级队列无效（例如，如果它只包含一个数据包，它就不能优先处理）。队列长度4是一个任意选择。队列类型设置为 :ned:`DropTailQueue`，以便在队列满时可以丢弃数据包：

.. literalinclude:: ../omnetpp.ini
   :start-at: Config FifoQueueing
   :end-before: Config
   :language: ini

在``PriorityQueueing``配置中，我们在Mac层改变了队列类型，从默认的 :ned:`PacketQueue` 改为 :ned:`PriorityQueue`：

.. literalinclude:: ../omnetpp.ini
   :start-at: Config PriorityQueueing
   :end-before: Config
   :language: ini

优先级队列利用两个内部队列，为两个流量类别服务。为了限制队列时间对测量的端到端延迟的影响，我们也限制了内部队列的长度为4。我们还禁用了共享缓冲区，并设置队列类型为 :ned:`DropTailQueue`。我们使用优先级队列的分类器将数据包放入两个流量类别中。

在``FramePreemption``配置中，我们用 :ned:`EthernetPreemptingMacLayer` 和 :ned:`EthernetPreemptingPhyLayer` 替换了 :ned:`LayeredEthernetInterface` 中默认的 :ned:`EthernetMacLayer` 和 :ned:`EthernetPhyLayer` 模块，这些模块支持抢占。

.. literalinclude:: ../omnetpp.ini
   :start-at: Config FramePreemption
   :end-at: DropTailQueue
   :language: ini

在此配置中没有优先级队列，两个MAC子模块各自拥有自己的队列。我们也限制了队列长度为4，并配置队列类型为 :ned:`DropTailQueue`。

.. note:: 我们也可以在以太网可抢占MAC模块中设置一个共享的优先级队列，但这里不包括这个设置。

我们对``RealisticFifoQueueing``、``RealisticPriorityQueueing`` 和 ``RealisticFramePreemption`` 配置使用以下流量：

.. literalinclude:: ../omnetpp.ini
   :start-after: Config RealisticBase
   :end-before: Config RealisticFifoQueueing
   :language: ini

在这个流量配置中，高优先级数据包的频率是低优先级数据包的100倍，大小是低优先级数据包的1/10。

传输线上
~~~~~~~~~~~~~~~~~~~~~~~~

为了理解在OMNeT++ GUI中帧抢占是如何表示的（在Qtenv的动画和数据包日志中，以及在IDE的序列图中），必须了解数据包传输在OMNeT++中是如何建模的。

传统上，链路上的帧传输在OMNeT++中通过发送“数据包”来表示。这个“数据包”是一个C++对象（即数据结构），属于或继承自OMNeT++类``cPacket``。发送时间对应于传输开始的时间。数据包数据结构包含帧的字节长度和（或多或少抽象的）帧内容。传输的结束是隐含的：它被计算为*开始时间* + *持续时间*，其中*持续时间*要么是明确的，要么根据帧大小和链路比特率推导出来。这种方法的原始形式当然不适合以太网帧抢占，因为无法预先知道帧传输是否会被抢占，以及在哪个点会被抢占。

相反，在OMNeT++ 6.0中，上述方法被修改以适应新的用例。在新方法中，原始的数据包发送保持不变，但其解释略有变化。它现在代表一个*预测*：“这是一个帧，其传输将会完成，除非我们另有声明”。也就是说，当传输正在进行时，可以发送*传输更新*，这改变了对传输剩余部分的预测。*传输更新*数据包本质上说：“忽略我之前关于总帧大小/内容和传输时间的说法，这是根据当前状况剩余传输将要花费的时间，这里是更新的帧长度/内容。”

传输更新可能会截断、缩短或延长传输（和帧）。出于技术原因，传输更新数据包携带完整的帧大小和内容（不仅仅是剩余部分），但必须由发送者以一种与已经传输的内容一致的方式制作（它不能改变过去）。例如，通过表示剩余时间为零，并设置帧内容为到那时为止已传输的内容来进行截断。更新的传输可能会被后续的传输更新进一步修改。传输的结束仍然是隐含的（根据最后一个传输更新完成），但也可以通过在传输本来结束的确切时间发送一个零剩余时间的传输更新来明确结束。在传输结束时间过后，自然不可能再为它发送更多的传输更新（我们不能修改过去）。

鉴于上述情况，很容易看出为什么一个被抢占的以太网帧会在例如Qtenv的数据包日志中多次出现：原始传输和随后的传输更新都是数据包。

- 第一个是原始数据包，包含完整的帧大小/内容，并预测帧传输将不间断地进行。
- 第二个在决定帧将被抢占的内部节点中发送。在那时，节点计算截断的帧和剩余的传输时间，考虑到至少当前的八位字节和FCS需要传输，且有最小帧大小要求。该数据包代表截断帧的大小/内容，包括FCS。
- 在当前的以太网模型实现中，还会发送一个显式的结束传输更新，其剩余传输持续时间为零，帧大小/内容与前一个相同。这实际上并不严格必要，且可能在未来的INET版本中发生变化。

上述数据包使用名称后缀来区分：``:progress`` 和 ``:end`` 分别添加到原始数据包名称中，用于传输更新和显式结束传输。此外，数据包本身也通过添加``-frag0``, ``-frag1``, 等到其名称来重新命名，以使帧片段相互区分。例如，名为``background3``的帧可能后继为``background3-frag0:progress`` 和 ``background3-frag0:end``。在干扰的快速帧也完成传输后，``background3-frag1`` 将会跟随（见下一节的视频）。

结果
-------

帧抢占行为
~~~~~~~~~~~~~~~~~~~~~~~~~

这是一个帧抢占行为的视频：

.. video:: media/preemption3.mp4
   :width: 100%
   :align: center

以太网MAC在``host1``开始传输``background-3``。在传输过程中，一个高优先级帧（``ts-1``）到达MAC。MAC中断了``background-3``的传输；在动画中，``background-3``最初显示为完整帧，当高优先级帧可用时变为``background-3-frag0:progress``。传输高优先级帧后，传输剩余的``background-3-frag1``片段。

帧序列显示在Qtenv的数据包日志中：

.. figure:: media/packetlog5.png
   :align: center
   :width: 100%

如前节所述，被抢占的帧在数据包日志中多次出现，因为对帧的更新被记录下来。起初，``background-3`` 被记录为一个不间断的帧。当高优先级帧可用时，帧名变为``background-3-frag0``，并被单独记录。实际上，在``ts-1``之前只发送了一个名为``background-3-frag0``的帧，但进行了三次单独的包更新。

相同的帧序列在以下图像的序列图中显示，每张图中选择并突出显示了不同的帧。注意时间线是非线性的：

.. figure:: media/seqchart4.png
   :align: center
   :width: 100%

就像在数据包日志中一样，序列图包含了最初预定的、未中断的``background-3``帧，它在其传输开始时被记录。

.. note:: 您可以认为序列图上实际上存在两个时间维度：事件和消息在当时发生，以及模块对未来的“思考”，即传输将花费多长时间。实际上，传输可能会被中断，因此原始的（``background-3``）和“更新的”（``background-3-frag0``）都存在于图表上。

这是在线性时间线上的帧序列，突出显示了``background-3-frag0``帧：

.. figure:: media/linear.png
   :align: center
   :width: 100%

注意``background-3-frag0:progress``非常短（它基本上只包含一个带有FCS的更新数据包，作为第一个片段的剩余数据部分）。``ts-1``的传输在一个短的帧间隙后开始。

这是Wireshark中显示的相同帧序列：

.. figure:: media/wireshark.png
   :align: center
   :width: 100%

帧在每个帧或片段的传输结束时记录在PCAP文件中，因此原本预定的1243B ``background-3``帧不在那里，只有两个片段。

在Wireshark日志中，``frame 5`` 和 ``frame 7`` 是``background-3``的两个片段。注意FPP指的是`帧抢占协议`；``frame 6`` 是在两个片段之间发送的``ts-1``。

这是Qtenv的数据包检查器中显示的``background-3-frag1``：

.. figure:: media/packetinspector5.png
   :align: center
   :width: 100%

这个片段不包含MAC头，因为它是原始以太网帧的第二部分。

.. **TODO** 无高亮

高优先级和低优先级（快速和可抢占）数据包在 :ned:`EthernetPreemptingMacLayer` 中的路径如下图红线所示：

.. figure:: media/preemptible2.png
   :align: center

.. figure:: media/express2.png
   :align: center

分析端到端延迟
~~~~~~~~~~~~~~~~~~~~~~~~~~

模拟结果
++++++++++++++++++

为了分析相同数据包长度配置的结果，我们在以下图表上绘制了[0,t]内UDP数据包的平均端到端延迟。注意配置使用不同的线条样式区分，流量类别由颜色区分：

.. figure:: media/delay.png
   :align: center
   :width: 80%

图表显示，在默认配置的情况下，两个流量类别的延迟大致相同。使用优先级队列显著降低了高优先级帧的延迟，并与基线默认配置相比，略微增加了背景帧的延迟。抢占对高优先级帧的延迟减少更大，但以增加背景帧的延迟为代价。

估计端到端延迟
+++++++++++++++++++++++++++++++

在下一节中，我们将通过一些简单的计算检验这些结果的可靠性。

``FifoQueueing``配置
**************************

对于``FifoQueueing``配置，MAC将背景和高优先级数据包存储在同一个FIFO队列中。因此，两个流量类别的延迟大致相同。由于高流量，队列始终包含数据包。队列限制为4个数据包，因此排队时间有上限：大约是4帧的传输时间。查看队列长度统计（见anf文件），我们可以看到平均队列长度约为2.6，因此数据包平均承受2.6帧传输持续时间的排队延迟。

端到端延迟大约是一帧的传输持续时间+排队延迟+帧间隙。1200B帧在100Mbps以太网上的传输持续时间大约为0.1ms。平均而言，队列中有两帧，因此帧在队列中等待两帧传输持续时间。100Mbps以太网的帧间隙为0.96us，所以我们认为它可以忽略不计：

``delay ~= txDuration + 2.6 * txDuration + IFG = 3.6 * txDuration = 0.36ms``

``PriorityQueueing``配置
******************************

对于``PriorityQueueing``配置，高优先级帧在MAC中的PriorityQueue模块有自己的子队列。当高优先级帧到达队列时，MAC将完成当前的低优先级传输（如果有的话）然后开始传输高优先级帧。因此，高优先级帧可能会被延迟，因为需要首先完成当前帧的传输。然而，使用优先级队列降低了高优先级帧的延迟，并增加了与仅使用一个队列的所有帧相比的背景帧的延迟。

由于高背景流量，背景队列中总是存在一个帧。高优先级帧需要等待当前背景帧传输完成；平均而言，剩余持续时间是背景帧传输持续时间的一半：

``delay ~= txDuration + 0.5 * txDuration + IFG = 1.5 * txDuration = 0.15ms``

``FramePreemption``配置
*****************************

对于``FramePreemption``配置，高优先级帧在MAC中有自己的队列。当一个高优先级帧可用时，当前的背景帧传输几乎立即停止。

延迟大致是一个FCS的持续时间+传输持续时间+帧间隙。FCS的持续时间约为1us，因此我们在计算中忽略它（如前所述，帧间隙也被忽略）：

``delay = txDuration + fcsDuration + IFG ~= txDuration = 0.1ms``

上述计算值大致与模拟结果相符。

真实交通
+++++++++++++++++

以下图表绘制了真实交通案例的平均端到端延迟：

.. figure:: media/realisticdelay.png
   :align: center
   :width: 80%

上图中矩形指示的范围在下图中放大显示，以便更清晰地查看：

.. figure:: media/realisticdelay_zoomed.png
   :align: center
   :width: 80%

如上所述，使用抢占时高优先级帧的端到端延迟独立于背景帧的长度。延迟大约是高优先级帧的传输持续时间（在相同长度和真实交通结果的情况下显而易见）。

在真实交通案例中，背景帧的延迟不受优先级队列或抢占的影响。由于交通不同（原来，背景和高优先级数据包的长度相同，因此可以更好地进行比较），高优先级帧的延迟显著降低。

来源：:download:`omnetpp.ini <../omnetpp.ini>`, :download:`FramePreemptionShowcase.ned <../FramePreemptionShowcase.ned>`

讨论
----------

使用 `这个 <https://github.com/inet-framework/inet/discussions/676>`__ 页面在GitHub问题跟踪器中评论此展示。

