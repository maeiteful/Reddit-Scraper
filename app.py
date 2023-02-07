import praw
import requests
from pytube import YouTube
import os



user_agent = "Scraper myro"
reddit = praw.Reddit(
    client_id= 'HO2fzJOdcIPsVyfgJT6sAA',
    client_secret = 'o167oBShCm5OnmjnBSrArdZGMXohMQ',
    user_agent=user_agent
)

video_extensions = ['.mp4', '.webm']

#                           Customizations

SAVE_PATHs = "D:/dekstop/VS code/Work/web scraping/redditapi/videos"
subreddit = reddit.subreddit('aww')
commentLimit= 10
submissionLimit =6
commentSort_mode = "best" # change this to the comment sorting method you want to use(e.g best, top, new, controversial, hot)
sort_mode = "hot" # change this to the sorting method you want to use (e.g. hot, new, rising, top, etc.)
time_filter = "day" # change this to the time filter you want to use (e.g. hour, day, week, month, year, all)






if sort_mode == "hot":
    submissions = subreddit.hot()
elif sort_mode == "new":
    submissions = subreddit.new()
elif sort_mode == "top":
    if time_filter == "day":
        submissions = subreddit.top("day")
    elif time_filter == "week":
        submissions = subreddit.top("week")
    elif time_filter == "month":
        submissions = subreddit.top("month")
    elif time_filter == "year":
        submissions = subreddit.top("year")
    elif time_filter == "all":
        submissions = subreddit.top("all")
elif sort_mode == "controversial":
    if time_filter == "day":
        submissions = subreddit.controversial("day")
    elif time_filter == "week":
        submissions = subreddit.controversial("week")
    elif time_filter == "month":
        submissions = subreddit.controversial("month")
    elif time_filter == "year":
        submissions = subreddit.controversial("year")
    elif time_filter == "all":
        submissions = subreddit.controversial("all")
        
for submission in submissions:
    if submission.is_video or 'youtube.com' in submission.url or 'youtu.be' in submission.url:
        file_name = submission.title + ".txt"
        file_path = os.path.join(SAVE_PATHs, file_name)
        
        
        submission.comments.replace_more(limit=None)
        comments = submission.comments.list()
        if commentSort_mode == "best":
            sorted_comments = sorted(comments, key=lambda comment: comment.score, reverse=True)
        elif commentSort_mode == "top":
            sorted_comments = sorted(comments, key=lambda comment: comment.score, reverse=True)
        elif commentSort_mode == "new":
            sorted_comments = sorted(comments, key=lambda comment: comment.created_utc, reverse=True)
        elif commentSort_mode == "controversial":
            sorted_comments = sorted(comments, key=lambda comment: comment.controversiality, reverse=True)
        elif commentSort_mode == "hot":
            sorted_comments = sorted(comments, key=lambda comment: comment.ups, reverse=True)

        with open(file_path, "w", encoding='utf-8') as f:
             f.write(f"Title: {submission.title}\nURL: {submission.url}\n")
             for comment in sorted_comments[:commentLimit]:
                 author = comment.author
                 f.write(f"Author: {author}\nComment: {comment.body}\n")
    
    if submission.is_video:
        video_url = submission.media['reddit_video']['fallback_url']
        print(submission.title)
        print(video_url)
        response = requests.get(video_url)
        with open(os.path.join(SAVE_PATHs , submission.title + '.mp4') , 'wb') as f:
            f.write(response.content)
        print("\n")
    
    if 'youtube.com' in submission.url or 'youtu.be' in submission.url:
        print(submission.title)
        print(submission.url)
        try:
            yt = YouTube(submission.url)
            yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution')[-1].download(SAVE_PATHs, filename=submission.title+".mp4")
            print('Video Downloaded!')
        except Exception as e:
            print("Error occurred!\n", e)
        print("\n")
    