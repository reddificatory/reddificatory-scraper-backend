import os
import config
# import scraper
import file
import text_processor
import text_to_speech
import database.submissions
import database.comments
import logger
import argparse

argument_parser = argparse.ArgumentParser()
subreddit_submission_group = argument_parser.add_mutually_exclusive_group(required=True)
subreddit_submission_group.add_argument('-S', '--submission', dest='submission', help='Specify submission.')
subreddit_submission_group.add_argument('-s', '--subreddit', dest='subreddit', help='Specify subreddit.')
argument_parser.add_argument('-t', '--title', action='store_true', dest='title', help='Enable submission title')
argument_parser.add_argument('-b', '--body', action='store_true', dest='body', help='Enable submission body')
argument_parser.add_argument('-l', '--length', dest='length', choices=['short', 'long'], default='short', help='Specify length of comments.')
argument_parser.add_argument('-c', '--comments', dest='comments', default=3, help='Set number of comments. -1: all comments, 0: no comments, number: number of comments.')
arguments = argument_parser.parse_args()

def main():
    submission_id = None
    if arguments.submission:
        submission_id = arguments.submission
    else:
        submission_id = database.submissions.get_random_submission(arguments.subreddit)

    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit
    save_path = file.get_save_path(os.path.join('media', 'reddit'), submission_id)
    comment_length = arguments.length
    comment_count = int(arguments.comments)
    texts = []

    if arguments.title:
        texts.append(submission.title)

    if arguments.body:
        texts.append(submission.body)

    # TODO: implement getting every comment
    # TODO: implement comment length
    # TODO: implement bot comment filtering
    # TODO: rewrite database queries to suite the new options
    if comment_count != 0 or comment_count != -1:
        comment_ids = database.comments.get_random_comments(submission_id, comment_count)
        for comment_id in comment_ids:
            comment = config.REDDIT_CLIENT.comment(comment_id)
            texts.append(text_processor.remove_duplicate_newlines(comment.body))

    print(arguments, texts)

if __name__ == '__main__':
    main()

# subreddit = 'askreddit'
# submission_id = database.submissions.get_random_submission()
# save_path = file.get_save_path(os.path.join('media', 'reddit'), submission_id)