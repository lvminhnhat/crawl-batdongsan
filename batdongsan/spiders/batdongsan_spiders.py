from scrapy import Spider
from scrapy.selector import Selector
from urllib.parse import urlencode
from batdongsan.items import BatdongsanItem
import scrapy

API_KEY = "3b54368f-b7ca-430a-989f-b30bb8fbf003"
class CrawlerSpider(Spider):
    name = "batdongsan"
    allowed_domains = ["batdongsan.com.vn" , "proxy.scrapeops.io"]
    

    def start_requests(self):
        urls = [
            "https://batdongsan.com.vn/nha-dat-ban",
        ]
        # muốn lấy nhiều thì tăng vòng lặp lên. Ví dụ muốn lấy 100 trang thì
        for i in range(2, 100):
            urls.append("https://batdongsan.com.vn/nha-dat-ban/p" + str(i))
        for url in urls:
            yield scrapy.Request(url=self.get_scrapeops_url(url), callback=self.parse)
    def get_scrapeops_url(self,url):
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
    

    def parse(self, response):
        # lấy ra tất cả các link có  class = "js__product-link-for-product-id"
        # và lưu vào biến links
        links = response.css(".js__product-link-for-product-id::attr(href)").extract()
        url = "https://batdongsan.com.vn"
        for link in links:
            # duyệt qua từng link trong links
            # và gọi hàm parse_item để lấy dữ liệu
            print("Crawling: ",url+link)
            yield scrapy.Request(self.get_scrapeops_url(url+link), callback=self.parse_item)

    # hàm parse_item để lấy dữ liệu từ trang detail
    def parse_item(self, response):
        info = {}
        # lấy tên sản phẩm là thẻ h1 nằm trong thẻ div có id là "product-detail-web"
        name = response.css("#product-detail-web h1::text").extract_first()
        # lấy thông tin tất cả các thẻ div có XPath = "/html/body/div[8]/div/div[2]/div[1]/div[3]/div[8]"
        date = response.xpath('//*[@id="product-detail-web"]/div[8]')
        dateUpLoad = ""
        dateExpiration = ""
        code = ""
        # lấy ra tất cả các thẻ div có trong date
        dates = date.css("div")
        for d in dates:
            # title là text của thẻ span có class = "title"
            title = d.css(".title::text").extract_first()
            value = d.css(".value::text").extract_first()
            info[title] = value



        # thông tin đặt điểm bất đổng sản

        detail = response.xpath("/html/body/div[8]/div/div[2]/div[1]/div[3]/div[3]/div/div")
        # lấy ra tất cả các thẻ div có trong detail
        sections = detail.css("div")
        
        # duyệt qua từng section trong sections
        for section in sections:
            # lấy ra tất cả các thẻ div có class = "re__pr-specs-content-item"
            # và lưu vào biến attributes
            attributes = section.css(".re__pr-specs-content-item")
            # duyệt qua từng attribute trong attributes
            print ("Thông tin căn hộ:")
            for attribute in attributes:
                # lấy ra text của thẻ div có class = "re__pr-specs-content-item-title"
                key = attribute.css(".re__pr-specs-content-item-title::text").extract_first()
                # lấy ra text của thẻ div có class = "re__pr-specs-content-item-value"
                value = attribute.css(".re__pr-specs-content-item-value::text").extract_first()
                # lưu vào dict info
                print(key," - ", value)

                info[key] = value
            
        
        # lấy ra thông tin về giá
        price = info.get("Mức giá", "")
        # lấy ra thông tin về diện tích
        area = info.get("Diện tích", "")
        # lấy ra thông tin về số phòng ngủ
        bedRoom = info.get("Số phòng ngủ", "")
        # lấy ra thông tin về số phòng vệ sinh
        WC = info.get("Số toilet", "")
        # lấy ra thông tin về pháp lý
        legal = info.get("Pháp lý", "")
        dateUpLoad = info.get("Ngày đăng", "")
        dateExpiration = info.get("Ngày hết hạn", "")
        code = info.get("Mã tin", "")
        huongnha = info.get("Hướng nhà", "")
        # tạo ra 1 item để chứa tất cả thông tin
        item = BatdongsanItem()
        # gán các thông tin cho item
        item["Name"] = name
        item["DateUpLoad"] = dateUpLoad
        item["DateExpiration"] = dateExpiration
        item["Code"] = code
        item["Price"] = price
        item["Area"] = area
        item["BedRoom"] = bedRoom
        item["WC"] = WC
        item["Legal"] = legal
        item["HuongNha"] = huongnha
        # xuất item
        yield item


        #xuất info

