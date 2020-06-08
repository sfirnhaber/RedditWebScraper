import os
import praw
import imgur_downloader as imgur
import requests
from os.path import basename
from optparse import OptionParser


# Reddit praw information:
CLIENT_ID = "RmAOAK0MYDx4xA"
CLIENT_SECRET = "wIraga8GRcswVA_VUgktt_TkrMk"
AGENT_NAME = "WebScrapeBot"


def parse_inputs():
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="dir_location", default="images",
                      help="Name of directory location to store images in.")
    parser.add_option("-l", "--limit", dest="pic_limit", type="int", default=10,
                      help="The amount of pictures the script will attempt to find.")
    parser.add_option("-s", "--subreddit", dest="subreddit", default="",
                      help="The name of the subreddit to grab pictures from.")
    return parser.parse_args()[0]


def create_folder(path):
    path = os.getcwd() + "\\"+ path + "\\"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# Works for i.redd.it
def download_image(link, path, dir_name_length):
    basename_link = basename(link)
    if not os.path.exists(path + basename_link):
        with open(basename_link, "wb") as f:
            f.write(requests.get(link).content)
            f.close()
            # Moves image from local area to folder that stores images
            os.rename(path[:-(dir_name_length + 1)] + basename_link, path + basename_link)
            return True
    return False


def get_pictures(posts, path, dir_name_length):
    count = 0
    for post in posts:
        if post.url[8:17] == "i.redd.it":
            count += download_image(post.url, path, dir_name_length)
        elif post.url[8:17] == "v.redd.it":
            continue  # Maybe in a future version that supports downloading videos
        elif post.url[8:19] == "i.imgur.com":
            count += len(imgur.ImgurDownloader(post.url, path).save_images()[0])
    return count


def print_output(pic_count):
    if pic_count == 0:
        print("Found 0 new pictures.")
    else:
        print("Found %s new picture%s. Placed into \"%s\" folder"
              % (pic_count, ("s" if pic_count > 1 else ""), options.dir_location))


reddit = praw.Reddit(client_id= CLIENT_ID,
                     client_secret= CLIENT_SECRET,
                     user_agent= AGENT_NAME)

options = parse_inputs()
if (options.subreddit == ""):
    print("Please enter a subreddit name.")
    exit(-1)
folder_path = create_folder(options.dir_location)
posts = reddit.subreddit(options.subreddit).top(limit=options.pic_limit)
pic_count = get_pictures(posts, folder_path, len(options.dir_location))
print_output(pic_count)
