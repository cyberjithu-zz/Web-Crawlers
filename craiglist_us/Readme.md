# Craiglist Services in  U.S
Extract `Services` data from the `craiglist.org`

## Running the spider
```scrapy crawl craiglist```

## Sample output
```
{
	'categories': [u 'SF bay area', u 'services', u 'real estate services'],
	'description': u 'Lovely office in suite with 4 other therapists available for sublet on Fridays. The office building is located in west Dublin near the 580/680 interchange, near Pleasanton and San Ramon. Off-street parking available. Office is on second-floor, with large waiting room with call light, and kitchen with full-sized refrigerator and microwave. We are a friendly group of therapists who provide referrals to one another frequently which can help with building a practice. Rent is $175 per month which includes utilities and weekly housecleaning. Please contact Linda Brunson, Ph.D. at show contact info',
	'geo': {
		'latitude': u '37.701302',
		'longitude': u '-121.938463'
	},
	'post': {
		'id': u '5386698939',
		'posted_on': u '2016-01-03 10:09pm',
		'updated_on': u '2016-01-24 8:52pm'
	},
	'title': u 'Psychotherapy Office for Sublet',
	'url': 'http://sfbay.craigslist.org/eby/rts/5386698939.html'
}
```