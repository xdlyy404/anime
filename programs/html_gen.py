import random
from programs.db import update_views
from programs.gogo import Anime, GoGoApi
from programs.others import get_atitle, get_genre, get_urls
from programs.anilist import Anilist


def get_genre_html(li):
    x = """<a>{}</a>"""
    html = ''

    for i in li:
        html += x.format(i.strip())

    return html


def get_eps_html(anime, title, data=None):
    try:
        if not data:
            aid = GoGoApi().search(anime, True)[0].strip()
            update_views(aid)
            data = GoGoApi().get_episodes(aid)
        x = """<a class="ep-btn" href="{}">{}</a>"""
        html = ''
        for i in range(1, data+1):
            html += x.format(f'/episode/{aid}/{str(i)}', str(i))
        return html
    except:
        return 'None'


ANIME_POS = """
<a href="{}"><div class="poster la-anime">
                    <div id="shadow1" class="shadow">
                            <div class="dubb">{}</div>
                            <div class="dubb dubb2">{}</div>
                        </div>
                        <div id="shadow2" class="shadow">
                        <img class="lzy_img" src="https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/loading.gif" data-src="{}">
                    </div>
                    <div class="la-details">
                        <h3>{}</h3>
                        <div id="extra">
                        <span>{}</span>
                        <span class="dot"></span>
                        <span>{}</span>                        
                        </div>
                    </div>
                </div></a>
"""

ANIME_POS2 = """
<a href="{}"><div class="poster la-anime">
                    <div id="shadow1" class="shadow">
                            <div class="dubb">{}</div>
                        
                        </div>
                        <div id="shadow2" class="shadow">
                        <img class="lzy_img" src="https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/loading.gif" data-src="{}">
                    </div>
                    <div class="la-details">
                        <h3>{}</h3>
                        <div id="extra">                        
                        <span>{}</span>                        
                        </div>
                    </div>
                </div></a>
"""


def animeRecHtml(data):
    html = ''

    for i in data:
        title = get_atitle(i.get('title'))
        url = get_urls(title)
        x = ANIME_POS.format(
            url,
            str(i.get('rating')).strip()+' / 100',
            'Ep '+str(i.get('episodes')).strip(),
            i.get('image').replace('large', 'medium'),
            title,
            i.get('type'),
            i.get('status')
        )
        html += x

    return html


def get_trending_html():
    data = Anilist.popular()
    html = ''

    for i in data:
        title = get_atitle(i.get('title'))
        url = get_urls(title)
        x = ANIME_POS.format(
            url,
            get_genre(i.get('genres')),
            'Ep '+str(i.get('totalEpisodes')).strip(),
            i.get('image').replace('large', 'medium'),
            title,
            i.get('type'),
            i.get('status')
        )
        html += x

    return html


def get_search_html(data: Anime):
    html = ''

    for i in data:
        if 'dub' in i.url.lower():
            d = 'DUB'
        else:
            d = 'SUB'
        x = ANIME_POS2.format(
            '/anime/'+i.url,
            d,
            i.img,
            i.title,
            i.lang,
        )
        html += x

    return html


def get_recent_html(data):
    html = ''

    for i in data:
        i: Anime

        x = ANIME_POS.format(
            i.url,
            i.lang,
            'Ep '+str(i.episode).strip(),
            i.img,
            i.title,
            f'Latest {i.lang}',
            'HD'
        )
        html += x

    return html


def get_selector_btns(url, current, episodes: list):
    if episodes < 2:
        return '', 0

    selector = ''

    if current == 1:
        x = """<a class="btns" href="usrl"><button
                    class="sbtn inline-flex text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg ">Episode NEXT<i style="margin-left:10px; margin-right: auto;" class="fa fa-arrow-circle-right"></i></button></a>"""

        selector += x.replace('usrl', url +
                              str(current+1)).replace('NEXT', str(current+1))

    elif current == episodes:
        x = """<a class="btns" href="usrl"><button
                    class="sbtn inline-flex text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg "><i
                        class="fa fa-arrow-circle-left"></i>Episode PREV</button></a>"""

        selector += x.replace('usrl', url + str(current-1)).replace(
            'PREV', str(current-1))

    else:
        x = """<a class="btns" href="usrl"><button
                    class="sbtn inline-flex text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg "><i
                        class="fa fa-arrow-circle-left"></i>Episode PREV</button></a>"""

        selector += x.replace('usrl',
                              url + str(current-1)).replace('PREV', str(current-1))

        x = """<a class="btns" href="usrl"><button
                    class="sbtn inline-flex text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg ">Episode NEXT<i style="margin-left:10px; margin-right: auto;" class="fa fa-arrow-circle-right"></i></button></a>"""

        selector += x.replace('usrl',
                              url + str(current+1)).replace('NEXT', str(current+1))
    return selector


SLIDER_HTML = """<div class="mySlides fade">
                <div class="data-slider">
                    <p class="spotlight">{}</p>
                    <h1>{}</h1>
                    <div class="extra1">

                        <span class="year"><i class="fa fa-play-circle"></i>{}</span>
                        <span class="year year2"><i class="fa fa-calendar"></i>{}</span>
                        <span class="cbox cbox1">{}</span>
                        <span class="cbox cbox2">HD</span>
                    </div>
                    <p class="small-synop">{}</p>

                    <div id="watchh">
                        <a href="{}" class="watch-btn">
                            <i class="fa fa-play-circle"></i> Watch Now
                        </a>
                        <a href="{}" class="watch-btn watch-btn2">
                            <i class="fa fa-info-circle"></i> Details<i class="fa fa-angle-right"></i>
                        </a>
                    </div>
                </div>
                <div class="shado">
                    <a href="{}"></a>
                </div>
                <img src="{}">
            </div>"""


def slider_gen():
    data = Anilist.trending()
    random.shuffle(data)
    html = ''
    pos = 1

    for i in data:
        title = get_atitle(i.get('title'))
        url = get_urls(title)
        temp = SLIDER_HTML.format(
            f'#{pos} Spotlight',
            title,
            i.get('type'),
            i.get('status'),
            get_genre(i.get('genres')),
            i.get('description'),
            url.replace(
                '/anime/', '/episode/')+'/1',
            url,
            url,
            i.get('cover')
        )
        html += temp
        pos += 1
    return html


def episodeHtml(episode, title):
    isSub = episode.get('SUB')
    isDub = episode.get('DUB')
    sub = dub = ''
    defa = 0
    s, d = 1, 1

    if isSub:
        for i in isSub:
            if defa == 0:
                defa = f'/embed?url={i}&title={title}'
                sub += f"""<div class="sitem">
                        <a class="sobtn sactive" onclick="selectServer(this)" data-value="/embed?url={i}&title={title}">Server {s}</a>
                    </div>"""
            else:
                sub += f"""<div class="sitem">
                        <a class="sobtn" onclick="selectServer(this)" data-value="/embed?url={i}&title={title}">Server {s}</a>
                    </div>"""
            s += 1

    if isDub:
        for i in isDub:
            if defa == 0:
                defa = f'/embed?url={i}&title={title}'
                dub += f"""<div class="sitem">
                        <a class="sobtn sactive" onclick="selectServer(this)" data-value="/embed?url={i}&title={title}">Server {d}</a>
                    </div>"""
            else:
                dub += f"""<div class="sitem">
                        <a class="sobtn" onclick="selectServer(this)" data-value="/embed?url={i}&title={title}">Server {d}</a>
                    </div>"""
            d += 1

    if sub != '':
        t4 = f"""<div class="server">
                <div class="stitle">
                    <i class="fa fa-closed-captioning"></i>SUB:
                </div>

                <div class="slist">
                    
                    {sub}
                </div>
            </div>"""
    else:
        t4 = ''

    if dub != '':
        t5 = f"""
        <div class="server sd">
                <div class="stitle">
                    <i class="fa fa-microphone-alt"></i>DUB:
                </div>

                <div class="slist">
                    {dub}
                    
                </div>
            </div>
        """
    else:
        t5 = ''

    return t4 + t5, defa
