import os
import config
import file
import text_processor
import text_to_speech
import database.submissions
import database.comments
import argparse
import image_generator

    # TODO: implement -a/--scrape option to run the scraper automatically if the submission is not scraped yet
    # TODO: rewrite database queries to suite the new options
    # TODO: figure out video transparency
    # TODO: rewrite image merging and video creation
    # TODO: implement bot comment filtering

argument_parser = argparse.ArgumentParser()
subreddit_submission_group = argument_parser.add_mutually_exclusive_group(required=True)
subreddit_submission_group.add_argument('-S', '--submission', dest='submission', help='Specify submission.')
subreddit_submission_group.add_argument('-s', '--subreddit', dest='subreddit', help='Specify subreddit.')
argument_parser.add_argument('-t', '--title', action='store_true', dest='title', help='Enable submission title')
argument_parser.add_argument('-b', '--body', action='store_true', dest='body', help='Enable submission body')
argument_parser.add_argument('-l', '--max-length', dest='max_length', help='Specify max length of comments in characters.')
argument_parser.add_argument('-c', '--comments', dest='comments', default=3, help='Set number of comments. -1: all comments, 0: no comments, number: number of comments.')
argument_parser.add_argument('-o', '--strong', action='store_true', dest='strong', help='Set only strong option to true')
arguments = argument_parser.parse_args()

def main():
    submission_id = None
    comment_max_length = None

    if arguments.submission:
        submission_id = arguments.submission
    else:
        submission_id = database.submissions.get_random_submission(arguments.subreddit)

    if arguments.max_length:
        comment_max_length = int(arguments.max_length)

    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit
    save_path = file.get_save_path(os.path.join('media', 'reddit'), submission_id)
    comment_count = int(arguments.comments)
    strong = arguments.strong
    tts_texts = []
    comments = []

    if arguments.title and arguments.body:
        tts_texts.append(f'{submission.title}\n{submission.selftext}')
    elif arguments.title:
        tts_texts.append(submission.title)
    elif arguments.body:
        tts_texts.append(submission.selftext)

    if comment_count != 0 or comment_count != -1:
        comment_ids = database.comments.get_comments(submission.id, comment_max_length, comment_count, strong)

        for comment_id in comment_ids:
            comment = config.REDDIT_CLIENT.comment(comment_id)
            tts_texts.append(comment.body)
            comments.append(comment)
    else:
        comments = False

    text_to_speech.run(tts_texts, save_path, text_to_speech.config_engine(150))
    image_generator.run(submission, save_path, title=arguments.title, body=arguments.body, comments=comments)
    print(arguments)

if __name__ == '__main__':
    main()

# subreddit = 'askreddit'
# submission_id = database.submissions.get_random_submission()
# save_path = file.get_save_path(os.path.join('media', 'reddit'), submission_id)