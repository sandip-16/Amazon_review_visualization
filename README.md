# review_visualization
Amazon product review analysis and visualization


Technologies: Python, Flask , HTML, CSS, JINJA Framework, Mongodb Database, NLTK, Matplotlib

- database contains two collections 
	1: For Amazon review data
	2: User Authentication
- libraries needed
	1: Numpy
	2: Pandas
	3: Matplotlib
	4: nltk
	5: flask

- We process each review by passing it to nltk and then calcualte the polar scores of each review. accordingly we update the positive, negative and neutral count of each and every review and based on this processing we plot our top 5 products and the induvisual product analysis.


Review data format:
{
  "reviewerID": "A2SUAM1J3GNN3B",
  "asin": "0000013714",
  "reviewerName": "J. McDonald",
  "helpful": [2, 3],
  "reviewText": "I bought this for my husband who plays the piano.  He is having a wonderful time playing these old hymns.  The music  is at times hard to read because we think the book was published for singing from more than playing from.  Great purchase though!",
  "overall": 5.0,
  "summary": "Heavenly Highway Hymns",
  "unixReviewTime": 1252800000,
  "reviewTime": "09 13, 2009"
}

Where,
reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
asin - ID of the product, e.g. 0000013714
reviewerName - name of the reviewer
helpful - helpfulness rating of the review, e.g. 2/3
reviewText - text of the review
overall - rating of the product
summary - summary of the review
unixReviewTime - time of the review (unix time)
reviewTime - time of the review (raw)
