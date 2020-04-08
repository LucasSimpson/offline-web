import re


def format_url(url, domain, current_url=None):
    # if weird continuation, trivial
    if current_url and len(url) > 0 and url[0] == '_':
        return current_url + '/' + url

    # remove protocol, don't need it
    match = re.match(r'(https?://)', url)
    if match:
        url = url[match.end():]

    # add in domain if relative url
    if len(url) > 0 and url[0] == '/':
        url = domain + url

    # remove trailing slash
    if len(url) > 0 and url[-1] == '/':
        url = url[:-1]

    return url


def is_mime_html(mime):
    return 'text/html' in mime.lower()


if __name__ == '__main__':
    def test(got, want):
        if got != want:
            print(f'Got {got}\n\tExpected {want}')

    test(format_url('http://domain.com/wurd', 'domain.com'), 'domain.com/wurd')
    test(format_url('http://domain.com/whateverman/likesurelkj^&*', 'domain.com'), 'domain.com/whateverman/likesurelkj^&*')
    test(format_url('https://domain.com/wurd', 'domain.com'), 'domain.com/wurd')
    test(format_url('https://domain.com/https://domain.com/wurd', 'domain.com'), 'domain.com/https://domain.com/wurd')
    test(format_url('domain.com/wurd', 'domain.com'), 'domain.com/wurd')
    test(format_url('/wurd/', 'domain.com'), 'domain.com/wurd')

    test(format_url('http://notmydomain.com/wuuurd', 'domain.com'), 'notmydomain.com/wuuurd')
    test(format_url('https://notmydomain.com/wuuurd', 'domain.com'), 'notmydomain.com/wuuurd')

    test(format_url('https://notmydomain.com/wuuurd/ljasdf/', 'domain.com'), 'notmydomain.com/wuuurd/ljasdf')

    test(format_url('_static/something.css', 'domain.com', 'domain.com/master/en'), 'domain.com/master/en/_static/something.css')
