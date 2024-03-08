直通交换
==============================

目标
-----

直通交换（Cut-through Switching）是一种在分组交换系统中广泛应用的方法，特别是在以太网交换机中，用于快速转发帧或数据包。 \
其基本原理是在整个帧完全接收之前即可开始转发，通常是在确认目地地址和出端口后立即执行。与存储-转发交换相比，存储-转发交换会等待 \
整个帧完全接收后才进行转发。直通交换的主要优势在于能够降低以太网帧的切换延迟，因为交换机可以在获取足够信息后立即开始转发帧。然而，直通交换也存在一些潜在的缺点，例如相较于存储-转发切换可能具有更高的错误率，因为在转发之前它不会对整个帧进行错误检查。在这个演示中，我们将展示直通交换的工作原理，并在延迟方面与存储-转发切换进行比较。


| INET 版本: ``4.3``
| 源文件位置: `inet/showcases/tsn/cutthroughswitching <https://github.com/inet-framework/inet/tree/master/showcases/tsn/cutthroughswitching>`__

模型
-----

Cut-through 切换可以减少切换延迟，但会跳过交换机中的 FCS 检查。FCS 位于以太网帧的末尾；在目标主机中执行 FCS 检查。 （这是因为到 FCS 检查发生的时候，帧几乎完全传输了，所以没有意义）。如果数据包通过多个交换机，延迟减少会更加显著（因为在每个交换机上可以节省一个数据包传输的时间）。

Cut-through 切换利用 INET 的模块化以太网模型中的节点内数据包流。数据包流是必需的，因为帧需要作为流程（而不是整个数据包）处理，以便交换机能够在完整的数据包接收之前开始转发它。

.. note:: 在 :ned:`StandardHost` 等主机中，默认为存储-转发行为。

示例仿真包含两个通过两个 :ned:`TsnSwitch` 连接的 :ned:`TsnDevice` 节点（所有连接速率均为 1 Gbps）：

.. .. figure:: media/Network.png
   :align: center
   :width: 100%

在仿真中，``device1`` 向 ``device2`` 发送 1000 字节的 UDP 包，平均到达时间为 100 毫秒，具有 X 毫秒的抖动。omnetpp.ini 中有两个配置，``StoreAndForward`` 和 ``CutthroughSwitching``，它们仅在使用 cut-through 切换方面有所不同。

以下是这两个配置：

.. literalinclude:: ../omnetpp.ini
   :start-at: StoreAndForward
   :end-at: phyLayer
   :language: ini

以太网交换机中的默认 :ned:`EthernetInterface` 不支持 cut-through。为了使用 cut-through，我们将默认接口替换为 :ned:`EthernetCutthroughInterface`。这个接口中默认情况下禁用 cut-through，因此需要通过将 :par:`enableCutthrough` 参数设置为 ``true`` 来启用它。

此外，交换机中的所有必要组件都需要支持数据包流。交换机中的 cut-through 接口默认支持数据包流；主机中的默认 PHY 层需要替换为 :ned:`EthernetStreamingPhyLayer`，它支持数据包流。

结果
-----

以下视频显示了 Qtenv 中的存储-转发行为：

.. video:: media/storeandforward.mp4
   :width: 90%
   :align: center

接下来的视频显示了 cut-through 行为：

.. video:: media/cutthrough1.mp4
   :width: 90%
   :align: center

以下序列图摘录显示了从 ``device1`` 发送到 ``device2`` 的包经过交换机的情况，分别为存储-转发和 cut-through（时间轴是线性的）：

.. figure:: media/storeandforwardseq2.png
   :align: center
   :width: 100%

.. figure:: media/seqchart2.png
   :align: center
   :width: 100%

我们比较了存储-转发切换和 cut-through 切换中 UDP 包的端到端延迟：

.. figure:: media/delay.png
   :align: center
   :width: 100%

我们可以通过分析来验证结果。在存储-转发的情况下，端到端持续时间为 ``3 *（传输时间 + 传播时间）``，约为 25.296 毫秒。在 cut-through 的情况下，持续时间为 ``1 * 传输时间 + 3 传播时间 + 2 * cut-through 延迟``，约为 8.432 毫秒。

来源: :download:`omnetpp.ini <../omnetpp.ini>`, :download:`CutthroughSwitchingShowcase.ned <../CutthroughSwitchingShowcase.ned>`

讨论
----------
如果您对这个示例有任何疑问或讨论，请在 `此页面 <https://github.com/inet-framework/inet/discussions/685>`__ 分享您的想法。