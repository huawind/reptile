
import scrapy

from bizhi import items


# 爬取图片并下载
class MybizhiSpider(scrapy.Spider):
    name = 'mybizhi'
    allowed_domains = ['bizhiku.net']
    start_urls = ['http://www.bizhiku.net/']

    def parse(self, response):
        """
        抓取不同类型图片的列表
        :param response:
        :return:
        """
        # 抓取一级标签
        level1List = response.xpath('//li[@class="item open category"]/div/a')
        for i in level1List:
            level1Url = "http://www.bizhiku.net" + i.xpath("./@href")[0].extract()
            imageType = i.xpath("./text()")[0].extract()
            # 构建一个请求
            request = scrapy.Request(level1Url, callback=self.get_level2)
            request.meta['imageType'] = imageType
            request.meta['level1Url'] = level1Url
            yield request

    def get_level2(self, response):
        '''
        :param response:
        :return:
        '''
        nums = response.xpath("//div[4]/ul/li/span/strong[1]/text()")[0].extract()
        if nums == 1:
            pass
        else:
            for i in range(1, int(nums) + 1):
                imgurl = response.meta['level1Url'] + 'list' + '_' + str(i) + '.html'
                request = scrapy.Request(imgurl, callback=self.get_imagesurl)
                request.meta['imageType'] = response.meta['imageType']
                request.meta['level1Url'] = response.meta['level1Url']
                yield request

    def get_imagesurl(self, response):
        """
        获取图片url
        :param response:
        :return:
        """
        imageslist = response.xpath('//div[@class="auto gallery"]/ul/li/a/@href').extract()
        imagenamelist = response.xpath('// div / ul / li / div / p /a/text()').extract()  # 图片名字

        for i in range(0, len(imageslist)):
            imagesurl = 'http://www.bizhiku.net' + imageslist[i]
            imagename = imagenamelist[i]
            request = scrapy.Request(imagesurl, callback=self.get_images)
            request.meta['imageType'] = response.meta['imageType']
            request.meta['imagename'] = imagename
            yield request

    def get_images(self, response):
        """
        # 获取不同类型图片
        :param response:
        :return:
        """
        imageurl = response.xpath('//*[@id="bigimg"]/@src')[0].extract()
        item = items.BizhiItem()
        item['imageType'] = response.meta['imageType']  # 分类
        item["imagename"] = response.meta['imagename']  # 图片标题
        item['imageurl'] = imageurl  # 图片路径
        yield item
