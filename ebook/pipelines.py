# -*- coding: utf-8 -*-
import os, requests


class EbookPipeline(object):
    def process_item(self, item, spider):
        path = os.getcwd() + '\\八年级物理上册课本教材'
        if not os.path.exists(path):
            os.makedirs(path)

        path += "\\" + item['chapter']
        if not os.path.exists(path):
            os.makedirs(path)

        path += "\\" + item['section']
        if not os.path.exists(path):
            os.makedirs(path)

        # 保存图片
        for index in range(len(item['pages'])):
            filename = item['pages'][index].split('/')[-1]

            # 下载网络图片并保存到本地
            res = requests.get("http://www.wsbedu.com" + item['pages'][index])
            with open(path + '\\' + filename, 'wb') as f:
                f.write(res.content)

        return item
