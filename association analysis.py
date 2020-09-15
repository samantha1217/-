# -*- coding:gbk -*-
from sklearn.feature_extraction import DictVectorizer
from dask.array.chunk import arange
import time  # 引入time模块
# from apriori2 import apriori

SUPPORT_DIVIDER = ","

CONFIDENCE_DIVIDER = "=>"

'''
构建模型
'''


class Apriori():
    def __init__(self, dataSet, minSupport, minConfidence):
        self.vec = DictVectorizer()
        '''最小支持度'''
        self.minSupport = minSupport
        '''最小置信度'''
        self.minConfidence = minConfidence
        '''整个列表，数组的行表示单个特证向量，里面的特证不重复，而且每一行的长度有可能不一样'''
        self.dataSet = dataSet
        self.numOfTypes = len(dataSet)
        '''构建所有种类出现的次数'''
        self.dataTypeMap = {}
        '''初始化一项式'''
        self.dataTypeMap[1] = createTrainSet(self.dataSet)


'''
构学无监督学习的数据
'''


def createTrainSet(dataTypeMap):
    dataTypeMapResult = {}
    for row in range(len(dataTypeMap)):
        rowValues = dataTypeMap[row]
        rowValues.sort()
        for column in range(len(rowValues)):
            value = str(rowValues[column])
            if value in dataTypeMapResult:
                '''更新当前键出现的次数'''
                dataTypeMapResult[value] = dataTypeMapResult[value] + 1
            else:
                '''第一次出现的数据值为1'''
                dataTypeMapResult[value] = 1
    return dataTypeMapResult


'''
analize_x 为n*k列距阵
'''


def analize(dataSet, minSupport=0.15, minConfidence=0.7):
    row = 2
    apriori = Apriori(dataSet, minSupport, minConfidence)
    '''从C(2, n), C(3, n)....到C(n, n)'''
    while True:
        if innerLoop(apriori, row) == 0:
            break
        row = row + 1
    '''生成关规则'''
    generateRule(apriori)
    return apriori


'''
计算通过k-1项，计算k项的数据
'''


def innerLoop(apriori, kSet):
    '''候选 k项式修选集'''
    kSetItems = {}
    beforeLenght = len(kSetItems)

    '''选择k项式的值'''
    print("选择{0}项式的值开始...".format(kSet))
    startTime = time.time()
    scanKMinusItems(kSetItems, apriori, kSet)
    print("获取候选{0}项式时间：".format(kSet) + str(time.time() - startTime))

    '''对候选集进行剪枝'''
    print("剪枝开始,剪枝数量{0}...".format(len(kSetItems)))
    startTime = time.time()
    sliceBranch(kSetItems, apriori)
    print("剪枝花费时间:" + str(time.time() - startTime))
    '''存在下一个key_set,则放在结果中'''
    afterLength = len(kSetItems)
    if afterLength != beforeLenght:
        apriori.dataTypeMap[kSet] = kSetItems
        return 1
    else:
        return 0


'''
通过1项式和k-1项式生成k项式
'''


def scanKMinusItems(kSetItems, apriori, kSet):
    '''频集1项式和k-1项式，组成新的k项式，然后把不满足的项式去掉'''
    '''频集1项式'''
    keys = list(apriori.dataTypeMap[1].keys())

    '''k-1项式,,1项式和k-1项式组成k项式'''
    kMinusOneKeys = list(apriori.dataTypeMap[kSet - 1].keys())
    '''生成候选集'''
    for row in range(len(keys)):
        for column in range(len(kMinusOneKeys)):
            '''2项式时，由于1项式和1项式进行组合，需要去除相同的组合数'''
            if kSet == 2 and row == column:
                continue
            calc(keys[row], kMinusOneKeys[column], kSetItems)


'''
生成候选频繁集
@param oneDataSetKey:             1项式的key值
@param dataSet:                   训练集1项式
@param kMinusOneItemKey:          k - 1项式的key值
@param kDataSetItems:             k项式map数据
'''


def calc(oneDataSetKey, kMinusOneItemKey, kDataSetItems):
    if kMinusOneItemKey.find(oneDataSetKey) != -1:
        return
    kDataSetItemKeys = kMinusOneItemKey + SUPPORT_DIVIDER + str(oneDataSetKey)
    '''分割成数组,再进行排序'''
    kItemKeys = kDataSetItemKeys.split(SUPPORT_DIVIDER)
    kItemKeys.sort()
    '''list合成字段串'''
    kDataSetItemKeys = SUPPORT_DIVIDER.join(kItemKeys)
    '''kDataSetItemKeys初始值为0'''
    if kDataSetItemKeys in kDataSetItems.keys():
        kDataSetItems[kDataSetItemKeys] += 1
    else:
        kDataSetItems[kDataSetItemKeys] = 0


'''
对后选频烦集进行剪枝
@param kDataSetItems
'''


def sliceBranch(kDataSetItems, apriori):
    kItemKeyArrays = list(kDataSetItems.keys())
    '''计算kItemKeys数组里面的所有元素同时在dataSet中出现的次数'''
    dataSets = {}
    for kItemKeys in kItemKeyArrays:
        kItemKeyArray = kItemKeys.split(SUPPORT_DIVIDER)
        kDataSetItemCount = 0
        setData = set(kItemKeyArray)
        for rowIndex in range(len(apriori.dataSet)):
            if rowIndex in dataSets:
                rowArray = dataSets[rowIndex]
            else:
                rowArray = set(apriori.dataSet[rowIndex])
                dataSets[rowIndex] = rowArray
            '''长度大于数据长度'''
            if len(rowArray) < len(kItemKeyArray):
                continue
            '''判断所有元素是否都在列表中同时存在'''
            if setData.issubset(set(rowArray)):
                kDataSetItemCount += 1
        '''小于最小支持度，则不添加到列表中'''
        if apriori.minSupport > kDataSetItemCount / apriori.numOfTypes:
            del kDataSetItems[kItemKeys]
        else:
            kDataSetItems[kItemKeys] = kDataSetItemCount


'''
计算置信度
@param kDataSetItems:    频集数据集{1:{'1, 2, 3':次数}}
@param apriori:          关联数据类
'''


def generateRule(apriori):
    cacheKeySet = {}
    resultConfidence = {}
    '''key是频集集合,value代表是K项式的k值'''
    for key in apriori.dataTypeMap:
        if key == 1:
            continue
        innerMap = apriori.dataTypeMap[key]
        for innerKey in innerMap:
            keyArray = innerKey.split(SUPPORT_DIVIDER)
            generateRule2(apriori, keyArray, innerMap[innerKey], resultConfidence, len(keyArray) - 1)


'''
目标繁集项和源繁集项两两结合在一起
@param kDataSetItems:     二项式繁集项
@param targetItems:       某个目标繁集
@param sourceItems:       源繁集项
'''


def generateRule2(apriori, targetItems, supportTargetItems, resultConfidence, childIndex):
    if childIndex <= 0:
        return
    dataMap = apriori.dataTypeMap
    '''数据长度'''
    dataLength = len(targetItems)
    totalSets = set(targetItems)
    '''构造targetItems非空真子集,并计算至信度'''
    for index in range(dataLength):
        '''超过了数组长度'''
        if index + childIndex > dataLength:
            break
        '''从index开始取childIndex个数据表示是leftDataSet'''
        leftDataArray = targetItems[index:childIndex + index]
        leftDataArray.sort()
        '''取总列表与左边的列表相减，就是右列key'''
        rightDataArray = list(totalSets ^ set(leftDataArray))
        rightDataArray.sort()

        leftDataKeyString = SUPPORT_DIVIDER.join(leftDataArray)
        rightDataKeyString = SUPPORT_DIVIDER.join(rightDataArray)

        '''不存在数量为数组长度的频集'''
        if (len(leftDataArray) not in dataMap) or (len(rightDataArray) not in dataMap):
            continue

        '''非频集'''
        if (leftDataKeyString not in dataMap[len(leftDataArray)]) or \
                (rightDataKeyString not in dataMap[len(rightDataArray)]):
            continue

        '''leftDataKey出现的时,rightDataKeyString出现的概率,即频集列表中两个出现的数量'''
        confidence = supportTargetItems / \
                     dataMap[len(leftDataArray)][leftDataKeyString]
        if confidence > apriori.minConfidence:
            '''置信度大于阀值'''
            print("{0}===>>{1}: confidence = {2}".format(leftDataKeyString, rightDataKeyString, str(confidence)))
            resultConfidence[leftDataKeyString + CONFIDENCE_DIVIDER + rightDataKeyString] = confidence
        else:
            '''置信度小于阀值,放在ignore例表中，用于下次判'''
    '''递规的方式云偏历'''
    generateRule2(apriori, targetItems, supportTargetItems, resultConfidence, childIndex - 1)
