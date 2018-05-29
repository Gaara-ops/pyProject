#coding:gbk
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def runplt():
    plt.figure()
    plt.title('piz prise and radius',fontsize=10)
    plt.xlabel('radius',fontsize=10)
    plt.ylabel('prise',fontsize=10)
    plt.axis([0,25,0,25])
    plt.grid(True)
    return plt

plt = runplt()
X = [[6],[8],[10],[14],[18]]
y = [[7],[9],[13],[17.5],[18]]
plt.plot(X,y,'k.')
# ~ plt.show()
X2 = [[0],[10],[14],[25]]
#create and predict
model = LinearRegression()
#LinearRegression的fit()方法学习一元线性回归模型：y = α + βx
# β=协方差/方差    α = y平均 - βx平均
model.fit(X,y)
y2 = model.predict(X2)
#残差平方和
print('residual sum of squares:%.2f' % np.mean((model.predict(X)-y)**2))
xbar = (6+8+10+14+18)/5
ybar = (7+9+13+17.5+18)/5
#求x的方差
variance = ((6-xbar)**2+(8-xbar)**2+(10-xbar)**2+(14-xbar)**2+(18-xbar)**2)/4
print(np.var([6,8,10,14,18],ddof=1))
#求x,y的协方差
print(np.cov([6,8,10,14,18],[7,9,13,17.5,18])[0][1])
# ~ y3 = [14.25,14.25,14.25,14.25]
# ~ y4 = y2 * 0.5 + 5
# ~ model.fit(X[1:-1],y[1:-1])
# ~ y5 = model.predict(X2)

plt.plot(X,y,'k.')
plt.plot(X2,y2,'g-.')
# ~ plt.plot(X2,y3,'r-.')
# ~ plt.plot(X2,y4,'y-.')
# ~ plt.plot(X2,y5,'o-.')
#residuals predict value残差预测值
yr = model.predict(X)
for idx,x in enumerate(X):
    plt.plot([x,x],[y[idx],yr[idx]],'r-')
plt.show()
# ~ print('a 12cun price:$%.2f' % model.predict([12])[0])
