# -*- coding: utf-8 -*-
# 调用bk_cls原子API服务
# 默认线程10

ak = "yl56WT1YeKnqvM5YEwd92b2RNPj7lxgF87jUPsc8"
sk = "wNMU-buwy-zx5BSRnO7ti8b1Sv59hm3Hewah_Exd"

import json
import argparse
import requests
from ava_auth import AuthFactory
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

def parse():
    args = argparse.ArgumentParser('terror class infer')
    args.add_argument('--mode',type = str,required = True,choices = ['cls','det'],help='暴恐分类【cls】or 检测【det】')
    args.add_argument('--gt',type = str,required = True, help = 'LabelX标注过的json文件')
    args.add_argument('--log',type = str,required = True, help = '日志文件，每行一个结果（name\tclass）')
    args.add_argument('--ak',type = str,required = True,help = 'ak')
    args.add_argument('--sk',type = str,required = True,help = 'sk')
    return args.parse_args()

def token_gen(ak,sk):
    factory = AuthFactory(ak,sk)
    fauth = factory.get_qiniu_auth
    token = fauth()
    return token

def bk_cls(img_url,ak,sk):
    res = {}
    request_url = 'http://argus.atlab.ai/v1/eval/terror-classify'
    headers = {"Content-Type": "application/json"}
    body = json.dumps({"data": {"uri": img_url}})
    token = token_gen(ak,sk)
    try:
        r = requests.post(request_url, data=body,timeout=15, headers=headers, auth=token)
    except:
        print('http error.')
    else:
        if r.status_code == 200:
            r = r.json()
            if r['code'] == 0 and r['result']['confidences'] is not None:
                img_name = img_url.split('/')[-1]
                res['img_name'] = img_name
                label = r['result']['confidences'][0]['class']
                res['label'] = label
    return res

def bk_det(img_url,ak,sk):
    res = {}
    request_url = 'http://argus.atlab.ai/v1/eval/terror-detect'
    headers = {"Content-Type": "application/json"} 
    body = json.dumps({"data": {"uri": img_url}})
    token = token_gen(ak,sk)
    try:
        r = requests.post(request_url, data=body,timeout=15, headers=headers, auth=token)
    except:
        print('http error.')
    else:
        if r.status_code == 200:
            r = r.json()
            if r['code'] == 0:
                img_name = img_url.split('/')[-1]
                res['img_name'] = img_name
                label = r['result']['detections']
                res['label'] = label
    return res


def url_gen(gt_file):
    urls = []
    with open(gt_file,'r') as f:
        for line in f:
            line = json.loads(line.strip())
            url = line['url']
            urls.append(url)
    return urls

def bk_infer(mode,img_urls,log,ak,sk,num_thread=10):
    """
    multithread 
    Args:
    -----
    img_urls : list of url
    log : bk cls tsv log
    num_thread : num thread

    """
    with open(log,'w') as f_log:
        with ThreadPoolExecutor(max_workers=num_thread) as exe:
            if mode == 'cls':
                future_tasks = [exe.submit(bk_cls, url,ak,sk) for url in img_urls]
            else:
                future_tasks = [exe.submit(bk_det, url,ak,sk) for url in img_urls]
            all_url = len(future_tasks)
            count = 1
            for task in as_completed(future_tasks):
                if task.done():
                    print('bk cls %d/%d'%(count,all_url))
                    count += 1
                    res = task.result()
                    if res == {}:
                        continue
                    f_log.write('%s\t%s'%(res['img_name'],res['label']))
                    f_log.write('\n')

if __name__ == '__main__':
    args = parse()
    urls = url_gen(args.gt)
    bk_infer(args.mode,urls,args.log,args.ak,args.sk)
