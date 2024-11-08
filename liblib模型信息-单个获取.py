"""
项目名称：liblib模型信息获取

功能：对单个模型链接进行提取信息的操作，在获取模型信息后可以支持自动化文件分类和图片下载

扩展：可以结合喜欢列表进行批量获取

@author: Alabyser， Huatin-Nice, 

"""

import json
import sys
import os
import requests
import re
import xpath
import threading

# 常量

MODEL_NAME = ''
MODEL_VERSION = ''
MODEL_ISORG = ''
MODEL_TYPE = ''
MODEL_BASETYPE = ''
MODEL_USINGTAGS = ''
MODEL_FUNC_INFO = ''
MODEL_SAMPLEMET = ''
MODEL_RECOMMEND = ''
MODEL_WEIGHT = ''
MODEL_CFG = ''
MODEL_VAE = ''
MODEL_HDSAMPLE = ''
MODEL_ONLINEIMG = ''
MODEL_ISMIX = ''
MODEL_ISPAYMODEL = ''
MODEL_ISPAYIMG = ''

# 内置json配置

d = {
    1: "Checkpoint",
    2: "Textual Inversion",
    3: "Hypernetwork",
    4: "Aesthetic Gradient",
    5: "LoRA",
    6: "LyCORIS",
    7: "Controlnet",
    8: "Poses",
    9: "Wildcards",
    10: "Other",
    18: "工作流"
}

A = {
    1: "基础算法 1.5",
    2: "基础算法 2.1",
    3: "基础算法 XL",
    4: "Cascade Stage a",
    5: "Cascade Stage b",
    6: "Cascade Stage c",
    7: "基础算法 v3",
    8: "混元DiT v1.2",
    9: "PixArt Σ",
    10: "Pony",
    11: "Kolors",
    12: "混元DiT v1.1",
    13: "PixArt α",
    14: "Aura Flow",
    15: "Playground V2",
    16: "Lumina",
    17: "SVD",
    18: "SVD XT",
    19: "基础模型 F.1",
    20: "基础算法 v3.5M",
    21: "基础算法 v3.5L"
}

# 获取json配置

with open(file='enums.json', mode='r', encoding='utf-8') as f:
    enums = json.loads(f.read())

# 开始爬虫准备

usg = '请求头'
ck = '完整cookie'
tk = 'token值'
og = 'https://www.liblib.art'
ref = 'https://www.liblib.art/userpage/你的用户id/like'

http_head = {
    'User-Agent': usg,
    'Referer': ref,
    'Origin': og,
    'Cookie': str(ck),
    'token': tk,
}

# 开始爬取信息

# url = "https://www.liblib.art/modelinfo/4abe0d99538d4867af86a59ee899b4fe?from=feed&versionUuid=92b7ee22d24f499394bfbc1f755c53b1"
url = input("输入模型链接: ").strip()
url_split = re.split(r'[/?]', url)
index1 = url_split.index("modelinfo") + 1
url_uid = url_split[index1]
end_url = f'https://www.liblib.art/api/www/model/getByUuid/{url_uid}?timestamp=1720684710679'
content = requests.post(end_url, headers=http_head).json()

only_using = ['独家', '是', '否', '可', '不可', '仅会员']


# 传入任意非空参数激活

def get_name(_get_cmd=''):
    global MODEL_NAME
    global MODEL_VERSION

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_NAME = content['data']['name']
            MODEL_VERSION = content['data']['versions'][0]['name']

            return MODEL_NAME + MODEL_VERSION

    except Exception as e:
        print(e)


def get_verson(_get_cmd=''):
    global MODEL_ISORG

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_ISORG = content['data']['versions'][0]['exclusive']

            return only_using[0] if MODEL_ISORG else only_using[1]

    except Exception as e:
        print(e)


def get_type(_get_cmd=''):
    global MODEL_TYPE

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_TYPE = d[content['data']['modelType']]

            return MODEL_TYPE

    except Exception as e:
        print(e)


def get_basetype(_get_cmd=''):
    global MODEL_BASETYPE

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_BASETYPE = A[content['data']['versions'][0]['baseType']]

            return MODEL_BASETYPE

    except Exception as e:
        print(e)


def get_usingtags(_get_cmd=''):
    global MODEL_USINGTAGS

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_USINGTAGS = content['data']['versions'][0]['triggerWord']

            return MODEL_USINGTAGS

    except Exception as e:
        print(e)


def get_func_info(_get_cmd=''):
    global MODEL_FUNC_INFO

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_FUNC_INFO = json.loads(content['data']['versions'][0]['versionIntro'])['loraDes']

            return MODEL_FUNC_INFO

    except Exception as e:
        print(e)


def get_samplemet(_get_cmd=''):
    global MODEL_SAMPLEMET

    try:
        samplerMethods = ''
        if _get_cmd and _get_cmd != ' ':
            MODEL_SAMPLEMET = json.loads(content['data']['versions'][0]['versionIntro']).keys()
            if 'samplerMethods' in MODEL_SAMPLEMET:
                print('samplerMethods作为键在列表，值为', MODEL_SAMPLEMET['samplerMethods'])
                if MODEL_SAMPLEMET['samplerMethods'] and MODEL_SAMPLEMET['samplerMethods'] != ' ':
                    return MODEL_SAMPLEMET['samplerMethods']
                else:
                    for x in MODEL_SAMPLEMET["samplerMethods"]:
                        samplerMethods += enums['data'][25]['items'][x]['text'] + ","
                    return samplerMethods
            else:
                print('samplerMethods作为键不在列表')
                return '无'


    except Exception as e:
        print(e)


def get_recommend(_get_cmd=''):
    global MODEL_RECOMMEND

    try:
        recommend_list = []
        if _get_cmd and _get_cmd != ' ':
            MODEL_RECOMMEND = '测试'
            r = requests.post(url=end_url, headers=http_head, json={})

            if r.status_code == 200:
                j = r.json()
                versionIntro = json.loads(j['data']['versions'][0]['versionIntro'])

                if "ckpt" in versionIntro.keys():
                    print("找到对应的推荐值!")

                    json_post = versionIntro['ckpt']
                    listbyids_url = "https://www.liblib.art/api/www/model-version/modelVersion/listByIds?timestamp=1730943223666"
                    r1 = requests.post(url=listbyids_url, headers=http_head, json={"versionIds": json_post})

                    for y in r1.json()['data']:
                        # print("推荐搭配:%s: 链接:%s" % (
                        #     y['modelName'], "https://www.liblib.art/modelinfo/" + y['modelUuid']))
                        recommend_list.append(y['modelName'])
                    MODEL_RECOMMEND = recommend_list
                    return MODEL_RECOMMEND

    except Exception as e:
        print(e)


def get_weight(_get_cmd=''):
    global MODEL_WEIGHT

    try:
        if _get_cmd and _get_cmd != ' ':
            # {'ckpt': ['2561763', '2628330', '2298961'], 'hdSamplerMethods': [15], 'cfg': 3.5, 'triggerWord': '["trendy"]', 'weight': 0.6, 'vae': 'none', 'loraDes': '时尚穿搭赛道流量收割机'}
            MODEL_WEIGHT = json.loads(content['data']['versions'][0]['versionIntro'])['weight']
            return MODEL_WEIGHT
    except Exception as e:
        print(e)


def get_cfg(_get_cmd=''):
    global MODEL_CFG

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_CFG = json.loads(content['data']['versions'][0]['versionIntro'])['cfg']
            return MODEL_CFG
    except Exception as e:
        print(e)


def get_vae(_get_cmd=''):
    global MODEL_VAE

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_VAE = json.loads(content['data']['versions'][0]['versionIntro'])['vae']
            match MODEL_VAE:
                case 'none':
                    return '无'
                case _:
                    vae_url = "https://www.liblib.art/api/www/model-version/modelVersion/listByIds"
                    vae_data = requests.post(url=vae_url, json={"versionIds": MODEL_VAE}).json()
                    MODEL_VAE = vae_data['data'][0]['modelVersionName']
                    return MODEL_VAE


    except Exception as e:
        print(e)


def get_hdsample(_get_cmd=''):
    global MODEL_HDSAMPLE

    try:
        if _get_cmd and _get_cmd != ' ':
            try:
                MODEL_HDSAMPLE = json.loads(
                    content['data']['versions'][0]['imageGroup']['images'][1]['generateInfo']['metainformation'])[
                    'Hires upscaler']
            except:
                pass

        if MODEL_HDSAMPLE and MODEL_HDSAMPLE != ' ':
            return MODEL_HDSAMPLE
        else:
            vr = json.loads(content['data']['versions'][0]['versionIntro'])
            if 'hdSamplerMethods' in json.loads(content['data']['versions'][0]['versionIntro']).keys():
                return enums['data'][33]['items'][[vr['hdSamplerMethods']][0][0]]['text']
            else:
                return '无'
    except:

        return '无返回'


def get_onlineImg(_get_cmd=''):
    global MODEL_ONLINEIMG

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_ONLINEIMG = content['data']['versions'][0]['showType']
            match MODEL_ONLINEIMG:
                case 1:
                    return only_using[3]
                case 0:
                    return only_using[4]
    except Exception as e:
        print(e)


def get_isMix(_get_cmd=''):
    global MODEL_ISMIX

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_ISMIX = content['data']['openMix']
            match MODEL_ISMIX:
                case 1:
                    return only_using[3]
                case 0:
                    return only_using[4]
    except Exception as e:
        print(e)


def get_isPayImg(_get_cmd=''):
    global MODEL_ISPAYIMG

    try:
        if _get_cmd and _get_cmd != ' ':
            MODEL_ISPAYIMG = content['data']['versions'][0]['vipUsed']
            MODEL_PRIVILEGE = content['data']['privilege']  # 读取授权逻辑数据
            freeOpenPay = '免费也可以进行商业目的的'  # 逻辑暂未添加，内容爬虫暂无头绪，等待Huatin-Nice进行下一步操作
            match MODEL_ISPAYIMG:
                case 1 | 2:
                    return only_using[5]
                case 0:
                    # 逻辑验证
                    if "1" in MODEL_PRIVILEGE and MODEL_ISPAYIMG == 0:
                        # 非会员模型可以可出售生成图片或用于商业目的逻辑判断
                        return only_using[3]  # 返回可
                    return only_using[4]  # 找不到内容返回不可
    except Exception as e:
        print(e)


def get_isPayModel(_get_cmd=''):
    global MODEL_ISPAYMODEL
    try:
        MODEL_PRIVILEGE = content['data']['privilege']  # 读取授权逻辑数据
        if "2" in MODEL_PRIVILEGE:
            return only_using[3]
        else:
            return only_using[4]
    except Exception as e:
        print(e)


def download_thread(image_url="", image_file_name="", save_dir=""):
    """ 线程下载 """
    error = 5
    error_count = 0
    try:
        file_path = f"{save_dir}/{image_file_name}"
        if os.path.exists(file_path):
            print(f"{image_file_name}已经存在跳过下载!")
            return

        while error_count < error:
            s = requests.get(url=image_url, headers=http_head)
            if s.status_code == 200:
                image_data = s.content
                with open(file=file_path, mode='wb') as f:
                    f.write(image_data)
            print(f"下载完成： {image_file_name}")
            break
        return
    except:
        error_count += 1


def get_imdDownload():
    all_img_info = content['data']['versions'][0]['imageGroup']['images']  # 到此是图片的url列表，包含无水印原图，可以免会员下载直链
    # print(type(all_img_info))

    n = len(all_img_info)
    print("无水印原图共计：", n)
    for get_imageUrl in all_img_info:
        threading.Thread(target=download_thread,
                         args=(get_imageUrl['imageUrl'], get_imageUrl['originalName'], get_name(_get_cmd='1'))).start()

    # 评论区返图功能
    url_plq = "https://www.liblib.art/api/www/community/returnPicList"
    post_json = {"uuid": url_uid, "pageSize": 10, "page": 1, "sortType": 0}
    s = requests.post(url_plq, json=post_json, headers=http_head).json()
    if s['msg'] == "success":
        for x in s['data']['dataList']:
            # print(x)
            for y in x['pics']:
                image_url = y['imageUrl']
                file_name = "FT-" + image_url.split("/")[-1]
                threading.Thread(target=download_thread,
                                 args=(image_url, file_name,
                                       get_name(_get_cmd='1'))).start()

                # print("返图无水印原图下载直链：", y['imageUrl'])


all = f"""
简介：{xpath.xpxp(url_ex=url, headers=http_head)}\n\n\n

标题：{get_name(_get_cmd='1')}

{get_verson(_get_cmd='1')} ==版本详情==：

模型种类：{get_type(_get_cmd='1')}
模型算法：{get_basetype(_get_cmd='1')}
触发词：{get_usingtags(_get_cmd='1')}
功能描述：{get_func_info(_get_cmd='1')}

==推荐参数==

采样方法：{get_samplemet(_get_cmd='1')}
推荐搭配：{get_recommend(_get_cmd='1')}
推荐权重：{get_weight(_get_cmd='1')}
CFG：{get_cfg(_get_cmd='1')}
VAE：{get_vae(_get_cmd='1')}
高清放大算法：{get_hdsample(_get_cmd='1')}

创作许可范围：
{get_onlineImg(_get_cmd='1')}在线生图
{get_isMix(_get_cmd='1')}进行融合

商业许可范围：
{get_isPayImg(_get_cmd='1')}出售生成图片或用于商业目的
{get_isPayModel(_get_cmd='1')}转售模型或出售融合模型

*许可范围为创作者本人设置，使用者需按规范使用
企业将模型用于商业用途，可联系平台咨询模型商业授权 
"""


def over_output(model_AllInfo='', write_info=''):
    os.makedirs(model_AllInfo, exist_ok=True)

    with open(file=f'{model_AllInfo}/简介.txt', mode='w', encoding="utf-8") as f:
        f.write(write_info)


over_output(model_AllInfo=get_name(_get_cmd='1'), write_info=all)
get_imdDownload()
print(all)
input()
