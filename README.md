# IOT

物联网从整个体系结构来看，可以分为三个层面。  

第一是设备层，也就是各种硬件设备。  
设备组件有传感器，比如测量温度、湿度、光照强度等参数的设备；也有执行器，比如控制电路通断的继电器、实现物体移动的马达等。物联网设备，不仅涉及传统嵌入式系统的开发，而且也需要考虑通信技术，比如 Wi-Fi、蓝牙和蜂窝网络等。  

第二是网络层，主要关注的是设备与物联网平台的通信协议。  
物联网的网络通信仍然是基于互联网的，所以底层还是 TCP/IP 协议。应用中你更多需要了解、掌握的是具体的网络协议，比如 HTTP、MQTT 和 AMQP 等。  

第三是应用层，也就是实现具体业务逻辑的地方。  
除了像普通互联网后台一样，要面对服务器框架、数据库系统、消息队列等问题外，物联网系统首先需要处理的就是海量的数据。这又可以分为三个方面：  

1. 数据存储，比如 NoSQL 数据库和时序数据库的选择。
2. 数据处理，比如 Spark、Flink 等大数据处理框架的不同特点，批处理和流处理的适用场景等。
3. 数据分析，如各类机器学习算法，甚至 AI 的应用。

![IOT1](images/IOT1.jpg)

## 1. 通信协议之MQTT

MQTT是基于二进制消息的发布/订阅编程模式的消息协议，最早由IBM提出的，如今已经成为OASIS规范。由于规范很简单，非常适合需要低功耗和网络带宽有限的IoT场景，比如：  

遥感数据  
汽车  
智能家居  
智慧城市  
医疗医护  

由于物联网的环境是非常特别的，所以MQTT遵循以下设计原则：  

精简，不添加可有可无的功能。  
发布/订阅（Pub/Sub）模式，方便消息在传感器之间传递。  
允许用户动态创建主题，零运维成本。  
把传输量降到最低以提高传输效率。  
把低带宽、高延迟、不稳定的网络等因素考虑在内。  
支持连续的会话控制。  
理解客户端计算能力可能很低。  
提供服务质量管理。  
假设数据不可知，不强求传输数据的类型与格式，保持灵活性。  

运用MQTT协议，设备可以很方便地连接到物联网云服务，管理设备并处理数据，最后应用到各种业务场景，如下图所示：  

![IOT2](images/IOT2.png)

### 1.1. MQTT 协议原理

基于发布/订阅模式的 MQTT 协议中有三种角色：发布者（Publisher）、代理（Broker）、订阅者（Subscriber）。发布者向代理发布消息，代理向订阅者转发这些消息。通常情况下，客户端的角色是发布者和订阅者，服务器的角色是代理，但实际上，服务器也可能主动发布消息或者订阅主题，客串一下客户端的角色。  

为了方便理解，MQTT 传输的消息可以简化为：主题（Topic）和载荷（Payload）两部分：  

Topic，消息主题，订阅者向代理订阅主题后，一旦代理收到相应主题的消息，就会向订阅者转发该消息。  
Payload，消息载荷，订阅者在消息中真正关心的部分，通常是业务相关的。  

### 1.2. MQTT 协议基础概念

#### 1.2.1. 客户端 （Client）

使用 MQTT 协议的程序或设备。它可以  

打开连接到服务端的网络连接  
发布应用消息给其它相关的客户端  
订阅以请求接受相关的应用消息  
取消订阅以移除接受应用消息的请求  
关闭连接到服务端的网络连接  

#### 1.2.2. 服务器（Server）  

在发送消息的客户端与已订阅的客户端之间充当中介角色的程序或设备，它可以  

接受来自客户端的网络连接  
接受客户端发布的应用消息  
处理客户端的订阅和取消订阅请求  
转发应用消息给符合条件的已订阅客户端  
关闭来自客户端的网络连接  

#### 1.2.3. 会话（Session）  

每个客户端与服务器建立连接后就是一个会话，客户端和服务器之间有状态交互。会话可以存在于一个网络连接之间，也可以跨越多个连续的网络连接存在。  

#### 1.2.4. 订阅（Subscription）

订阅包含一个主题过滤器（Topic Filter）和一个最大的服务质量（QoS）等级。订阅与单个会话（Session）关联。会话可以包含多于一个的订阅。会话的每个订阅都有一个不同的主题过滤器。  

#### 1.2.5. 主题名（Topic Name）

附加在应用消息上的一个标签，被用于匹配服务端已存在的订阅。服务端会向所有匹配订阅的客户端发送此应用消息。  

#### 1.2.6. 主题过滤器（Topic Filter）

仅在订阅时使用的主题表达式，可以包含通配符，以匹配多个主题名。  

MQTT 主题的更多特性请访问我们的博文：MQTT 主题的高级特性。  

#### 1.2.7. 载荷（Payload）

对于 PUBLISH 报文来说载荷就是业务消息，它可以是任意格式（二进制、十六进制、普通字符串、JSON 字符串、Base64）的数据。  

### 1.3. MQTT 报文结构

MQTT 报文由三部分组成，分别为：固定报头（Fixed header）、可变报头（Variable header）以及有效载荷（Payload）。  

包含报文类型等字段的固定包头存在于所有 MQTT 报文中。可变报头的内容根据报文类型的不同而不同，一些报文中甚至不存在可变报头。有效载荷通常是与业务/场景相关的数据，例如对 PUBLISH 报文来说有效载荷就是应用消息，对 SUBSCRIBE 报文来说有效载荷就是订阅列表。  

MQTT 协议提供了 3 种消息服务质量等级（Quality of Service），它保证了在不同的网络环境下消息传递的可靠性。  

QoS 0：消息最多传递一次，如果当时客户端不可用，则会丢失该消息。  
QoS 1：消息传递至少 1 次。  
QoS 2：消息仅传送一次。  

消息中间件-消息代理（Broker）  

MQTT 协议工作过程中需要一个消息服务器，也称为消息代理（Broker），将消息存放在若干队列中，在合适的时候再将消息转发给接收设备。当接收设备收到信息触发事件完成相对应的操作。它有四个功能：  

1. 【网络连接】，接受来自客户端的网络连接请求
2. 【队列缓存消息数据】，保存客户端发布的数据信息
3. 【断开网络】，处理来自客户端的订阅和退订请求
4. 【消息数据转发】，向订阅的客户端转发数据信息

### 1.4. 开源 MQTT 服务器如何选择

到目前为止，比较流行的开源 MQTT 服务器有几个：

1. Eclipse Mosquitto  

使用 C 语言实现的 MQTT 服务器。Eclipse 组织还还包含了大量的 MQTT 客户端项目：https://www.eclipse.org/paho/#

2. EMQ X  

使用 Erlang 语言开发的 MQTT 服务器，内置强大的规则引擎，支持许多其他 IoT 协议比如 MQTT-SN、 CoAP、LwM2M 等。

3. Mosca  

使用 Node.JS 开发的 MQTT 服务器，简单易用。

4. VerneMQ  

同样使用 Erlang 开发的 MQTT 服务器.  

从支持 MQTT 5.0、稳定性、扩展性、集群能力等方面考虑，EMQ X 的表现应该是最好的：  

使用 Erlang OTP 开发，容错能力好 (电信领域久经考验的语言，曾经做出过 99.9999999% 可用性的交换机设备5)  
官方有大量的扩展插件可供扩展。有很多认证插件，数据存储(backend)插件可供选择。可支持各种关系型数据库，NoSQL 数据库，以及常见消息队列如 Kafka，RabbitMQ，Pulsar 等  
支持集群，支持节点水平扩展  
单节点支持 2000K 并发连接  
支持规则引擎和编解码  
