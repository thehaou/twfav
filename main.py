import json
import urllib.request
import datetime
from win32_setctime import setctime


def load_json_file():
    with open('tweets.json') as json_file:
        json_data = json.load(json_file)
    return json_data


def save_images(json_data):
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
        epoch_s = datetime_ts.timestamp()

        setctime('images/' + file_name, epoch_s)


if __name__ == "__main__":
    data = load_json_file()
    save_images(data)
