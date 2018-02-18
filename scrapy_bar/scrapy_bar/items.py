
import scrapy


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
