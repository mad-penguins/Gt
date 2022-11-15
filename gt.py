from bs4 import BeautifulSoup


class Gt(object):
    """docstring for Gt"""
    def __init__(self, siteaddress, filename=None):
        self.gt_url = siteaddress
        self.filename = filename

    def getSoupFromFile(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            html_text = f.read()

        soup = BeautifulSoup(html_text, 'lxml')

        return soup

    def getPostsFromSoup(self, soup):
        posts_div_html = soup.find("section", attrs={ "class": "tgme_channel_history"})
        posts_html = posts_div_html.find_all(class_="tgme_widget_message_wrap")

        return posts_html

    def parsePost(self, post_html):
        d = {}

        d['head'] = {}
        d['body'] = {}

        _copy = post_html.find("div", class_='tgme_widget_message_forwarded_from')
        if _copy is None:
            d['head']["copy"] = False
        else:
            d['head']["copy"] = True

        _author = post_html.find("a", class_="tgme_widget_message_owner_name").text
        d['head']['author'] = _author

        _id = post_html.find("div", class_="tgme_widget_message").get("data-post")
        d['id'] = _id

        _date = post_html.find("time", class_="time").get('datetime')
        d['head']['date'] = _date

        d['head']['link'] = self.gt_url + _id

        _text = post_html.find("div", class_='tgme_widget_message_text')
        if _text is not None:
            d['body']['text'] = _text.text

        if _copy is not None:
            d['head']['orig_head'] = {}

            _orig_author = post_html.find("a", class_='tgme_widget_message_forwarded_from_name').text
            d['head']['orig_head']['author'] = _orig_author

            _orig_link = post_html.find("a", class_='tgme_widget_message_forwarded_from_name').get("href")
            d['head']['orig_head']['link'] = _orig_link

        return d

    def processFile(self):
        if self.filename is None:
            return

        soup = self.getSoupFromFile()

        response = []

        for post in self.getPostsFromSoup(soup):
            post_data = self.parsePost(post)
            response.append(post_data)

        return response

    def process(self, html_text):
        soup = BeautifulSoup(html_text, 'lxml')
        del html_text

        response = []

        for post in self.getPostsFromSoup(soup):
            post_data = self.parsePost(post)
            response.append(post_data)

        return response
        
