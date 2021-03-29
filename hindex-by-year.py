#!/usr/bin/python3

from scholarly import scholarly
import argparse
import sys

def computeHindex(pub_cites_per_year, year):
  cites_per_pub = []
  for cites_per_year in pub_cites_per_year:
    count = 0
    for k,v in cites_per_year.items():
      if k <= year:
        count += v
    cites_per_pub.append(count)

  cites_per_pub.sort(reverse=True)
  hindex = 0
  pcount = 0
  for c in cites_per_pub:
    pcount += 1
    if c >= pcount:
      hindex += 1
    else:
      break

  return hindex

# Parse CLI args
parser = argparse.ArgumentParser(description='Compute h-index of a given author by year')
parser.add_argument('--from-year', metavar='<year>', type=int, nargs='?', default=0,  help='First year to consider for h-index computation')
parser.add_argument('--to-year', metavar='<year>', type=int, nargs='?', default=10000, help='Last year to consider for h-index computation')
parser.add_argument('author', metavar='<author>', type=str, nargs='+',
                    help='The target author name on Google Scholar')
args = parser.parse_args()
firstYear = args.from_year
lastYear = args.to_year
author = ' '.join(args.author)

# Query Scholar and index citations per publication per year
print("Scanning publications for author '%s'..." % author)
search_query = scholarly.search_author(author)
authorObject = scholarly.fill(next(search_query))
pub_cites_per_year = []
minYear = 10000
maxYear = 0
for p in authorObject['publications']:
  pub = scholarly.fill(p)
  cites_per_year = pub['cites_per_year']
  pub_cites_per_year.append(cites_per_year)
  bib = pub['bib']
  print(" * '%s' (%d)" % (bib['title'], sum(cites_per_year.values())))
  if 'pub_year' not in bib or bib['pub_year'] == 'NA':
    continue
  year = int(bib['pub_year'])
  if year < minYear:
    minYear = year
  if year > maxYear:
    maxYear = year

# Compute a h-index for each year considered
if firstYear < minYear:
  firstYear = minYear
if lastYear > maxYear:
  lastYear = maxYear
print("The h-index of %s at the end of [%d-%d] is:" % (author, firstYear, lastYear))
for year in range(firstYear, lastYear+1):
  hindex = computeHindex(pub_cites_per_year, year)
  print(" %d: %d" % (year, hindex))