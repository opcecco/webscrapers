#!/usr/bin/env python

#
# Download and parse all Jake and Amir episode titles and scripts from scripts.jakeandamir.com
#
# Usage: python jake_amir_scrape.py OUTPUT_FILE
#  OUTPUT_FILE - File to write scripts to
#

import sys, requests, lxml.html


def ascii_only(s):
	return ''.join(c for c in s if ord(c) < 128)
	
	
def main():
	print 'Loading page...'
	page = requests.get('http://scripts.jakeandamir.com/index.php?search=amir&do-search=1', stream = False, timeout = 5.0)
	
	print 'Parsing content...'
	tree = lxml.html.fromstring(page.content)
	
	raw_title_list = tree.xpath('//td[@class="header-inner-title"]/text()[normalize-space()]')
	episode_divs = tree.xpath('//div[@class="episode-script-inner"]')
	raw_script_list = [div.xpath('text()[normalize-space()]') for div in episode_divs]
	
	with open(sys.argv[1], 'w') as output_file:
		for i in xrange(len(raw_title_list)):
			
			title = ascii_only(raw_title_list[i].strip())
			script = '\n'.join(ascii_only(line.strip()) for line in raw_script_list[i] if 'http://' not in line)
			
			output_file.write('Script Title: %s\n\n%s\n\n-----\n\n' % (title, script))
			
	print 'Scraped %d scripts.' % len(raw_title_list)
	
	
if __name__ == '__main__':
	main()
	