#!/bin/bash
# Tetun Crawler Pipeline

# echo "Initiating the crawling process ..."

# Generate seed words and seed URLS
# Loop to run the seeder.py script 10 times
for i in {1..10}; do
   echo "Generating seed words and seed URLS for the $i time ..."
   python3 ./pipeline/seeder.py
done

# Crawling the World Wide Web for 15 rounds
echo "Crawling the World Wide Web ..."
cd nutch
./bin/crawl -i -s urls/ --hostdbupdate --hostdbgenerate crawl/ 15
cd ..
# # Crawling process is concluded
echo "The crawling have been successfully concluded."

# Construct the text corpus
echo "Constructing text corpus ..."
python3 ./pipeline/construct_corpus.py
# Corpus construction process is concluded
echo "The corpus have been successfully generated."

# Generate collection statistic
echo "Generating statistic for the collection ..."
python3 ./pipeline/view_collection_stat.py
# Statistic generation process is concluded
echo "The statistics have been successfully generated."
