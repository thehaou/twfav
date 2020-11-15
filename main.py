import datetime
import json
import os
import urllib.request  # python3 only
# from win32_setctime import setctime  # Uncomment for Windows; python3.5+; mkvirtualenv --> pip install win32-setctime


def load_json_file():
    """
    Expects a file named tweets.json which is produced by running tweet_snippet.js on your browser.
    Please save that file to twfav's top level directory (same level as this file).
    :return:
    """
    with open('tweets.json') as json_file:
        json_data = json.load(json_file)
    return json_data


def save_images(json_data):
    """Fetches images from twitter, saves them to images/., then modifies the system timestamp to be tweet upload date.
    The format of the image saved is twitter_<account handle>_<status ID>_<batch number>
    * account_handle: what comes after @
    * status ID: tweet identifier
    * batch number: if the tweet has multiple images posted, batch_number corresponds to the individual images.
        By default batch number is 0 for tweets with only one image.

    Put all together, this matches the twitter URL format of https://twitter.com/<account handle>/status/<status ID>

    Example:
        twitter_dodonpahchi_1011217603698704384_0
    becomes
        https://twitter.com/dodonpahchi/status/1011217603698704384

    This way you can easily reconstruct a direct link to the tweet based on the filename alone.

    If you don't have virtualenv set up or don't want to modify the system file timestamp (your loss!), you can leave
    the commented out parts as they are. Otherwise the tweet images will be written to your file system according to
    their original upload date, which is kind of neat to see!

    :param json_data: JSON blob produced by running tweet_snippet.js in your browser
    :return:
    """
    print('processing ' + str(len(json_data)) + ' files (however, there may be duplicates, so the real # may be less)')
    # json_data = json_data[:4]  # uncomment for testing
    for image in json_data:
        # determine file type
        file_type = image['imageURL'].split("=")[1].split("&")[0]

        # fetch and save image
        file_name = 'twitter_' + image['fileName'] + '.' + file_type
        urllib.request.urlretrieve(image['imageURL'], 'images/' + file_name)

        # update file creation time to match the upload time of tweet
        datetime_ts = datetime.datetime.strptime(image['dateTime'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Uncomment for Mac
        # os.system('SetFile -d "{}" {}'.format(datetime_ts.strftime('%m/%d/%Y %H:%M:%S'), 'images/' + file_name))

        # Uncomment for Windows
        # epoch_s = datetime_ts.timestamp()
        # setctime('images/' + file_name, epoch_s)  # Windows only


if __name__ == "__main__":
    data = load_json_file()
    save_images(data)
