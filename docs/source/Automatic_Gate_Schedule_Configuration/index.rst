自动门控配置
==================================================

在时间感知整形(TAS)中，可以手动配置门控列表(GCL),即对应不同流量类别的门何时打开或关闭。 在一些简单的情况下这可能就足够了。 然而，在复杂的情况下，手动计算门控列表可能是不可能的，因此可能需要自动化。 自动门控配置器可以实现此目的。

用户需要为不同的流量类别指定约束，例如最大延迟，自动门控配置器会自动计算和配置满足这些约束的门控列表。

目前，INET 包含三个门调度配置器模型：
 
+ `EagerGateScheduleConfigurator <https://doc.omnetpp.org/inet/api-current/neddoc/inet.linklayer.configurator.gatescheduling.common.EagerGateScheduleConfigurator.html>`__ : 这是一个简易模型，它会快速生成门控列表。即使存在可行解，它也可能调度失败。 
+ `Z3GateScheduleConfigurator <https://doc.omnetpp.org/inet/api-current/neddoc/inet.linklayer.configurator.gatescheduling.z3.Z3GateScheduleConfigurator.html>`__ : 它使用基于SAT求解器的方法来查找满足延迟和抖动要求的解决方案。 
+ `TSNschedGateScheduleConfigurator <https://doc.omnetpp.org/inet/api-current/neddoc/inet.linklayer.configurator.gatescheduling.common.TSNschedGateScheduleConfigurator.html>`__ : 它使用外部工具而不是内置功能。 

以下示例演示了时间感知整形的门调度：

.. toctree::
    :maxdepth: 1
    :glob:

    Eager_Gate_Schedule_Configuration
    SAT-Solver-based_Gate_Schedule_Configuration
    TSNsched-based_Gate_Scheduling