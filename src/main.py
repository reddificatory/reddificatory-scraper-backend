import os
import config
import file
import text_to_speech
import database.submissions
import database.comments
import argument_parser
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

def main():
    arguments = argument_parser.argument_parser.parse_args()
    submission_id = None
    comment_max_length = None
    scapred_submissions_count = database.submissions.get_submission_count('scraped', True)
    tts_texts = []
    comments = []

    if scapred_submissions_count == 0:
        if arguments.auto_scrape:
            if arguments.submission_id:
                scraper.scrape_submission(arguments.submission_id, arguments.strong, arguments.limit_comments)
            elif arguments.subreddit:
                scraper.scrape_subreddit(arguments.subreddit, arguments.strong, arguments.limit_submissions, arguments.limit_comments)
        else:
            logger.logger.error('No scraped submissions in database. Please run the scraper.')
            return 1

    if arguments.submission_id:
        submission_id = arguments.submission_id
    else:
        submission_id = database.submissions.get_random_submission(arguments.subreddit)

    if arguments.max_length:
        comment_max_length = arguments.max_length

    submission = config.REDDIT_CLIENT.submission(submission_id)
    save_path = file.get_save_path(os.path.join(os.getcwd(), 'media', 'reddit'), submission_id)

    logging.basicConfig(level=logging.INFO, filename=os.path.join(save_path, '..', 'titles.txt'), filemode='w', fromat='%(message)s')

    if arguments.title and arguments.body:
        tts_texts.append(f'{submission.title}\n{submission.selftext}')
    elif arguments.title:
        tts_texts.append(submission.title)
    elif arguments.body:
        tts_texts.append(submission.selftext)

    if arguments.comments_count != 0 or arguments.comments_count != -1:
        comment_ids = database.comments.get_comments(submission.id, comment_max_length, arguments.comments_count, arguments.strong)

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