import psycopg2
import scrapy
from scrapy import Spider, Request
import uuid

# Set up a connection to the postgres server.
conn_string = "host=localhost port=5432 dbname=scrapy user=michael"
conn=psycopg2.connect(conn_string)
print("Connected!")

cur = conn.cursor()

class ScrapyBarItem(scrapy.Item):
	barName = scrapy.Field()
	barCategory = scrapy.Field()
	barPriceRange = scrapy.Field()
	barNumberReviews = scrapy.Field()
	barNumberStars = scrapy.Field()
	barHood = scrapy.Field()
	barPhone = scrapy.Field()
	barReservations = scrapy.Field()
	barCreditCard = scrapy.Field()
	barParking = scrapy.Field()
	barWeelchair = scrapy.Field()
	barAttire = scrapy.Field()
	barDancing = scrapy.Field()
	barHappy = scrapy.Field()
	barOutdoor = scrapy.Field()
	barTV = scrapy.Field()
	barDogs = scrapy.Field()
	barPoolTable = scrapy.Field()

class Scrapy_bar(Spider):
	name = 'bar_spider'
	allowed_urls = ['https://www.yelp.com/']
	start_urls = ['https://www.yelp.com/search?find_desc=bars&find_loc=Manhattan,+NY&start=' + str(n) for n in range(0,1000,10)]

	def parse(self, response):
		# bars = response.xpath('//a[contains(@data-analytics-label,"biz-name")]//@href').extract()
		# bars = response.xpath('/h3/a//@href').extract()
		bars = response.xpath('//a[starts-with(@href, "/biz")]/@href').extract()
		bar_urls = ['https://www.yelp.com' + bar for bar in bars]

		for url in bar_urls:
			yield Request(url, callback=self.parse_bar)


	def parse_bar(self, response):
		barName = response.xpath('//h1[contains(@class,"biz-page-title embossed-text-white")]/text()').extract()
		if len(barName) > 1:
			barName = ' '.join(barName)
		else:
			barName = barName[0]

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

		barReservations = (attributes['Takes Reservations'] if 'Takes Reservations' in attributes.keys() else None)
		barCreditCard = (attributes['Accepts Credit Cards'] if 'Accepts Credit Cards' in attributes.keys() else None)
		barParking = (attributes['Parking'] if 'Parking' in attributes.keys() else None)
		barWeelchair = (attributes['Wheelchair Accessible'] if 'Wheelchair Accessible' in attributes.keys() else None)
		barAttire = (attributes['Attire'] if 'Attire' in attributes.keys() else None)
		barDancing = (attributes['Good For Dancing'] if 'Good For Dancing' in attributes.keys() else None)
		barHappy = (attributes['Happy Hour'] if 'Happy Hour' in attributes.keys() else None)
		barOutdoor = (attributes['Outdoor Seating'] if 'Outdoor Seating' in attributes.keys() else None)
		barTV = (attributes['Has TV'] if 'Has TV' in attributes.keys() else None)
		barDogs = (attributes['Dogs Allowed'] if 'Dogs Allowed' in attributes.keys() else None)
		barPoolTable = (attributes['Has Pool Table'] if 'Has Pool Table' in attributes.keys() else None)

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

		cur.execute("SELECT * from bars where bar_name = %s", (barName,))
		res = cur.fetchall()

		if len(res) == 0:
			cur.execute("INSERT INTO bars (id, bar_name, bar_category, bar_price_range, bar_number_reviews, bar_number_stars, bar_hood, bar_phone, bar_reservations, bar_credit_card, bar_parking, bar_weel_chair, bar_attire, bar_dancing, bar_happy, bar_outdoor, bar_tv, bar_dogs, bar_pool_table) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (str(uuid.uuid4()), barName, barCategory, barPriceRange, barNumberReviews, barNumberStars, barHood, barPhone, barReservations, barCreditCard, barParking, barWeelchair, barAttire, barDancing, barHappy, barOutdoor, barTV, barDogs, barPoolTable))
			conn.commit()

		yield item
