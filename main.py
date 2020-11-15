import datetime
import json
import os
import urllib.request  # python3 only
# from win32_setctime import setctime  # Uncomment for Windows; python3.5+; mkvirtualenv --> pip install win32-setctime


def load_json_file():
    with open('tweets.json') as json_file:
        json_data = json.load(json_file)
    return json_data


def save_images(json_data):
    """Fetches images from twitter, saves them to images/., then modifies the system timestamp to be tweet upload date.
    If you don't have virtualenv set up or don't want to modify the system file timestamp (your loss!), you can leave
    the commented out parts as they are.
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

        # update creation time to match the upload time of tweet
        datetime_ts = datetime.datetime.strptime(image['dateTime'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Uncomment for Mac
        os.system('SetFile -d "{}" {}'.format(datetime_ts.strftime('%m/%d/%Y %H:%M:%S'), 'images/' + file_name))

        # Uncomment for Windows
        # epoch_s = datetime_ts.timestamp()
        # setctime('images/' + file_name, epoch_s)  # Windows only


if __name__ == "__main__":
    data = load_json_file()
    save_images(data)
