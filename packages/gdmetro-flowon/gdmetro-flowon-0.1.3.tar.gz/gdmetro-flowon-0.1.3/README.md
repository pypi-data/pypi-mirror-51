# gdflowon

  包含使用DAG描述的自动流模型渲染工具、样品信息表的定义等，可通过简单的配置结合样品信息表中的 `subproject`、`sample`、`lane`等模型快速地描述分析流程。

## 渲染DAG及绑定顶点活动的资源

以子项目为单位，通过配置中的顶点模板映射DAG的各个顶点。首先需要定义顶点的模板，顶点模板包含以下元素：

```yml
<顶点类型>:
    scope: <资源类型>  # 指定该顶点类型使用到的资源类型：`subproject` | `sample` | `lane`
    dependencies: <依赖到的顶点类型>

```

以WGS分析流程为例，人工操作需要完成以下步骤：

1. 按Lane上传，无依赖项
2. 按Lane比对，依赖绑定的资源（Lane）上传完成
3. 按样本WGS分析，依赖绑定的资源（样本下所有Lane）全部比对完成
4. 按整个子项目合并处理报告，依赖绑定的资源（子项目下所有的样本）全部分析完成
5. 按整个子项目下载结果，依赖绑定的资源（子项目）报告处理完成

```yml
upload:
    scope: lane
    dependencies: null

mapping:
    scope: lane
    dependencies: upload

wgs:
    scope: sample
    dependencies: mapping

report:
    scope: subproject
    dependencies: wgs

download:
    scope: subproject
    dependencies: report
```

样品信息表 <-> DAG的映射方式如下：

![](http://gitlab.genedock.com/liberate861/gdmetro-flowon/raw/master/doc/通过子项目映射到DAG.png)

```PlantUML
@startuml 通过子项目映射到DAG
!includeurl https://raw.githubusercontent.com/xuanye/plantuml-style-c4/master/core.puml
start
:子项目/
split
    :子项目下的Lane列表/
    :映射|
    :顶点列表(upload)/
split again
    :子项目下的Lane列表/
    :映射|
    :顶点列表(mapping)/
split again
    :子项目下的样品列表/
    :映射|
    :顶点列表(wgs)/
split again
    :子项目/
    :映射|
    :顶点(report)/
split again
    :子项目/
    :映射|
    :顶点(download)/
end split

:处理依赖关系，生成DAG;
stop
@enduml
```

## 使用方式

```python
from gdflowon import dag

# flow_config: 使用DAG描述的流程模板
# subproject: 样品信息表
graph = dag.subproject_2_dag(subproject, flow_config)
```
