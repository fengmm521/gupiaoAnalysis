#!/usr/bin/env python
#-*- coding: utf-8 -*-
#可以通过此文件读取所有股票的ID和中文名，及所在版块信息
import os
import sys
import shutil
import pinyin
import time
import copy
import chardet  #中文编码判断
import xlrd


excelpth = 'res/xlsx/2016code1.xls'

reload(sys)
sys.setdefaultencoding( "utf-8" )


# print pinyin.get('你好')

# print pinyin.get('你好', format="strip", delimiter=" ")

# print pinyin.get('你好', format="numerical")
#中文转拼音
def getStringName(hanyu):
    #pname = pinyin.get_initial(hanyu,delimiter='').upper()
    pname = pinyin.get(hanyu, format="strip", delimiter="").lower()
    return pname
#提交数据到MySQL数据库


#获取文件名
def getFileNameFromPath(path):
    fname = os.path.splitext(os.path.split(path)[1])[0]
    return fname

def conventStrTOUtf8(oldstr):
    cnstrtype = chardet.detect(oldstr)['encoding']
    utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
    return utf8str

#读取股票中文名
#将EXCEL表转换为json文件
def getAllCodeID(fullfilename):
    codedics = {}
    wb = xlrd.open_workbook(fullfilename)  
    for sheetName in wb.sheet_names():
        if sheetName=="Sheet1":
            nclows = 0
            sheet = wb.sheet_by_name(sheetName)
            print sheet.ncols
            for i in range(0,sheet.ncols):            
                if sheet.cell(2,i).value=='':
                ##print sheet.nrows,',',sheet.ncols,',',len(sheet.cell(2,sheet.ncols-1).value)
                    nclows=i
                    break
                else:
                    nclows=sheet.ncols
            print '表格列数='+ str(nclows)
            for rownum in range(1,sheet.nrows):
                linetmp = []
                for nnumber in range(3):#只取三列，股票编号,股票名,股票行业
                    if nnumber > 0:#中文转为utf8
                        linetmp.append(sheet.cell(rownum,nnumber).value.encode('utf-8'))
                    else:
                        linetmp.append(sheet.cell(rownum,nnumber).value.encode('utf-8'))
                codedics[linetmp[0]] = linetmp
            print len(codedics)
    return codedics

def getAllIDs(isbackID = True):
    idstmp = []
    excelfile1 = excelpth
    id1s = getAllCodeID(excelfile1)
    idkeys = id1s.keys()

    if isbackID:
        for d in idkeys:
            idstmp.append(d)
        return idstmp
    else:
        return id1s


def downAllGuPiaoMsg():
    id1s = getAllIDs(False)
    print id1s[id1s.keys()[0]][1]
    print id1s[id1s.keys()[1]][2]

    #http请求百度百科的股票介绍，请求地址：https://baike.baidu.com/item/中信海直
    #互动百科，企业简介查询，（中文名称查询）地址：http://www.baike.com/wiki/华锐风电
    #凤凰网的公司简介,(使用股票代码请求)请求地址：http://app.finance.ifeng.com/data/stock/tab_gsjj.php?symbol=002011
    #凤凰网提供的资产负债表,(使用代码)查询地址：http://app.finance.ifeng.com/data/stock/tab_zcfzb.php?symbol=002011
    #网易公司经营产品（使用代码查询）.查询地址：http://quotes.money.163.com/f10/gszl_601558.html
    #网易的公司资产负债表,(使用代码查)，地址：http://quotes.money.163.com/f10/zcfzb_300418.html
    #网易提牮的公司主要财务指标，（使用代码），地址：http://quotes.money.163.com/f10/zycwzb_300418.html
    #网易提供的公司财务报表摘要，（使用代码），地址：http://quotes.money.163.com/f10/cwbbzy_300418.html
    #网易提供的现金流表，（使用代码），地址：http://quotes.money.163.com/f10/xjllb_300418.html
    #网易提供的利润表，（使用代码），地址：http://quotes.money.163.com/f10/lrb_300418.html
    #网易提供的股东分析,（使用代码），地址：http://quotes.money.163.com/f10/gdfx_300418.html
    #网易提供的基金持股，（使用代码），地址：http://quotes.money.163.com/f10/jjcg_300418.html
    #网易提供的公司内部持股数据,(使用代码)，地址：http://quotes.money.163.com/f10/nbcg_300418.html
    #仓位在线企业信息查询，（使用代码）,查询地址：http://cwzx.shdjt.com/gpdmf10.asp?gpdm=000543
    #证卷之星提供的数据，(使用代码)，查询地址：http://stock.quote.stockstar.com/finance/profit_601558.shtml
    #正点财经公司经营业务及子公司,(使用股票代码查询)查询地址:http://stock.zdcj.net/gongsi/000099.html
    #正点财经提供的股东股本信息，（使用代码），查询地址：http://stock.zdcj.net/gudong/000099.html
    #正点财经提供的主力持仓信息，（使用代码），查询地址：http://stock.zdcj.net/zhuli/000099.html
    #新浪提供的资产负债表查询，（使用代码查询）查询地址：http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/002011/ctrl/part/displaytype/4.phtml
    #新浪提供的利润表，(使用代码查询)查询地址:http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/002011/ctrl/part/displaytype/4.phtml
    #新浪提供的现金流量表,(使用代码查询)查询地址:http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/002011/ctrl/part/displaytype/4.phtml
    #新浪提供的财务摘要表,(使用代码查询)查询地址：http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/002011/displaytype/4.phtml
    #东方财富网提供的企业简介，（代码查询）查询地址：http://f10.eastmoney.com/f10_v2/CompanySurvey.aspx?code=sh601558
    #赢家财富网提供的企业简介，（代码查询）查询地址：http://www.yjcf360.com/gegu/601558/gsjs/
    #*----企业高管简介，（代码查询）查询地址：http://601558.stock.inv.org.cn/info/manage.php
    #*----企业董事成员简介，（代码查询）查询地址：http://601558.stock.inv.org.cn/info/director.php
    #*----企业监视成员简介，（代码查询）查询地址：http://601558.stock.inv.org.cn/info/supervisor.php
    #十五股东，（代码查询）地址：http://002011.stock.inv.org.cn/info/stockholder.php
    #企业简介，(代码查询)地址：http://002011.stock.inv.org.cn/info/profile.php
    #另一个企业简介，（代码加股票证卷类型）地址：http://soft-f9.eastmoney.com/soft/gp3.php?code=60155801

#测试
if __name__ == '__main__':

    downAllGuPiaoMsg()



# aaa = getStringName('中国')
# print aaa
        
