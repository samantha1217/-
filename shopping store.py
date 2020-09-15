#!/usr/bin/env python

# coding:utf-8

import shelve

import time

shop_list = {  # 定义商品清单

    '数码电器': {'电脑': '8000', '照相机': '10000', '手机': '3800', '打印机': '3600'},

    '服装百货': {'牛仔裤': '288', '夹克': '300', '王老吉': '6', '方便面': '4'},

    '汽车': {'特斯拉': '999999', '宝马X5': '550000', '帕沙特': '250000', '奇瑞': '100000'},

    '化妆品': {'欧莱雅': '888', '欧诗漫': '666', '韩束': '388', '百雀羚': '259'},

}

count = 0  # 定义一个计数器

jiage = []

shop_list1 = {}

shop_name = list(shop_list.keys())  # 将商品第一层清单数据类型转换为列表

lock_file = open('file_lock.txt', 'r+')

user_pass = open('username_file.txt', 'r+')

count = 0


def show_list():  # 打印序列号与商品分类清单

    for i, j in enumerate(shop_list):
        print('%d:%s' % (i, j))


def show_menu(user_choise):  # 打印序列号与商品第二层清单

    user_choise = int(user_choise)

    a = shop_name[user_choise]

    for index, key in enumerate(shop_list[a]):  # 打印序列号与商品第二层清单

        print('%d:%s %s' % (index, key, shop_list[a][key]))


def show_menu2(user_choise, user_choise2):  # 调用用户第一次选择和第二次选择，进入对应的购物列表

    user_choise = int(user_choise)

    if user_choise2.isdigit() and int(user_choise2) < len(
            shop_list[shop_name[int(user_choise)]]):  # 判断用户输入的是否为数字，并小于商品序列号

        user_choise2 = int(user_choise2)

    # if user_choise2==0:

    jiage.clear()

    for v, k in enumerate(shop_list[shop_name[user_choise]]):  # 获取用户进入第二层商品的清单

        jiage.append(shop_list[shop_name[user_choise]][k])  # 将获取的商品清单存入列表中

    jiage2 = (int(jiage[user_choise2]))

    global jiage2


def quit_time():  # 查询完成后退出

    for i in [3, 2, 1]:
        print('\033[32;1m查询完毕，正在返回主菜单.....\033[1m', i)

        time.sleep(1)


def start():
    while True:

        if user_choise.isdigit() and int(user_choise):
            show_menu(user_choise)  # 调用show_menu函数，

            break

        else:

            print('\033[31;1m无效选项，请重新输入\033[1m')  # 用户重新输入

            break


########################################################################################################################

while count < 3:  # 只要重试不超过3次就不断循环

    print('\033[31;1m默认用户名密码为：pan,123 li,123\033[1m')

    username = input('\033[34;1m请输入您的用户名:\033[1m')

    for i in lock_file.readlines():  # 判断用户名是否在锁文件中

        i = i.split()

        if username in i[0]:
            print('\033[31;1m对不起 %s 已锁定\033[1m' % username)

            exit()

    match = False

    for j in user_pass.readlines():

        user, password = j.strip('\n').split()  # 去掉每行多余的\n并把这一行按空格分成两列，分别赋值为user,passwd两个变量

        if username == user:  # 判断输入的用户是否存在

            passwd = input('\033[30;1m请输入密码:')

            if password == passwd:

                match = True

                break



            elif password != passwd:  # 在用户名正确的前提下，判断输入的密码是否正确

                for i in range(2):

                    passwd = input('\033[31;1m密码错误，请重新输入密码:\033[1m')

                if password == passwd:

                    match = True

                    break

                else:

                    print('\033[31;1m密码和用户名不匹配，尝试超过三次，用户被锁定\033[1m')

                lock_file.write('%s \n' % username)

                lock_file.close()

                user_pass.close()

                exit()

    if username != user:

        print('\033[31;1m您输入用户名不存在,程序已退出\033[1m')

        exit()

    elif match == True:

        break

########################################################################################################################

f = shelve.open('user.db', 'c+')

try:

    if f[user] > 0:

        pay = f[user]

        chong_zhi = input('\033[33;1m您的当前余额为%d,是否充值？充值请输入您要充值的金额，任意键进入下一步，退出程序请按q：\033[1m' % f[user])

        if chong_zhi.isdigit() and int(chong_zhi) > 0:
            pay = int(chong_zhi) + int(pay)

            print('\033[35;1m充值后金额为\033[1m', pay)

except KeyError:

    chong_zhi = input('\033[36;1m您的当前余额为0,是否充值？充值请输入您要充值的金额，退出程序请按q：\033[1m')

    while True:

        if chong_zhi.isdigit() and int(chong_zhi) > 0:

            pay = int(chong_zhi)

            print('\033[33;1m充值后金额为\033[1m', pay)

            break

        elif chong_zhi == 'q':

            print('\033[36;1m程序正在退出\033[1m')

            exit()

        else:

            pass

#  pay=input('您的当前余额为0,是否充值？充值请输入您要充值的金额，退出程序请按q：')

########################################################################################################################

while True:

    show_list()  # 调用show_list函数，打印商品分类清单

    user_choise = input('\033[32;1m选择购买商品的类型：\033[1m')  # 获取用户选择商品的分类

    start()  # 调用start函数

    user_choise2 = input('\033[36;1m选择购买商品的类型。按q退出,按c查看易购买记录,按s查看当前已购买商品，任意键返回上一级菜单，：\033[0m')  # 获取用户选择的商品

    # user_num=input('\033[35;1m请选择需要购买的件数，默认为1：\033[0m')#获取用户选择商品的数量

    if user_choise2.isdigit() and int(user_choise2) < len(
            shop_list[shop_name[int(user_choise)]]):  # 判断用户输入的是否为数字，并小于商品序列号

        user_num = input('\033[35;1m请选择需要购买的件数，默认为1：\033[1m')  # 获取用户选择商品的数量

        show_menu2(user_choise, user_choise2)  # 调用show_menu2函数，获取用户选择商品的种类和数量，可用金额是否满足

        if user_num.strip() == '':  # 如果用户输入为空，默认为1

            user_num = int(1)

        elif user_num.isdigit and int(user_num) > 1:  # 如果用户输入是数字切大于1，获得用户输入中

            user_num = int(user_num)

        else:

            user_num = int(1)  # 其余情况下默认为一

        pay = int(pay)

        if pay > jiage2 * user_num:  # 判断用户选择商品的价格*数量是否可以支付

            pay = pay - jiage2 * user_num

            choise = list(shop_list[shop_name[int(user_choise)]].keys())  # 得到用户进入第二层商品列表

            count += 1  # 计数器值加一

            goumai_jilu = shelve.open('goumai_jilu.txt', 'a+')  # 调用shelve打开一个数据文件

            goumai_jilu[str(count)] = choise[int(user_choise2)], jiage2, user_num, time.ctime()  # 向数据文件中插入用户选择的商品，个数和购买时间

            goumai_jilu.close()  # 关闭数据文件

            a = choise[int(user_choise2)]  # 得到用户选择的商品，choise为用户选择第二层商品列表

        if a in shop_list1:  # 如果用户选择的商品已购买

            shop_list1[a][0] = int(shop_list1[a][0]) + user_num  # 将购买数加一

            shop_list1[a][1] = int(shop_list1[a][1]) + int(shop_list1[a][1] * user_num)  # 将总额加

        else:

            shop_list1[a] = list([1, jiage2])

        print('\033[32;1m您的余额为：\033[1m', pay)


    elif user_choise2 == 'b':  # 返回商品分类清单

        continue

    elif user_choise2 == 'q':  # 退出程序

        f = shelve.open('user.db', 'a+')

        f[user] = pay

        f.close()

        exit()

    elif user_choise2 == 'c':

        goumai_jilu = shelve.open('goumai_jilu.txt', 'a+')

        print('\033[32;1m您的当前购买记录为：\033[1m')

        for i in goumai_jilu.items():  # 获取购买记录中的数据

            print('{} {}'.format(i[0], goumai_jilu[i[0]]))  # 打印购买记录

        print('\033[32;1m################################################\033[0m')

        quit_time()

    elif user_choise2 == 's':

        print('\033[32;1mp_name  num   total_price\033[1m')

        print('\033[32;1m%-10s%-10s%-10s\033[1m' % (a, shop_list1[a][0], shop_list1[a][1]))  # 打印当前购买的商品，个数以及总额

        print('\033[32;1m################################################\033[0m')

        quit_time()

    else:

        print('\033[41;33m无效选项，请重新选择：\033[0m')

        continue

