import argparse

argument_parser = argparse.ArgumentParser()

subreddit_submission_group = argument_parser.add_mutually_exclusive_group(required=True)
subreddit_submission_group.add_argument('-S', '--submission-id', dest='submission_id', help='Specify submission.')
subreddit_submission_group.add_argument('-s', '--subreddit', dest='subreddit', help='Specify subreddit.')
argument_parser.add_argument('-t', '--title', action='store_true', dest='title', help='Enable submission title')
argument_parser.add_argument('-b', '--body', action='store_true', dest='body', help='Enable submission body')
argument_parser.add_argument('-l', '--max-length', type=int, dest='max_length', help='Specify max length of comments in characters.')
argument_parser.add_argument('-c', '--comments_count', type=int, dest='comments_count', default=3, help='Set number of comments. -1: all comments, 0: no comments, number: number of comments.')
argument_parser.add_argument('-o', '--strong', action='store_true', dest='strong', help='Set only strong option to true')
argument_parser.add_argument('-a', '--auto-scrape', action='store_true', dest='auto_scrape', help='Run scraper automatically if there are no scraped submissions in the database.')
argument_parser.add_argument('-i', '--limit-submissions', type=int,  dest='limit_submissions', default=25, help='Scraper: limit submission count')
argument_parser.add_argument('-I', '--limit-comments', type=int, dest='limit_comments', default=25, help='Scraper: limit comment count')