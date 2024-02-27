独立使用流量整形器1
====================

目标
----

在INET框架中，调度和流量整形模块可以独立于网络节点运行。以这种方式利用这些模块的优势在于轻松构建和验证复杂的调度和流量整形行为，这在全面的网络设置中可能很难复制。

在这个演示中，我们演示了通过直接连接其各个组件来创建一个完全运行的异步流量整形器（ATS）。接下来，我们通过将ATS链接到流量源和流量汇之间，构建了一个简单的排队网络。关键亮点是观察网络内的流量整形，通过在整形过程之前和之后绘制生成的流量来实现。

| INET版本： ``4.4``
| 源文件位置： `inet/showcases/tsn/trafficshaping/underthehood <https://github.com/inet-framework/inet/tree/master/showcases/tsn/trafficshaping/underthehood>`__


.. raw::html
    <iframe src="//player.bilibili.com/player.html?aid=283448464&bvid=BV1Wc411t7TD&cid=1399372456&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>


