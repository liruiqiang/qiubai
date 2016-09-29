import scrapy
from qiubai.items import QiubaiItem
from scrapy.http import Request

class QiuBaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls =["http://www.qiushibaike.com/",]

    def parse(self,response):
        for href in response.xpath('//span[@class="stats-comments"]/a/@href').extract():
            detail_url = response.urljoin(href)
            req = Request(detail_url,self.parse_detail_page)
            item = QiubaiItem()
            req.meta['item']=item
            yield req

    def parse_detail_page(self,response):
        item = response.meta["item"]
        item["author"] = response.xpath('//div[@class="author clearfix"]/a[2]/h2/text()').extract()[0] if response.xpath('//div[@class="author clearfix"]/a[2]/h2/text()').extract() else ""
        item["content"] = response.xpath('//div[@class="article block untagged noline mb15"]/div/div[@class="content"]/text()').extract()[0:]
        comments = []
        for comment in response.xpath('//div[starts-with (@class,"comment-block clearfix floor")]'):
            comment_author = comment.xpath('./div[@class="replay"]/a/text()').extract()[0]
            comment_content = comment.xpath('./div[@class="replay"]/span/text()').extract()[0] if comment.xpath('./div[@class="replay"]/span/text()').extract() else ""
            comments.append({"comment_author":comment_author,"comment_content":comment_content})
        item["comments"]=comments
        yield item
