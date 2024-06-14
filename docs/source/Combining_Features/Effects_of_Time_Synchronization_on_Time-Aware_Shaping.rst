时间同步对TAS整形的影响
============================================================================

| `原文链接 <https://inet.omnetpp.org/docs/showcases/tsn/combiningfeatures/gptpandtas/doc/index.html>`__ 

目标
-----

在此演示的示例中，我们将演示时间同步如何影响使用时间感知流量整形的网络中的端到端时延。

此示例建立在 `时钟漂移 <https://inet.omnetpp.org/docs/showcases/tsn/timesynchronization/clockdrift/doc/index.html>`__ 、 `使用 gPTP <https://inet.omnetpp.org/docs/showcases/tsn/timesynchronization/gptp/doc/index.html>`__ 和 `时间感知整形 <https://inet.omnetpp.org/docs/showcases/tsn/trafficshaping/timeawareshaper/doc/index.html>`__ 的基础上。

INET version: ``4.5``

Source files location:
`inet/showcases/tsn/combiningfeatures/gptpandtas <https://github.com/inet-framework/inet/tree/master/showcases/tsn/combiningfeatures/gptpandtas>`__

模型
-----------------------------------------------

概述
~~~~~~~~~~~~~~~~~~~~~~~
本演示案例中包含一个网络，该网络在每个网络节点中使用时间感知整形和不准确的本地时钟。\
时间感知整形需要所有网络节点之间的时间同步，因此我们也使用 gPTP 进行时间同步。\
这会导致流量持续存在端到端时延。我们研究了时间同步中的故障和恢复如何影响时延。

如果时间同步由于某种原因（例如主时钟离线）而失败，则时间感知整形无法再保证有界时延。\
但是，如果所有网络节点都切换到辅助主时钟，则可以继续时间同步并满足时延保证。

为了证明这一点，该示例包含三种情况，对应三种配置:

+  ``Normal operation``: 、时间同步工作，并且时延是恒定的（这与使用 gPTP 展示中的最后一个配置中的情况相同）。
+  ``Failure of master clock``: 主时钟与网络断开，时间不再同步。
+  ``Failover to a secondary master clock``: 主时钟与网络断开连接，但时间同步可以继续，因为网络节点切换到辅助主时钟。

