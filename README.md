"# compareImage" 
1. 首先安装同其他第三方库，直接 pip install pillow ,from PIL import Image 如果没有报错则说明安装成功
2. histogram()是图片直方图，返回一个列表；
	```	
	 math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))/len(histogram1))
	 这个表达式获得结果是 一个 histogram1[i] - histogram2[i] 相减的结果平方的新的列表，结果再除以n
	 最后得到differ,如果两张图 一模一样那么最终结果differ应该是0，即differ越小，图片越相似（甚至相同），differ越大，图片差异越大
	```	
3. 圈出不同的点
    * 参考文章：https://blog.csdn.net/ibaymin/article/details/74936742?utm_source=blogxgwz0
	