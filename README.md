# ESPN NBA article extractor

This is some quick and dirty code for a data science project to extract NBA article text from ESPN's archived NBA articles.

1. Run "python article_extractor.py" to download the html's of the ESPN articles for the current month. They will be stored in the "articles" folder.
2. Run "python extract_raw_text.py" to extract the raw text from the html documents and store them in the "raw_text" folder

## Dependencies

goose (https://github.com/grangier/python-goose)  
urllib2  
bs4
