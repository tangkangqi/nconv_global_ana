# nconv_global_ana
Anlays of nconv confirmed case number by timeseries in different countries  
# 新冠全球数据分析
本文采用的中国CDC和约翰霍普金斯的全球新冠数据，对确诊病例数前30各国/地区的新冠确诊时序数据做了一个挖掘分析。

先放结论图：
![4各国家地区确诊病例突破100人后的时序增长图-对数拟合](img/4各国家地区确诊病例突破100人后的时序增长图-对数拟合.png)

这张图包含了不少信息：

- 东亚目前较为稳定，韩国（绿色点虚线）应该到拐点了，这个月底会控制下来，最终确诊数可能与我国除湖北（绿色星点虚线）外相同
- 欧美还在爆发期，最终确诊数可能远超我国包括湖北...

# 数据分析流程：
## 获取数据：
我们采用John Hopkins 整理的全球新冠疫情数据：https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv    
这个数据是实时更新的
​
### 数据清洗、本地化：
主要是选取疫情最严重的前30个地区，为了方便中文读者， 国家名转化为中文名。
```python
df0 = pd.read_csv('time_series_19-covid-Confirmed.csv')
dates = ['%s月%s日' % (v1[0], v1[1]) for v1 in [v.split('/')[:2] for v in df0.columns[4:]]]
dates = [(df0.columns[4:][i], dates[i]) for i in range(len(dates))]
df0 = df0.rename(columns=dict(dates))
df1 = df0.groupby('Country/Region').sum().reset_index()

top30_cn_str = '''中国大陆 意大利 伊朗 韩国 法国 西班牙 美国 德国 钻石公主号邮轮 日本 瑞士 挪威 英国 荷兰 瑞典 比利时 丹麦 奥地利 新加坡 马来西亚 香港特别行政区 巴林王国 澳大利亚 希腊 加拿大 阿联酋 伊拉克 科威特 冰岛 埃及'''
top30_cn = top30_cn_str.split(' ')
names = ['Mainland China', 'Italy', 'Iran (Islamic Republic of)',
         'Republic of Korea', 'France', 'Spain', 'US', 'Germany', 'Others',
         'Japan', 'Switzerland', 'Norway', 'UK', 'Netherlands', 'Sweden',
         'Belgium', 'Denmark', 'Austria', 'Singapore', 'Malaysia',
         'Hong Kong SAR', 'Bahrain', 'Australia', 'Greece', 'Canada',
         'United Arab Emirates', 'Iraq', 'Kuwait', 'Iceland', 'Egypt']
```

### 数据聚合
数据可视化选取，和模型拟合分析这里略去（具体可查看代码）

## 数据可视化
### 线性坐标系
这是在普通线性坐标系里的各国增长图：
![1各国家地区确诊病例突破100人后的时序增长图](img/1各国家地区确诊病例突破100人后的时序增长图.png)

### 对数坐标系

普通坐标系中很难看出关联， 我们试一下对数坐标系，可以挖掘不少insight：
![2各国家地区确诊病例突破100人后的时序增长图-对数](img/2各国家地区确诊病例突破100人后的时序增长图-对数.png)

在对数坐标下，隐藏的增长关系被暴露了，每一条曲线前期都是直线，显示很明显的线性回归。
而曲线的斜率就是日增长率。

我们可以看到：

- 在左上方密集曲线， 欧美各国+伊朗的数据都与中国平行。

- 但是也有三组离群曲线：钻石公主号， 日本，新加坡和中国香港。


## 拟合分析
### 模型选取
我采用的是简单的指数拟合 $y=a^x$,
有效的依据是各传染病模型在初期都可以近似为指数增长(类似于高中生物的种群增长曲线)：
![种群增长曲线](img/种群增长曲线.jpg)
图片源自[百度](https://bkimg.cdn.bcebos.com/pic/78310a55b319ebc4f14ae9a08e26cffc1e1716dc?x-bce-process=image/resize,m_lfit,w_268,limit_1/format,f_jpg)

典型的传染病传播数学模型，无论是SI模型还是SIRS、SERI，都类似logistic函数。

此外，历史增长数据在对数坐标系中为直线也证实了我们的结论。

### 指数拟合
我们拟合的结果如下：
![4各国家地区确诊病例突破100人后的时序增长图-对数拟合](img/4各国家地区确诊病例突破100人后的时序增长图-对数拟合.png)

### 模型分析
增长速度可以分为三大类， 分别对应翻倍天数为2天， 7天， 25天。

1.51大概等于根号2， 也就是说zh。
我倾向于认为是这个病毒感染到确诊需要一定的时间，欧美现在和我们早期都未采取措施， 所以是指数增长， 那么可以认为在无防护的情况下，新冠肺炎的日增长率是1.51。
注：这里日增长率不是R0， R0是一个患者平均总感染其他人数， 据说新冠的R0是3左右。不过采用日增长率显然更直观。当然翻倍天数更直观。

日本和新加坡、香港特别行政区日增长倍数分别是1.1和1.03，当然有些过于低，但病例出现时间这么长了，我倾向于认为数据是真的。这些地区早期人数控制的比较好， 而且防护意识比较强， 新加坡和港澳台据报道比我们更早防护， 另外东亚有戴口罩卫生习惯，文化对待陌生人相对于欧美更内敛和距离感，可能是偏低的原因；而我们在爆发前期刚好是春运，韩国的宗教集会可能是偏高的原因。


（也不排除欧美情况已经失控，故意根据中国早期增长情况调整数据公开，因为这个1.51实在是太一致了...)


### 增长趋势
韩国（绿色星号点）有变缓趋势
其他国家还是一条直线

# 
本文也可以看成一个典型的数据分析案例。欢迎感兴趣的读者深入挖掘。