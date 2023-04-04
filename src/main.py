import os
import config
import file
import text_processor
import text_to_speech
import database.submissions
import database.comments
import argparse
import image_generator

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
    tts_texts = []
    comments = []

    if arguments.title and arguments.body:
        tts_texts.append(f'{submission.title}\n{submission.selftext}')
    elif arguments.title:
        tts_texts.append(submission.title)
    elif arguments.body:
        tts_texts.append(submission.selftext)

    # TODO: implement getting every comment
    # TODO: implement comment length
    # TODO: implement bot comment filtering
    # TODO: rewrite database queries to suite the new options
    # TODO: rewrite getting exactly as many comments as specified in the option
    if comment_count != 0 or comment_count != -1:
        comment_ids = database.comments.get_random_comments(submission_id, comment_count)
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