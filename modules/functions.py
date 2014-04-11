from config import app
import datetime


def prettydate(d):
    diff = datetime.datetime.now() - d
    s = diff.seconds

    if diff.days > 365 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days > 180:
        return '{} months ago'.format(diff.days / 30)
    elif diff.days > 14:
        return '{} weeks ago'.format(diff.days / 7)
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s / 60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s / 3600)


app.jinja_env.filters['prettydate'] = prettydate
