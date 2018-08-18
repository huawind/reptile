# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib.request

rootDir = r"D:\reptile\image"  # 根目录


class BizhiPipeline(object):
    def process_item(self, item, spider):
        '''
        :param item:
        :param spider:
        :return:imageType=scrapy.Field()
        '''
        imageType = item['imageType']
        imageurl = item['imageurl']
        # 如果不存在则创建
        if not os.path.exists(rootDir):
            os.mkdir(rootDir)
        else:
            level1Dir = rootDir + '\\' + imageType  # 一级目录
            if not os.path.exists(level1Dir):
                os.mkdir(level1Dir)
            else:
                imagename = item['imagename'] + '.jpg'  # 文件名
                path = level1Dir + '\\' + imagename
                print(path)
                urllib.request.urlretrieve(imageurl, path)
            return item
