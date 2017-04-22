#!/usr/bin/python

import socket


def get_subdomains(domain):
    # TODO: Marked as comment temporarily
    # br = mechanize.Browser()
    # br.set_handle_robots(False)
    # hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686)', 'Connection': 'keep-alive'}
    # br.addheaders = [hdr]
    subdomains = []
    # for i in range(1,2):
    #     url = "http://www.google.com/search?q=site:" + domain + "&start=" + str(i*10)
    #     page = br.open(url)
    #     soup = BeautifulSoup(page, "lxml")
    #     for a in soup.select('.r a'):
    #         href = urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0]
    #         if (".com/")  in href:
    #             if not href in subdomains:
    #                 subdomains.append(href)
    #                 print href
    #     time.sleep(2)

    subdomains.append('www.ibm.com')
    return subdomains


def get_ip(domains):
    ips = {}
    for domain in domains:
        # domain = domain.replace("https://","")
        if (domain.endswith(".com")):
            ip = socket.gethostbyname(domain)
            ips[domain] = ip
    return ips


def main(domain, comp):
    domains = get_subdomains(domain)
    return get_ip(domains)
