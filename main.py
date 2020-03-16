# coding: utf-8

from workflow import Workflow,web,ICON_WEB
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_recent_movies():
    url = "https://api.douban.com/v2/movie/in_theaters?apikey=0df993c66c0c636e29ecbb5344252a4a&start=0&count=10"
    r = web.get(url)

    # throw an error if request failed, Workflow will catch this and show
    # it to the user
    r.raise_for_status()
    result = r.json()
    return r.json()['subjects']


def main(wf):
    movies = wf.cached_data('movies', get_recent_movies, max_age=300)

    for r in movies:
        wf.add_item(title=u"【{}/10】{}".format(r['rating']['average'], r['title']),
                     subtitle=u"{} 类型:{} ".format(r['year'], "/".join(r['genres'])),
                     arg=r['alt'],
                     valid=True,
                     icon=ICON_WEB)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
