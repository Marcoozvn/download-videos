# Alura-Scraper
Scrap all videos from a formation you want and download'em automatically(downloading is optional).
Attention, you need to be a paid member to work. And nope, I didn't code anything to treat errors like wrong username/password or link yet.

By the way, the links for the video resets daily. Pay attention when downloading.

# Documentation
class AluraLogin:  
-Login on the site. Only needed to crawl and scrap a formation.  
-Uses AluraScraper and AluraCrawler as subclasses, so you only need to create one object.
  
class AluraScraper:  
-scraps categories formations from formation page  
-scraps json requests from video links  
-Saves formation categories, formation category, and formations from a category in properties    
usage: AluraScraper.formations, AluraScraper.categories, AluraScraper.category 

class AluraCrawler:  
-Choose formation you wanna crawl  
-crawls formation links with video
-Saves link formation and links with video from a formation into properties.
usage: AluraCrawler.link, AulraCrawler.links


# File Parser Documentation
def json_decoder():  
  decodes json chunks from a text file
 
def get_files():  
  download batch of links from a text file
