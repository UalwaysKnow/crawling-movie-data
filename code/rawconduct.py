import csv
import codecs
import matplotlib.pyplot as plt

#对比两个列表，返回其中相同元素到同一列表中
def contr(a,b):
    lst=[]
    for i in a:
        if i in b:
            lst.append(i)
        else:
            continue
    return lst
    
def main():
    #打开文件 读取豆瓣电影中的名称和评分
    #其中打开文件以utf-8格式读取
    count=[]
    name1=[]
    score1=[]
    csv_reader = csv.reader(open('DBmovie.csv', encoding='utf-8'))
    for line in csv_reader:
        name1.append(line[1])
        score1.append(line[2])
    name1.pop(0)
    score1.pop(0)
    #打开文件 读取猫眼电影中的名称和评分
    name2=[]
    score2=[]
    csv_reader = csv.reader(open('MYmovie.csv', encoding='utf-8'))
    for line in csv_reader:
        name2.append(line[1])
        score2.append(line[2])
    name2.pop(0)
    score2.pop(0)
    cou100=contr(name1,name2).copy()
    #生成count列表，储存榜单中同处于前num位的相同影片
    count.append(len(contr(name1,name2)))
    for i in [90,80,70,60,50,40,30,20,10]:
        a=name1.copy()
        b=name2.copy()
        del(a[i:])
        del(b[i:])
        count.append(len(contr(a,b)))
        if i==30:
            cou30=contr(a,b).copy()
        if i==10:
            cou10=contr(a,b).copy()
    #print(count)

    #打印一些信息
    print("***豆瓣和猫眼TOP榜单分析结果见统计图***")
    print("---------------------------------------")
    print("其中：")
    print("---同处于两份榜单TOP10有{}部，分别为：".format(count[-1]))
    print("-----------------")
    for i in cou10:
        print("{:^10}".format(i))
    print("-----------------")
    print("---同处于两份榜单TOP30有{}部，分别为：".format(count[-3]))
    print("-----------------")
    for i in cou30:
        print("{:^10}".format(i))
    print("-----------------")
    print("---同处于两份榜单TOP50/80/100有{}/{}/{}部".format(count[-5],count[-8],count[0]))
    print("-------其他略，见统计图-------")
    print("-----------------")
    print("Figure_1是豆瓣、猫眼两份榜单中TOP10/20/30/...的相同电影数目")
    print("Figure_2是豆瓣、猫眼两份榜单中TOP10/20/30/...的电影的相同率")
    print("Figure_3是豆瓣、猫眼两榜单TOP100中的相同电影的评分对比")
    print("通过figure_3可以看出，猫眼的评分变化曲线波动更加大，因此可知豆瓣的评分相比猫眼更加可靠")
    
    #开始绘制图表工作 第一个条形图
    #统计了TOP10/20/..中重复的影片数量
    xlabel=['TOP10','TOP20','TOP30','TOP40','TOP50','TOP60','TOP70','TOP80','TOP90','TOP100']
    xlabel.reverse()
    x=range(len(xlabel))
    plt.figure(1)
    plt.bar(x,count)
    plt.xticks(x,xlabel)
    plt.title('Number of repetition')
    plt.xlabel("DouBan TOP and TianMao TOP")
    #第二个条形图
    #反映了两个榜单的重复率
    per=[]
    nnum=[100,90,80,70,60,50,40,30,20,10]
    for i in range(10):
        num=count[i]*100/nnum[i]
        per.append(num)
    plt.figure(2)
    plt.bar(x,per)
    plt.xticks(x,xlabel)
    plt.title('Repetitive rate/%')
    plt.xlabel("DouBan TOP and TianMao TOP")
    #第三个 为折线图
    #对于两个榜单重复的66部电影，对于其评分进行对比
    y1=[]
    y2=[]
    for g in cou100:
        place=name1.index(g)
        y1.append(score1[place])
    for g in cou100:
        place=name2.index(g)
        y2.append(score2[place])
    plt.figure(3)
    x1=range(0,66)
    x2=range(0,66)
    plt.plot(x1,y1,label='DouBan line',linewidth=3,color='r',marker='o',markerfacecolor='blue') 
    plt.plot(x2,y2,label='MaoYan line') 
    plt.title('Coomparison:Rating scores of 66 films')
    plt.legend()
    #绘制三个统计图
    plt.show()  

if __name__=="__main__":
    main()
