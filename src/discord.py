import urllib.parse, urllib.request, urllib.error, json, time

BASE_URL = 'https://discord.com/api/v9/'

MESSAGE_TYPE_DEFAULT = 0
MESSAGE_TYPE_REPLY = 19

def get(token, relative_url):
    absolute_url = urllib.parse.urljoin(BASE_URL, relative_url)
    request = urllib.request.Request(absolute_url)
    request.add_header('Authorization', token)
    request.add_header('User-Agent', '')
    try:
        response = urllib.request.urlopen(request)
        return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 429:
            delay = float(json.load(error)['retry_after'])
            time.sleep(delay)
            return get(token, relative_url)
        else:
            raise error

def get_messages(token, channel, after=None):
    url_parts = list(urllib.parse.urlparse('channels/%s/messages' % channel))
    latest_message_id = after or 0
    while True:
        url_parts[4] = urllib.parse.urlencode({
            'after': latest_message_id,
            'limit': 100
        })
        url = urllib.parse.urlunparse(url_parts)
        messages = get(token, url)
        if len(messages) == 0:
            break
        for message in reversed(messages):
            yield message
        latest_message_id = messages[0]['id']

def get_guild(token, guild):
    url = 'guilds/%s' % guild
    return get(token, url)

def get_channel(token, channel):
    url = 'channels/%s' % channel
    return get(token, url)

def get_member(token, user, guild):
    url = 'guilds/%s/members/%s' % (guild, user)
    return get(token, url)

def get_user(token, user):
    url = 'users/%s' % user
    return get(token, url)

