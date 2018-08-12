## 通用分类评估工具
本工具是通用的分类评估工具，**可以但不限于评估暴恐分类指标**，若要评估其他分类常景，只需修改类别映射文件即可，详见步骤1。   
评估指标包括：   
* accuracy
* 各类别recall和precision
* 混淆矩阵    
### 使用方法
**1. 准备类别映射文件** 
```
该文件定义了编号和类型之间的对应关系，格式规范为：
编号\t类别名，例如
0	bloodiness
1	bomb
2	beheaded
3	march
4	fight
5	normal
注：编号必须从0依次+1递增
```
默认的暴恐6分类文件见label.txt文件，若有变更，按需修改即可。   
**2. 准备标注好的数据**   
数据为符合LabelX规范的json文件   
**3. 准备推理结果**   
每行一个结果，格式为:图片名\t类别，例如    
```
pulp_normal_0318_00327794.jpg	bomb
pulp_normal_0318_00110128.jpg	normal
1027cb0ad867c4ee268d4e7a37d48fb7.jpg	fight
```
**4. 运行eval.py**
```
usage: terror class evaluation tool [-h] --gt GT --log LOG --label LABEL
                                    [--verbose]

optional arguments:
  -h, --help     show this help message and exit
  --gt GT        LabelX标注过的json文件
  --log LOG      日志文件，每行一个结果（name class）
  --label LABEL  标签映射文件（index classname）
  --verbose      指定时绘制混淆矩阵
  ```
### 运行结果
**1. 暴恐分类**   
当类别映射文件为暴恐6分类时，输出形如
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
accuracy:      0.875000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bloodiness_recall:     1.000000
bloodiness_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bomb_recall:     1.000000
bomb_precision:  0.500000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
beheaded_recall:     0.666667
beheaded_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
march_recall:     1.000000
march_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fight_recall:     1.000000
fight_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
normal_recall:     1.000000
normal_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Confusion Matrix
[[1 0 0 0 0 0]
 [0 1 0 0 0 0]
 [0 1 2 0 0 0]
 [0 0 0 1 0 0]
 [0 0 0 0 1 0]
 [0 0 0 0 0 1]]
```
指定--verbose参数时，混淆矩阵可绘制如下   
![confusion_matrix.png](pic/terror_confusion_matrix.png)   
**2. 其他分类**   
若评估其他分类，只需修改label文件即可，例如，四分类评估，只需修改label.txt如下
```
0	Class_A
1	Class_B
2	Class_C
3	Class_D

运行即可产生四分类评估结果
class evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
accuracy:      0.714286
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Class_A_recall:     0.666667
Class_A_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Class_B_recall:     0.500000
Class_B_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Class_C_recall:     1.000000
Class_C_precision:  0.333333
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Class_D_recall:     1.000000
Class_D_precision:  1.000000
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Confusion Matrix
[[2 0 1 0]
 [0 1 1 0]
 [0 0 1 0]
 [0 0 0 1]]
```
![confusion_matrix.png](pic/common_confusion_matrix.png) 
