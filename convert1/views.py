
# Create your views here.
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
import zhconv,json,re
from pypinyin import pinyin, Style
from hanzi_chaizi import HanziChaizi
from utils.word_desp import get_word_des,get_clean_description
from .models import History,XiaoZhuanHistory

def convert_api(request):
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

    if text == '':
        return JsonResponse({
            "code": 400,
            "msg": "请输入待转换文字",
            "result": ""
        })

    if mode == "s2t":
        # 输入应为简体
        is_simp = zhconv.issimp(text)
        if is_simp is False:
            return JsonResponse({
                "code": 400,
                "msg": "当前为「简体 → 繁体」模式，输入内容包含繁体字，请切换为「繁体 → 简体」或修改输入",
                "result": ""
            })
        result = zhconv.convert(text, 'zh-tw')

    elif mode == "t2s":
        # 输入应为繁体
        is_simp = zhconv.issimp(text)
        if is_simp is True:
            return JsonResponse({
                "code": 400,
                "msg": "当前为「繁体 → 简体」模式，输入内容包含简体字，请切换为「简体 → 繁体」或修改输入",
                "result": ""
            })
        result = zhconv.convert(text, 'zh-cn')

    else:
        return JsonResponse({"code": 400, "msg": "mode参数错误", "result": ""})

    # 简繁转换成功后保存记录
    History.objects.create(
        input=text,
        output=result,

    )
    return JsonResponse({
        "code":200,
        "msg":"ok",
        "result": result
    })

def convertUI(request):
    return render(request, 'convertUI.html')

def history_center(request):
    return render(request, 'history_center.html')

def HistoryUI(request):
    datas = History.objects.all()
    context = {'datas': datas}
    return render(request, 'HistoryList.html', context=context)

def  delete_history(request):
    if request.method == "POST":
        History.objects.all().delete()
    return redirect("convert1:historyUI")
def xiaozhuanUI(request):
    return render(request, 'xiaozhuanUI.html')
#hc = HanziChaizi()
def xiaozhuan_api(request):
    char = request.GET.get("char", "").strip()
    if not char:
        return JsonResponse({"code": 400, "msg": "请输入汉字"})
    py_list = pinyin(char, style=Style.TONE)
    pinyin_str = py_list[0][0] if py_list else "无"

    # radical = "—"
    # try:
    #     components = hc.query(char)
    #     if components:
    #         radical = '、'.join(components)
    # except Exception as e:
    #     print(f"hanzi_chaizi 解析失败: {e}")

    unicode_code = f"U+{ord(char):04X}"

    word_data = get_word_des(char)
    stroke_raw = word_data.get("strokes", "—").strip()
    stroke = stroke_raw if word_data else "暂无笔画信息，该字信息待完善"
    radical_raw = word_data.get("radicals", "").strip()
    radical = radical_raw if radical_raw else "暂无部首信息，该字信息待完善"
    description = get_clean_description(word_data)

    info = {
        "char": char,
        "pinyin": pinyin_str,
        "stroke": stroke,
        "radical": radical,
        "unicode": unicode_code,
        "description": description,
    }
    XiaoZhuanHistory.objects.create(
        char=char,
        info=json.dumps(info, ensure_ascii=False)
    )

    return JsonResponse({
        "code": 200,
        "char": char,
        "info": info
    })

def xiaozhuanhistoryUI(request):
    datas = XiaoZhuanHistory.objects.all().order_by("-create_time")
    context = {'datas': datas}
    return render(request, 'xiaozhuanhistoryList.html', context=context)

# 小篆清空记录
def del_xz_history(request):
    if request.method == "POST":
        XiaoZhuanHistory.objects.all().delete()
    return redirect("convert1:xiaozhuanhistoryUI")

def evolution(request):
    return render(request, 'evolution.html')
