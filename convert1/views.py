from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
import zhconv

from convert1.models import History

appname = "convert1"

def convert_text(request):
    """
    接口：简繁转换
    GET参数：
        text: 待转换文字
        mode: 转换方向
            s2t：简体转繁体
            t2s：繁体转简体
    """
    text = request.GET.get("text", "")
    mode = request.GET.get("mode", "s2t")

    if text=='':
        return JsonResponse({
            "code":400,
        })

    if mode == "s2t":
        result = zhconv.convert(text, 'zh-tw')
    elif mode == "t2s":
        result = zhconv.convert(text, 'zh-cn')
    # else:
    #     # return JsonResponse({"code":400,"msg":"mode参数错误","result":""})
    #     return HttpResponse("参数错误")

    History.objects.create(input=text, output=result)

    return JsonResponse({
        "code":200,
        "msg":"ok",
        "result": result
    })

def convertUI(request):
    return render(request, 'convert.html')

def HistoryView(request):
    datas = History.objects.all()
    context = {'datas': datas}
    return render(request, 'HistoryList.html', context=context)

def  delete_history(request):
    History.objects.all().delete()
    return HttpResponse("历史记录删除")