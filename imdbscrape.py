#!/usr/bin/env python

import sys, re, requests, random, time, lxml.html


def ascii_only(s):
	return ''.join(c for c in s if ord(c) < 128)
	
	
def main():
	print 'Loading movie titles...'
	
	with open(sys.argv[1], 'r') as input_file:
		all_data = (line.split('\t') for line in input_file)
		movie_data = [row for row in all_data if row[1] == 'movie']
		
		num_movies = int(sys.argv[3])
		random.shuffle(movie_data)
		movie_samples = movie_data[:num_movies]
		
	print 'Searching online for movie summaries...'
	
	with open(sys.argv[2], 'w') as output_file:
		for index, row in enumerate(movie_samples):
			
			id = row[0]
			title = ''.join([c for c in row[2] if ord(c) < 128])
			
			page = None
			while page is None:
				try:
					# time.sleep(0.5)
					page = requests.get('http://www.imdb.com/title/%s' % id, stream = False, timeout = 1.0)
				except requests.exceptions.Timeout as ex:
					print 'Timeout Error: %s\nRetrying...' % str(ex)
					time.sleep(2)
				except requests.exceptions.ConnectionError as ex:
					print 'Connection Error: %s\nRetrying...' % str(ex)
					time.sleep(2)
					
			tree = lxml.html.fromstring(page.content)
			parsed_summary = tree.xpath('//div[@class="article" and @id="titleStoryLine"]/div[@class="inline canwrap" and @itemprop="description"]/p/text()[normalize-space()]')
			parsed_genres = tree.xpath('//div[@class="see-more inline canwrap" and @itemprop="genre"]/a/text()')
			parsed_rating = tree.xpath('//div[@class="txt-block"]/span[@itemprop="contentRating"]/text()')
			
			percent = 100.0 * float(index) / float(num_movies)
			
			if len(parsed_summary) > 0 and len(parsed_genres) > 0 and len(parsed_rating) > 0:
				summary = ascii_only(parsed_summary[0].strip())
				genres = [ascii_only(genre.strip()) for genre in parsed_genres]
				rating = ascii_only(parsed_rating[0].strip())
				
				output_file.write('TITLE: %s\nSUMMARY: %s\nGENRE: %s\nRATING: %s\n\n' % (title, summary, ', '.join(genres), rating))
				print '%.02f%% - Scraped %s (%s)' % (percent, id, title)
			else:
				print '%.02f%% - Skipping %s (%s)' % (percent, id, title)
				
	print 'Done.'
	
	
if __name__ == '__main__':
	main()
	