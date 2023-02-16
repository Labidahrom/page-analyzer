from validators.url import url


def validate_url(site_url):
    return not url(site_url) or len(site_url) > 255
