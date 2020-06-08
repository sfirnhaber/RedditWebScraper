# RedditWebScraper
A python script that takes a subreddit name as an input, and downloads pictures that it can find from the top rated posts on that subreddit. Will not download images again if previously downloaded and put in the same location.


Options:


    -d, --directory
  
    Name of directory location to store images in.
    
    -l, --limit
  
    The amount of pictures the script will attempt to find.
    
    -s, --subreddit
  
    The name of the subreddit to grab pictures from.


 Usage Example:
 
    python redditScraper.py -s cats -l 15 -d images
  
    Will put up to 15 images from the "cats" subreddit and store them in a local file called "images"
