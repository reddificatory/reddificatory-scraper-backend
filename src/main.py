import os
import config
import file
import text_to_speech
import database.submissions
import database.comments
import argparse
import image_generator
import video_generator
import audio
import logger
import logging
import plyer
import scraper

    # TODO: implement -a/--scrape option to run the scraper automatically if the submission is not scraped yet
    # TODO: rewrite database queries to suite the new options
    # TODO: rewrite video creation
        # different tts voices
        # vertical and landscape mode
        # watermark
    # TODO: implement markdown
    # TODO: log titles and paths in a file
    # TODO: implement bot comment filtering

argument_parser = argparse.ArgumentParser()
subreddit_submission_group = argument_parser.add_mutually_exclusive_group(required=True)
subreddit_submission_group.add_argument('-S', '--submission', dest='submission', help='Specify submission.')
subreddit_submission_group.add_argument('-s', '--subreddit', dest='subreddit', help='Specify subreddit.')
argument_parser.add_argument('-t', '--title', action='store_true', dest='title', help='Enable submission title')
argument_parser.add_argument('-b', '--body', action='store_true', dest='body', help='Enable submission body')
argument_parser.add_argument('-l', '--max-length', type=int, dest='max_length', help='Specify max length of comments in characters.')
argument_parser.add_argument('-c', '--comments', type=int, dest='comments', default=3, help='Set number of comments. -1: all comments, 0: no comments, number: number of comments.')
argument_parser.add_argument('-o', '--strong', action='store_true', dest='strong', help='Set only strong option to true')
argument_parser.add_argument('-a', '--auto-scrape', action='store_true', dest='auto_scrape', help='Run scraper automatically if there are no scraped submissions in the database.')
argument_parser.add_argument('-i', '--limit-submissions', dest='limit_submissions', default=25, help='Scraper: limit submission count')
argument_parser.add_argument('-I', '--limit-comments', dest='limit_comments', default=25, help='Scraper: limit comment count')
arguments = argument_parser.parse_args()

def main():
    submission_id = None
    comment_max_length = None

    if arguments.submission:
        submission_id = arguments.submission
    else:
        submission_id = database.submissions.get_random_submission(arguments.subreddit)

    if arguments.max_length:
        comment_max_length = arguments.max_length

    submission = config.REDDIT_CLIENT.submission(submission_id)
    save_path = file.get_save_path(os.path.join(os.getcwd(), 'media', 'reddit'), submission_id)
    comment_count = arguments.comments
    strong = arguments.strong
    tts_texts = []
    comments = []

    logging.basicConfig(level=logging.INFO, filename=os.path.join(save_path, '..', 'titles.txt'), filemode='w', fromat='%(message)s')

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
    audio.merge_audios(save_path)
    image_generator.run(submission, save_path, title=arguments.title, body=arguments.body, comments=comments)
    video_generator.run(save_path)
    database.submissions.update_submission(submission_id, 'used')
    logger.logger.info(f'Video saved to: {save_path}')
    logging.info(f'{submission.title};{save_path}')
    plyer.notification.notify(title='Video generation', message=f'Video saved to {save_path}', app_name='Reddificatory Video Generator')

if __name__ == '__main__':
    main()