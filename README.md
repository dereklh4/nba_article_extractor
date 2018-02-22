# Stage 1 - Extracting Person Names from ESPN NBA Articles

This is the code repository for extracting person names from espn nba articles. Section 1 shows how we downloaded the articles from ESPN. Section 2 describes the labeling process. Section 3 describes the training process.

## 1. ESPN NBA article extractor

This is some quick and dirty code for a data science project to extract NBA article text from ESPN's archived NBA articles.

1. Run "python article_extractor.py" to download the html's of the ESPN articles for the current month. They will be stored in the "html_articles" folder.
2. Run "python extract_raw_text.py" to extract the raw text from the html documents and store them in the "raw_text" folder

The html of the articles is stored in the folder "html_articles". The raw text is stored in the "raw_text" folder.

## 2. Labeling

We labeled all occurances of person names in 300 documents with the tag </> (e.g Jack is labeled \<Jack/\>). Those markings can be found in "marked_raw_html". We split those marked documents into two sets: set I for training, set J for testing.

## 3. Training

For training we needed to extract examples from the text with features and labels. The process can be found in "example_generator.py". It extracts examples from the text, prunes away obvious non-names (e.g not capitalized, odd punctuation, etc), generates features for the examples (e.g. contains common first name, contains NBA team or city, etc), and labels it accordingly (is it tagged?). Using the extracted positive and negative examples, we could develop a learning algorithm.

The best algorithm we found for this problem was the Random Forest Algorithm. It was able to achieve precision of 92.6% and recall of 92.4%. The comparison's of the learning algorithms can be observed in "compare_classifier.ipynb"

### Dependencies (for step 1)

goose (https://github.com/grangier/python-goose)  
urllib2  
bs4
