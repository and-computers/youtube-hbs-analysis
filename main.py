# -*- coding: utf-8 -*-
import configparser
import logging
import os
import re

import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
# some provided subclasses, each outputs a different string format.
from youtube_transcript_api.formatters import TextFormatter


logger_name_file_name = "youtube-transcripts"
logger = logging.getLogger(logger_name_file_name)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_fh = logging.FileHandler(f"{logger_name_file_name}.log")
log_fh.setFormatter(formatter)
log_fh.setLevel(logging.DEBUG)
logger.addHandler(log_fh)
log_sh = logging.StreamHandler()
log_sh.setLevel(logging.INFO)
logger.addHandler(log_sh)


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TARGET_DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "youtube_data")

cfg = configparser.ConfigParser()
# https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
cfg.optionxform = str
cfg.read('.keys')

CONFIG_PARAMS = {}
for config_tuple in cfg.items('configuration'):
    name = config_tuple[0]
    val = config_tuple[1]
    CONFIG_PARAMS[name] = val

sb_api_key = CONFIG_PARAMS["SCRAPING_BEE_API_KEY"]
channel_url = CONFIG_PARAMS["CHANNEL_URL"]

# https://www.scrapingbee.com/blog/python-requests-proxy/
proxies = {
        "http": f"http://{sb_api_key}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8886",
        "https": f"https://{sb_api_key}:render_js=False&premium_proxy=True@proxy.scrapingbee.com:8887"
    }
# https://github.com/jdepoix/youtube-transcript-api/pull/362
# the above wont work because you need to pass verify=False into the request
# which the api doesnt expose or not even kwargs.. so have to fork to use proxies
FORMATTER = TextFormatter()
if not os.path.exists(TARGET_DATA_DIRECTORY):
    os.makedirs(TARGET_DATA_DIRECTORY)

def write_file_to_target(txt, filename):
    """
    Write text to file in the target directory
    """

    if not txt:
        logger.warning(f"No text found for {filename}. Skipping.")
        return
    fullpath = os.path.join(TARGET_DATA_DIRECTORY, filename)
    try:
        with open(fullpath, "x") as f:
            f.write(txt)
    except FileExistsError:
        logger.info(f"File {filename} already exists. Skipping")


def get_transcripts_from_youtube():
    """
    
    from youtube_transcript_api import YouTubeTranscriptApi  
    YouTubeTranscriptApi.get_transcript(
        video_id, 
        proxies={"https": "https://user:pass@domain:port"}
    )
    """
    videos = scrapetube.get_channel(
        channel_url=channel_url,
        # proxies=proxies,
        # verify=False,
    )
    for video in videos:
        video_id = video['videoId']
        human_readable_id = video_id
        transcript_filename = f"{video_id}-transcript.txt"

        try:
            video_title = video['title']['runs'][0]['text']
            human_readable_id = f"{video_title} - {human_readable_id}"
        except (KeyError, IndexError):
            logger.warning(f"No title found for video.")

        if os.path.exists(os.path.join(TARGET_DATA_DIRECTORY, transcript_filename)):
            logger.debug(f"Skipping, {human_readable_id} already have file.")
            continue

        logger.info(f"Processing {human_readable_id}.")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id=video_id,
                languages=["en", "en-US"],
                # proxies=proxies,
                # verify=False
            )
        except Exception as e:
            logger.warning(f"Exception while trying to process {human_readable_id}.\n{e}")
            continue
        
        if not transcript:
            logger.warning(
                f"Was unable to find transcript for video id: {human_readable_id}"
            )
            continue

        transcript_formatted = FORMATTER.format_transcript(transcript)
        write_file_to_target(
            txt=transcript_formatted,
            filename=transcript_filename,
        )

def analyze_transcripts():
    look4new = False
    if look4new:
        get_transcripts_from_youtube()
    NUM_RECORDS_UNTIL_CHART_CONSIDERED_PROCESSED = 2
    # the order `os.listdir` returns is arbitrary, so sort to keep consistent.
    all_transcript_files = sorted(os.listdir(TARGET_DATA_DIRECTORY))
    num_files = len(all_transcript_files)
    files_with_mentions = 0
    total_mentions = 0
    for transcript_file in all_transcript_files:
        with open(os.path.join(TARGET_DATA_DIRECTORY, transcript_file), "r") as f:
            text = f.read().lower()
            num_mentions_here = len(re.findall(r'\bcase(?:-|(?=\b))', text))
            logger.info(f"{num_mentions_here} mentions in {transcript_file}")
            total_mentions += num_mentions_here
            if num_mentions_here:
                files_with_mentions += 1

    logger.info(f"Total number of video transcripts reviewed: {num_files}")
    logger.info(f"Total case mentions: {total_mentions}")
    logger.info(f"Avg mentions per file: {total_mentions/num_files}")
    logger.info(f"Percent of videos with mention: {(files_with_mentions/num_files)*100}%")

if __name__ == "__main__":
    get_transcripts_from_youtube()
    analyze_transcripts()
