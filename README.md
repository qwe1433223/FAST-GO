### 开源工具

> OneForAll，Web-SurvivalScan，403 ByPasser

## 作用

> 在SRC信息收集中，搜集到的子域可能有成千上万条，状态码为200的少说也有上百条，要是都对这些子域进行测试，那得产生几何倍数的请求（各种爆破）

> 好在有些站点是使用同一模板开发的，比如丁香园的资产，多个子域实际就是一台服务器中的同一个web，此时可以判断web的静态文件以及JS文件是否与另一个站点相同，来排除来自同一模板的资产。

> 在此基础上，我把一些开源工具给整合起来了，更方便进行资产处理

## 流程

```
OneForAll
FOFA处理
URLS_TO_IPS
存活扫描
资产去重
403_ByPasser
```

## 用法

### 1. 在工具运行目录创建一个项目文件夹

<img src="https://github.com/qwe1433223/FAST-GO/blob/main/img/image-20230826214018078.png" width="210px">

> 将FOFA导出的资产（csv格式的）放到这个项目内，导出的字段要包含：link
> 创建一个OneForAll目标界定.txt 文件，界定子域名爆破目标

<img src="https://github.com/qwe1433223/FAST-GO/blob/main/img/image-20230826214211393.png" width="210px">

### 2. PowerShell环境下运行 start.ps1

> ./start.ps1 项目名称(也就是刚刚创建的那个文件夹) 可选参数1或0
>
> 第二个可选参数选0就好，不用选1 

<img src="https://github.com/qwe1433223/FAST-GO/blob/main/img/QQ录屏20230826214941.gif" width="210px">

### 3.运行结束的样子，最后不建议对一大堆403资产进行ByPass

<img src="https://github.com/qwe1433223/FAST-GO/blob/main/img/image-20230826215225068.png" width="210px">

### 4.运行结果

> 包括各种状态的web，IPS，存活报告，以及去重的报告，后续进行SRC挖掘选择单独开发资产.txt里的目标进行测试就好，项目名.txt内是所有资产（未做存活扫描及去重），200.txt是状态码200的资产

<img src="https://github.com/qwe1433223/FAST-GO/blob/main/img/image-20230826215547561.png" width="210px">
