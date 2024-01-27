

def get_hashtags(tweet: str):
    return set(i.strip('#').lower() for i in tweet.split() if i.startswith('#'))


def get_mentions(tweet: str):
    return set(i.strip('@') for i in tweet.split() if i.startswith('@'))
