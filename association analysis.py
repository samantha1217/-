# -*- coding:gbk -*-
from sklearn.feature_extraction import DictVectorizer
from dask.array.chunk import arange
import time  # ����timeģ��
# from apriori2 import apriori

SUPPORT_DIVIDER = ","

CONFIDENCE_DIVIDER = "=>"

'''
����ģ��
'''


class Apriori():
    def __init__(self, dataSet, minSupport, minConfidence):
        self.vec = DictVectorizer()
        '''��С֧�ֶ�'''
        self.minSupport = minSupport
        '''��С���Ŷ�'''
        self.minConfidence = minConfidence
        '''�����б�������б�ʾ������֤�������������֤���ظ�������ÿһ�еĳ����п��ܲ�һ��'''
        self.dataSet = dataSet
        self.numOfTypes = len(dataSet)
        '''��������������ֵĴ���'''
        self.dataTypeMap = {}
        '''��ʼ��һ��ʽ'''
        self.dataTypeMap[1] = createTrainSet(self.dataSet)


'''
��ѧ�޼ලѧϰ������
'''


def createTrainSet(dataTypeMap):
    dataTypeMapResult = {}
    for row in range(len(dataTypeMap)):
        rowValues = dataTypeMap[row]
        rowValues.sort()
        for column in range(len(rowValues)):
            value = str(rowValues[column])
            if value in dataTypeMapResult:
                '''���µ�ǰ�����ֵĴ���'''
                dataTypeMapResult[value] = dataTypeMapResult[value] + 1
            else:
                '''��һ�γ��ֵ�����ֵΪ1'''
                dataTypeMapResult[value] = 1
    return dataTypeMapResult


'''
analize_x Ϊn*k�о���
'''


def analize(dataSet, minSupport=0.15, minConfidence=0.7):
    row = 2
    apriori = Apriori(dataSet, minSupport, minConfidence)
    '''��C(2, n), C(3, n)....��C(n, n)'''
    while True:
        if innerLoop(apriori, row) == 0:
            break
        row = row + 1
    '''���ɹع���'''
    generateRule(apriori)
    return apriori


'''
����ͨ��k-1�����k�������
'''


def innerLoop(apriori, kSet):
    '''��ѡ k��ʽ��ѡ��'''
    kSetItems = {}
    beforeLenght = len(kSetItems)

    '''ѡ��k��ʽ��ֵ'''
    print("ѡ��{0}��ʽ��ֵ��ʼ...".format(kSet))
    startTime = time.time()
    scanKMinusItems(kSetItems, apriori, kSet)
    print("��ȡ��ѡ{0}��ʽʱ�䣺".format(kSet) + str(time.time() - startTime))

    '''�Ժ�ѡ�����м�֦'''
    print("��֦��ʼ,��֦����{0}...".format(len(kSetItems)))
    startTime = time.time()
    sliceBranch(kSetItems, apriori)
    print("��֦����ʱ��:" + str(time.time() - startTime))
    '''������һ��key_set,����ڽ����'''
    afterLength = len(kSetItems)
    if afterLength != beforeLenght:
        apriori.dataTypeMap[kSet] = kSetItems
        return 1
    else:
        return 0


'''
ͨ��1��ʽ��k-1��ʽ����k��ʽ
'''


def scanKMinusItems(kSetItems, apriori, kSet):
    '''Ƶ��1��ʽ��k-1��ʽ������µ�k��ʽ��Ȼ��Ѳ��������ʽȥ��'''
    '''Ƶ��1��ʽ'''
    keys = list(apriori.dataTypeMap[1].keys())

    '''k-1��ʽ,,1��ʽ��k-1��ʽ���k��ʽ'''
    kMinusOneKeys = list(apriori.dataTypeMap[kSet - 1].keys())
    '''���ɺ�ѡ��'''
    for row in range(len(keys)):
        for column in range(len(kMinusOneKeys)):
            '''2��ʽʱ������1��ʽ��1��ʽ������ϣ���Ҫȥ����ͬ�������'''
            if kSet == 2 and row == column:
                continue
            calc(keys[row], kMinusOneKeys[column], kSetItems)


'''
���ɺ�ѡƵ����
@param oneDataSetKey:             1��ʽ��keyֵ
@param dataSet:                   ѵ����1��ʽ
@param kMinusOneItemKey:          k - 1��ʽ��keyֵ
@param kDataSetItems:             k��ʽmap����
'''


def calc(oneDataSetKey, kMinusOneItemKey, kDataSetItems):
    if kMinusOneItemKey.find(oneDataSetKey) != -1:
        return
    kDataSetItemKeys = kMinusOneItemKey + SUPPORT_DIVIDER + str(oneDataSetKey)
    '''�ָ������,�ٽ�������'''
    kItemKeys = kDataSetItemKeys.split(SUPPORT_DIVIDER)
    kItemKeys.sort()
    '''list�ϳ��ֶδ�'''
    kDataSetItemKeys = SUPPORT_DIVIDER.join(kItemKeys)
    '''kDataSetItemKeys��ʼֵΪ0'''
    if kDataSetItemKeys in kDataSetItems.keys():
        kDataSetItems[kDataSetItemKeys] += 1
    else:
        kDataSetItems[kDataSetItemKeys] = 0


'''
�Ժ�ѡƵ�������м�֦
@param kDataSetItems
'''


def sliceBranch(kDataSetItems, apriori):
    kItemKeyArrays = list(kDataSetItems.keys())
    '''����kItemKeys�������������Ԫ��ͬʱ��dataSet�г��ֵĴ���'''
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
            '''���ȴ������ݳ���'''
            if len(rowArray) < len(kItemKeyArray):
                continue
            '''�ж�����Ԫ���Ƿ����б���ͬʱ����'''
            if setData.issubset(set(rowArray)):
                kDataSetItemCount += 1
        '''С����С֧�ֶȣ�����ӵ��б���'''
        if apriori.minSupport > kDataSetItemCount / apriori.numOfTypes:
            del kDataSetItems[kItemKeys]
        else:
            kDataSetItems[kItemKeys] = kDataSetItemCount


'''
�������Ŷ�
@param kDataSetItems:    Ƶ�����ݼ�{1:{'1, 2, 3':����}}
@param apriori:          ����������
'''


def generateRule(apriori):
    cacheKeySet = {}
    resultConfidence = {}
    '''key��Ƶ������,value������K��ʽ��kֵ'''
    for key in apriori.dataTypeMap:
        if key == 1:
            continue
        innerMap = apriori.dataTypeMap[key]
        for innerKey in innerMap:
            keyArray = innerKey.split(SUPPORT_DIVIDER)
            generateRule2(apriori, keyArray, innerMap[innerKey], resultConfidence, len(keyArray) - 1)


'''
Ŀ�귱�����Դ���������������һ��
@param kDataSetItems:     ����ʽ������
@param targetItems:       ĳ��Ŀ�귱��
@param sourceItems:       Դ������
'''


def generateRule2(apriori, targetItems, supportTargetItems, resultConfidence, childIndex):
    if childIndex <= 0:
        return
    dataMap = apriori.dataTypeMap
    '''���ݳ���'''
    dataLength = len(targetItems)
    totalSets = set(targetItems)
    '''����targetItems�ǿ����Ӽ�,���������Ŷ�'''
    for index in range(dataLength):
        '''���������鳤��'''
        if index + childIndex > dataLength:
            break
        '''��index��ʼȡchildIndex�����ݱ�ʾ��leftDataSet'''
        leftDataArray = targetItems[index:childIndex + index]
        leftDataArray.sort()
        '''ȡ���б�����ߵ��б��������������key'''
        rightDataArray = list(totalSets ^ set(leftDataArray))
        rightDataArray.sort()

        leftDataKeyString = SUPPORT_DIVIDER.join(leftDataArray)
        rightDataKeyString = SUPPORT_DIVIDER.join(rightDataArray)

        '''����������Ϊ���鳤�ȵ�Ƶ��'''
        if (len(leftDataArray) not in dataMap) or (len(rightDataArray) not in dataMap):
            continue

        '''��Ƶ��'''
        if (leftDataKeyString not in dataMap[len(leftDataArray)]) or \
                (rightDataKeyString not in dataMap[len(rightDataArray)]):
            continue

        '''leftDataKey���ֵ�ʱ,rightDataKeyString���ֵĸ���,��Ƶ���б����������ֵ�����'''
        confidence = supportTargetItems / \
                     dataMap[len(leftDataArray)][leftDataKeyString]
        if confidence > apriori.minConfidence:
            '''���Ŷȴ��ڷ�ֵ'''
            print("{0}===>>{1}: confidence = {2}".format(leftDataKeyString, rightDataKeyString, str(confidence)))
            resultConfidence[leftDataKeyString + CONFIDENCE_DIVIDER + rightDataKeyString] = confidence
        else:
            '''���Ŷ�С�ڷ�ֵ,����ignore�����У������´���'''
    '''�ݹ�ķ�ʽ��ƫ��'''
    generateRule2(apriori, targetItems, supportTargetItems, resultConfidence, childIndex - 1)
