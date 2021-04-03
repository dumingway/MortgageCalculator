from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
# Create your views here.

from .models import Book


def index(request):
    # return HttpResponse("这里是房贷计算器！")
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        # myForm = request.POST.get('form')
        # totalLoan:贷款总额(万) loanType:贷款类型 repaymentMode:还款模式 repaymentPeriod:还款年数
        # repaymentDate:首次还款日期 interestRateStandard:利率标准 LPR basePoint:基点
        totalLoan = data.get('totalLoan')
        loanType = data.get('loanType')
        repaymentMode = data.get('repaymentMode')
        repaymentPeriod = int(data.get('repaymentPeriod'))
        repaymentDate = data.get('repaymentDate')
        interestRateStandard = data.get('interestRateStandard')
        LPR = data.get('LPR')
        basePoint = data.get('basePoint')
        baseInterestRate = data.get('baseInterestRate')

        loanCNY = float(totalLoan) * 10000
        repaymentMonth = repaymentPeriod * 12
        monthPrincipalPayment = []
        monthInterestPayment = []
        currentRemaining = []
        monthPayment = 0
        # 获取利率标准，算出贷款年利率、贷款月利率
        if interestRateStandard == "1":
            annualRate = round(float(LPR) * 0.01 + float(basePoint) * 0.0001, 8)  # 贷款年利率
            monthRate = round(annualRate / 12, 10)  # 贷款月利率
        elif interestRateStandard == "2":
            annualRate = round(float(baseInterestRate) * 0.01, 5)  # 贷款年利率
            monthRate = round(annualRate / 12, 7)  # 贷款月利率

        # 商业贷款，等额本金
        if (loanType == "1") and (repaymentMode == "1"):
            # 每月应还本金
            monthPrincipalPayment = [round(loanCNY / (repaymentPeriod*12), 2)] * repaymentPeriod * 12
            # 每月应还利息
            monthInterestPayment = [round((loanCNY - loanCNY * n / (repaymentPeriod * 12)) * monthRate, 2) for n in range(0, repaymentPeriod * 12)]
            currentRepayment = []
            currentAlreadyPaid = []
            alreadyPaidTemp = 0
            totalInterest = 0
            for i in range(repaymentMonth):
                temp = round(monthPrincipalPayment[i] + monthInterestPayment[i], 2)
                alreadyPaidTemp = alreadyPaidTemp + temp
                currentAlreadyPaid.append(alreadyPaidTemp)
                totalInterest = totalInterest + monthInterestPayment[i]
                currentRepayment.append(temp)
            # 本期剩余
            currentRemaining = [round(loanCNY + totalInterest - currentAlreadyPaid[n], 2) for n in range(0, repaymentMonth)]
        # 商业贷款，等额本息
        elif (loanType == "1") and (repaymentMode == "2"):
            # 首月应还利息
            firstMonthInterest = loanCNY * monthRate
            # 每月应还本息
            monthPayment = round((loanCNY * monthRate * (1 + monthRate) ** repaymentMonth) / ((1 + monthRate) ** repaymentMonth - 1), 2)
            # print("等额本息每月应还{}".format(round(monthPayment, 2)))
            # 本金剩余
            principalRemaining = [round(loanCNY * (1 + monthRate) - monthPayment, 2)]
            # 本期剩余
            currentRemaining = [round(monthPayment * repaymentMonth - monthPayment, 2)]
            # 每期应还利息
            monthInterestPayment = [round(loanCNY * monthRate, 2)]
            for n in range(1, repaymentMonth):
                principalRemaining.append(round((principalRemaining[n - 1] * (1 + monthRate) - monthPayment), 2))
                monthInterestPayment.append(round(principalRemaining[n - 1] * monthRate, 2))
                currentRemaining.append(round(currentRemaining[n-1] - monthPayment, 2))
            # 每期应还本金
            monthPrincipalPayment = [round(monthPayment - monthInterestPayment[n], 2) for n in range(0, repaymentMonth)]

        # print(request.body)
        # return render(request, 'result.html')
        context = {
            'title': '房贷清单',
            'totalLoan': totalLoan,
            'loanType': loanType,
            'repaymentMode': repaymentMode,
            'repaymentPeriod': repaymentPeriod,
            'repaymentDate': repaymentDate,
            'interestRateStandard': interestRateStandard,
            'LPR': LPR,
            'basePoint': basePoint,
            'baseInterestRate': baseInterestRate,
            'monthPrincipalPayment': monthPrincipalPayment,
            'monthInterestPayment': monthInterestPayment,
            'currentRemaining': currentRemaining,
            'monthPayment': monthPayment,

        }
        # return HttpResponse("这里是房贷计算器展示界面");
        return JsonResponse(context)
    else:
        period_list = []
        for value in range(30, 0, -1):
            temp = {'year': value, 'month': value*12}
            period_list.append(temp)
            # return render(request, 'index.html', {'data': period_list})
            return HttpResponse("这里是房贷清单")


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


def hello(request):
    page = request.GET.get('page')  # 从前端获取listQuery参数中的数据
    limit = request.GET.get('limit') # 从前端获取listQuery参数中的数据
    mytype = request.GET.get('type') # 从前端获取listQuery参数中的数据
    sort = request.GET.get('sort') # 从前端获取listQuery参数中的数据

    dict1 = {}
    # 第一行数据
    dict1['id'] = '1'
    dict1['date'] = '606208526029'
    dict1['title'] = 'my title'
    dict1['author'] = 'james'
    dict1['reviewer'] = 'Larry'
    dict1['importance'] = '1'
    dict1['readmings'] = '1'
    dict1['status'] = 'draft'
    dict1['actions'] = '1'
    dict1['edit'] = '1'
    dict1['publish'] = '1'
    dict1['draft'] = '0'
    dict1['content_short'] = 'it is a test'
    dict1['content'] = 'ceshishuju'
    dict1['forecast'] = 99.11
    dict1['type'] = 'JP'
    dict1['status'] = 'draft'
    dict1['display_time'] = '1994-05-26 18:59:04'
    dict1['comment_disabled'] = 'true'
    dict1['pageviews'] = 1823
    dict1['image_uri'] = 'https://wpimg.wallstcn.com'
    dict1['platforms'] = ['a-platform']


    dict2 = {} # 第二行数据
    dict2['id'] = '2'
    dict2['date'] = '602208526029'
    dict2['title'] = 'my title2'
    dict2['author'] = 'james2'
    dict2['reviewer'] = 'Larry2'
    dict2['importance'] = '2'
    dict2['readmings'] = '2'
    dict2['status'] = 'draft'
    dict2['actions'] = '1'
    dict2['edit'] = '1'
    dict2['publish'] = '1'
    dict2['draft'] = '0'
    dict2['content_short'] = 'it is a test2'
    dict2['content'] = 'ceshishuju2'
    dict2['forecast'] = 99.22
    dict2['type'] = 'CN'
    dict2['status'] = 'draft'
    dict2['display_time'] = '1994-05-26 18:59:04'
    dict2['comment_disabled'] = 'true'
    dict2['pageviews'] = 2000
    dict2['image_uri'] = 'https://wpimg.wallstcn.com'
    dict2['platforms'] = ['a-platform']


    mylist =list()
    mylist.append(dict1)
    mylist.append(dict2)
    resultlist =list()

    if mytype == '' or None: # 根据请求参数不同，返回的数据不同
        resultlist = mylist
    else:
        for mydict in mylist:
            if mydict['type'] == mytype:
                resultlist.append(mydict)

    return HttpResponse(json.dumps(resultlist),content_type="application/json")
    # 这里返回Json格式数据本文


