

from scrapy import Spider, Request
#from scrapy.selector import Selector
from scrapy_bar.items import ScrapyBarItem

class Scrapy_bar(Spider):
	name = 'bar_spider'
	allowed_urls = ['https://www.yelp.com/']
	start_urls = ['https://www.yelp.com/search?find_desc=bars&find_loc=Manhattan,+NY&start=' + str(n) for n in range(0,1000,10)]


	def parse(self, response):
		bars = response.xpath('//a[contains(@data-analytics-label,"biz-name")]//@href').extract()
		bars = ['https://www.yelp.com' + bar for bar in bars]

		for url in bars:
			yield Request(url, callback=self.parse_bar)


	def parse_bar(self, response):


		barName = response.xpath('//h1[contains(@class,"biz-page-title embossed-text-white shortenough")]/text()').extract()[0].strip()
		barCategory = response.xpath('//span[contains(@class,"category-str-list")]/a/text()').extract()[0]
		barPriceRange = response.xpath('//span[contains(@class,"business-attribute price-range")]/text()').extract()[0]
		barNumberReviews = int(response.xpath('//span[contains(@class,"review-count rating-qualifier")]/text()').extract()[0].split()[0])
		barNumberStars = float(response.xpath('//div[contains(@class,"biz-rating biz-rating-very-large clearfix")]//@title').extract()[0].split()[0])
		barHood = response.xpath('//span[contains(@class,"neighborhood-str-list")]/text()').extract()[0].strip()
		barPhone = response.xpath('//span[contains(@class,"biz-phone")]/text()').extract()[0].strip()

		key=response.xpath('//div[contains(@class,"short-def-list")]//dt/text()').extract()
		key = [x.strip() for x in key]

		value = response.xpath('//div[contains(@class,"short-def-list")]//dd/text()').extract()
		value =  [x.strip() for x in value]

		attributes = dict(zip(key,value))

		barReservations = (attributes['Takes Reservations'] if 'Takes Reservations' in attributes.keys() else 'N/A')
		barCreditCard = (attributes['Accepts Credit Cards'] if 'Accepts Credit Cards' in attributes.keys() else 'N/A')
		barParking = (attributes['Parking'] if 'Parking' in attributes.keys() else 'N/A')
		barWeelchair = (attributes['Wheelchair Accessible'] if 'Wheelchair Accessible' in attributes.keys() else 'N/A')
		barAttire = (attributes['Attire'] if 'Attire' in attributes.keys() else 'N/A')
		barDancing = (attributes['Good For Dancing'] if 'Good For Dancing' in attributes.keys() else 'N/A')
		barHappy = (attributes['Happy Hour'] if 'Happy Hour' in attributes.keys() else 'N/A')
		barOutdoor = (attributes['Outdoor Seating'] if 'Outdoor Seating' in attributes.keys() else 'N/A')
		barTV = (attributes['Has TV'] if 'Has TV' in attributes.keys() else 'N/A')
		barDogs = (attributes['Dogs Allowed'] if 'Dogs Allowed' in attributes.keys() else 'N/A')
		barPoolTable = (attributes['Has Pool Table'] if 'Has Pool Table' in attributes.keys() else 'N/A')


		item = ScrapyBarItem()
		item['barName'] = barName
		item['barCategory'] = barCategory
		item['barPriceRange'] = barPriceRange
		item['barNumberReviews'] = barNumberReviews 
		item['barNumberStars'] = barNumberStars 
		item['barHood'] = barHood 
		item['barPhone'] = barPhone
		item['barReservations'] = barReservations
		item['barCreditCard'] = barCreditCard
		item['barParking'] = barParking
		item['barWeelchair'] = barWeelchair
		item['barAttire'] = barAttire
		item['barDancing'] = barDancing
		item['barHappy'] = barHappy
		item['barOutdoor'] = barOutdoor
		item['barTV'] = barTV
		item['barDogs'] = barDogs
		item['barPoolTable'] = barPoolTable

		yield item
