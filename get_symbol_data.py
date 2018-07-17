import urllib.request
import json
import pymongo
import datetime


# http://api.mongodb.com/python/current/tutorial.html
symb_key = '@@SYM@@'
base_url = 'https://finance.yahoo.com/quote/' + symb_key + '/history?p=' + symb_key
rw_user = 'HistoricalPriceStore0_RW';
rw_pass = 'Ki4,8BNo6SbA1CbTvuY50.RW';
mongo_svr = 'historicalpricestore0-h0pai.mongodb.net';
mongo_cxn = 'mongodb+srv://' + rw_user + ':' + rw_pass + '@' + mongo_svr + '/test?retryWrites=true'


def make_url(ticker_symbol):
    return base_url.replace(symb_key, ticker_symbol)


def get_historical_price_store(ticker_symbol):
    url = make_url(ticker_symbol)
    chunks = ''
    print(url)
    with urllib.request.urlopen(url) as f:
        chunks += f.read().decode('utf-8')

    parts = chunks.split('HistoricalPriceStore')
    prices_array = parts[1].split(']')
    actual_prices_array = prices_array[0].split('[')
    data_string = '{"prices":[' + actual_prices_array[1] + ']}'
    data_out = json.loads(data_string)
    return data_out['prices']


def add_and_fetch_data():
	client = pymongo.MongoClient(mongo_cxn)
	db = client.test
	collection_name = 'posts'
	collection = db[collection_name]
	post = {'author': 'Mike', 'text': 'My first blog post!', 'tags': ['mongodb', 'python', 'pymongo'], 'date': datetime.datetime.utcnow()}
	post_id = collection.insert_one(post).inserted_id
	print(post_id)
	print(collection.find_one())
	client.close()
	

def json_fix(penny_stock, json_in):
	print(str(penny_stock) + ' >>> ' + str(json_in))
	from_quote = "'"
	to_quote = '"'
	return str(json_in).replace(from_quote, to_quote)


def datetime_from_long(long_date_string):
	long_date = int(str(long_date_string))
	return datetime.datetime.fromtimestamp(long_date).strftime('%Y-%m-%d %H:%M:%S')

	
def load_data():
	print('Starting the load process ...')
	
	penny_stocks = ['AAPL','ABIL','RKDA','GEVO','NAKD','CRON','GEVO','EGY','DEST','BLNK','SNES','SNES','DPW','JVA','AVXL','CRON','POTN','KBLB','BLNK']
	
	client = pymongo.MongoClient(mongo_cxn)
	db = client.test
	
	for penny_stock in penny_stocks:
		result_messages = ''
		prices = get_historical_price_store(penny_stock)
		collection = db[penny_stock]
		previous_count = collection.count_documents({})
		incoming_count = len(prices)
		for price in prices:
			price_string = json_fix(penny_stock, price)
			price_details = json.loads(price_string)
			date_key = price_details['date']
			search_arg = {'date': date_key}
			match_index = 0
			match_messages = ''
			matches = collection.find(search_arg)
			for match in matches:
				match_index += 1
				match_messages += str(match_index) + '=>' + str(match) + ';'				
			if match_index == 0:
				message = str(penny_stock) + ' No matches for [' + str(datetime_from_long(date_key)) + '] ' + str(search_arg)
				print(message)
			if match_index > 1:
				message = str(penny_stock) + ' Multiple matches for [' + str(datetime_from_long(date_key)) + '] ' + str(search_arg) + ' => ' + str(match_messages)
				print(message)
			result = collection.replace_one(search_arg, price, upsert=True)
			if match_index != 1:
				result_messages += str(penny_stock) + ' DATE: ' + str(datetime_from_long(date_key)) + ' [' + str(date_key) + '] result=' + str(result.raw_result) + '\n'
		
		current_count = collection.count_documents({})
		if incoming_count != current_count:
			message = str(penny_stock) + ' STATS: incoming_count=' + str(incoming_count) + '; previous_count=' + str(previous_count) + '; current_count=' + str(current_count)
			print(message)
			if len(result_messages) > 0:
				print(result_messages)
	
	client.close()
	print('All done!')


def main():
	load_data()
	# some test code here ...
	add_and_fetch_data()
	print(datetime_from_long(1530624600))
	print(datetime_from_long(1531771201))
	print(datetime_from_long(1516804200))
	
	
if __name__== '__main__':
	main()
