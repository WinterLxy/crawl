'''
使用urllib模块编写百度翻译功能 ---2020/2/9
'''
from urllib import parse,request
import json
import re
import js2py
from bs4 import BeautifulSoup
#####js2py用法###
# gen_guid="""
# function createGuid() {
#     return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
# }
# var guid1 = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid();
# """
#     context = js2py.EvalJs()
#     context.execute(gen_guid)
#     guid=context.guid1 # 将guid1传递到Python中
#     print guid
#################

#经分析，网页返回的token及js中的部分变量均来自网页的返回内容
class baidufanyi():
    def __init__(self,word):
        self.word = word
        url = "https://fanyi.baidu.com/"
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
            "Cookie": "BIDUPSID=BED0DD630E472A5686CC9A382847D347; PSTM=1580452245; BAIDUID=BED0DD630E472A56DAC83F575ABB0AE8:SL=0:NR=50:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[HHw4GR7hd6D]=mk3SLVN4HKm; H_PS_PSSID=1448_21124; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1580526965,1580542767,1581083493,1581214328; yjs_js_security_passport=ff082fbef7b8609e6bb116c07da5f0e86b54278b_1581219001_js; delPer=0; PSINO=7; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1581229225; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D"
        }
        req = request.Request(url=url,headers=headers)
        rsp = request.urlopen(req)
        html =rsp.read().decode("utf-8")
        #此处为了显示出来返回的东西
        # with open("123.txt","w",encoding="utf-8") as f:
        #     f.write(html)
        # print(html)
        self.token = re.findall("token: ('.*')",html)[0]
        self.token =self.token.replace("\'","")
        print(self.token)
        self.gtk = re.findall("window.gtk = ('.*');",html)[0]
        print(self.gtk)

    def get_sign(self):
        js_code =r"""
    function a(r) {
        if (Array.isArray(r)) {
            for (var o = 0,
            t = Array(r.length); o < r.length; o++) t[o] = r[o];
            return t
        }
        return Array.from(r)
    }
    function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
    function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr( - 10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)"" !== e[C] && f.push.apply(f, a(e[C].split(""))),
            C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice( - 10).join(""))
        }
        var u = void 0,
        l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i: (i = window[l] || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A: (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
        }
        for (var p = m,
        F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b],
        p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
        """
        js_code=js_code.replace(r'null !== i ? i: (i = window[l] || "") || ""',self.gtk)

        # print(js_code)
        # print(self.gtk)
        context = js2py.EvalJs()
        context.execute(js_code)
        self.sign = context.e(self.word)
        print(self.sign)

    def get_trans(self):
        url_trans = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
        data={
            "from": "en",
            "to": "zh",
            "query": self.word,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": self.sign,
            "token": self.token
        }
        print(data)
        data = parse.urlencode(data).encode("utf-8")
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
            "Content-Length": len(data),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"BIDUPSID=BED0DD630E472A5686CC9A382847D347; PSTM=1580452245; BAIDUID=BED0DD630E472A56DAC83F575ABB0AE8:SL=0:NR=50:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[HHw4GR7hd6D]=mk3SLVN4HKm; H_PS_PSSID=1448_21124; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1580526965,1580542767,1581083493,1581214328; yjs_js_security_passport=ff082fbef7b8609e6bb116c07da5f0e86b54278b_1581219001_js; delPer=0; PSINO=7; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1581229225; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D"
        }
        print(headers)
        req = request.Request(url=url_trans,data=data,headers=headers)
        rsp = request.urlopen(req)
        html = rsp.read().decode("utf-8")
        print(html)
        html = json.loads(html) #通过网页可以看出，返回的为json格式，使用json解析
        print(html)
        meas = str(html)
        meas = re.findall(r"word_means': (.+?)]",meas)[0]+"]" #找到解释，因为json太麻烦，所以转成了字符串，然后通过正则查找
        print(meas)
        # soup = BeautifulSoup(html,"lxml")
        # print(soup)
        # means = soup.find_all("div",{"class":"dictionary-comment"})
        # print(means)
        # for i in means:
        #     print(i["span"])

i = input("请输入要翻译的内容")
s = baidufanyi(i)
s.get_sign()
s.get_trans()


# 前期参数试验程序
# def fanyi(kw):
#     url="https://fanyi.baidu.com/v2transapi?from=en&to=zh"
#     # data = {"query": "girl"}
#     data={
#         "from":"en",
#         "to":"zh",
#         "query":"girl",
#         "transtype":"realtime",
#         "simple_means_flag":"3",
#         "sign":"780982.985479",
#         "token":"1b30425fd329a06732e54769ee003419"
#     }
#     data = parse.urlencode(data).encode("utf-8")
#     headers={
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
#         "Content-Length":"121",
#         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#         "cookie": "BIDUPSID=BED0DD630E472A5686CC9A382847D347; PSTM=1580452245; BAIDUID=BED0DD630E472A56DAC83F575ABB0AE8:SL=0:NR=50:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; BDUSS=FPNHJESy03QVdIVFZBZFpTYzJrdHZaOEhoVEdKc1V-ZkJWak5xT0p4azNJRjVlRVFBQUFBJCQAAAAAAAAAAAEAAAB63o86AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADeTNl43kzZeUD; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[HHw4GR7hd6D]=mk3SLVN4HKm; H_PS_PSSID=1448_21124; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1580526965,1580542767,1581083493,1581214328; yjs_js_security_passport=0623ff0862906cdacc759feea04186a7b4fe4486_1581215343_js; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22fra%22%2C%22text%22%3A%22%u6CD5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1581218508; __yjsv5_shitong=1.0_7_626e3dd95c3e8e4df7a20c5e970a0bb10922_300_1581218507887_111.23.225.106_f2385709"
#     }
#     req = request.Request(url=url,data=data,headers=headers)
#     rsp = request.urlopen(req)
#     html = rsp.read().decode("utf-8")
#     json_data=json.loads(html)
#     print(json_data)
# fanyi("boy")