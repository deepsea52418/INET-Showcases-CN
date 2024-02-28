Automatic Gate Schedule Configuration 自动门控配置
==================================================

在时间感知整形中，可以手动指定门时间表（即对应不同流量类别的门何时打开或关闭）。 在一些简单的情况下这可能就足够了。 然而，在复杂的情况下，手动计算登机口时间表可能是不可能的，因此可能需要自动化。 门时间表配置器可用于此目的。

人们需要为不同的流量类别指定约束，例如最大延迟，配置器会自动计算和配置满足这些约束的门时间表。

目前，INET 包含三个门调度配置器模型：
- :ned:`EagerGateScheduleConfigurator`: 这是一个简易模型，它会快速生成门控列表。即使存在可行解，它也可能调度失败。
- :ned:`Z3GateScheduleConfigurator`: 它使用基于SAT求解器的方法来查找满足延迟和抖动要求的解决方案。
- :ned:`TSNschedGateScheduleConfigurator`: 它使用外部工具而不是内置功能。

以下示例演示了时间感知整形的门调度：

.. toctree::

    Eager Gate Schedule Configuration
    SAT-Solver-based Gate Schedule Configuration
    TSNsched-based Gate Scheduling