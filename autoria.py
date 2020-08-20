import scrapy


def clean(text):
    digits = [symbol for symbol in text if symbol.isdigit()]
    cleaned_text = ''.join(digits)
    if not cleaned_text:
        return None
    return int(cleaned_text)


class Cars(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://auto.ria.com/uk/car/bmw/', ]

    def parse(self, response):
        for cars in response.css('.content'):
            link = cars.css('a.address')
            title = link.css('span.bold::text').get()
            year = link.css('::text').get()
            raw_mileage = cars.css('li.item-char::text').get()
            price = cars.css('span.size22::text').get()
            href = link.css('::attr(href)').get()

            mileage = raw_mileage and clean(raw_mileage) or None
            yield {
                'title': title,
                'year': year,
                'mileage': mileage,
                'price': price,
                'href': href,
            }