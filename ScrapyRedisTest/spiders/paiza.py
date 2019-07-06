from scrapy_redis.spiders import RedisSpider
from urllib import parse
from scrapy.http import Request

class PaizaSpider(RedisSpider):
    name = 'paiza'
    # allowed_domains = ['paiza.jp']
    redis_key = "paiza:start_urls"

    def parse(self, response):
        post_urls = response.xpath("//a[@class='c-job_offer-box__header__title__link']/@href").getall()
        img_urls = response.xpath("//img[@class='c-job_offer-recruiter__thumbnail']/@src").getall()

        for post_url, img_url in zip(post_urls, img_urls):
            """parse.urljoinでurlを補充する"""
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_img_url": img_url},
                          callback=self.parse_detail, dont_filter=True)
            next_urls = response.xpath("//li[@class='next']/a/@href").get()
            if next_urls:
                # 次のページのurlを返す
                yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        """
                企業名 name
                ポジション  position
                年収  income
                画像 images
                特徴 content
                url
                url_object_id(プレミアムキー代わり)
                :return:
                """
        pass
        # article_item = PaizaArticleItem()
        #
        # title = response.xpath("//h2[@class='ttl mt0 mb0']/text()").get()
        # position = response.xpath("//td[@class='font16']/strong/text()").get()
        # income = response.xpath("//div[@class='strong font18 color_blue']/text()").get()
        # images = response.meta.get('front_img_url', '')
        # content = response.xpath("//div[@class='rBox font13 lineHeight17']/p/text()").getall()
        # content = ''.join(content)
        #
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['url'] = response.url
        # article_item['name'] = title
        # article_item['position'] = position
        # article_item['income'] = income
        # article_item['images'] = [images]
        # article_item['content'] = content
        # article_item['create_date'] = datetime.now().date()
        # yield article_item