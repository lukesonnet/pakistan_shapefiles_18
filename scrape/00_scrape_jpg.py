import requests
from bs4 import BeautifulSoup
import time
import os

def find_jpgs(html_file):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp)
    links = soup.find_all("a")
    jpg_links = []
    for l in links:
        href = l.get("href")
        if href[-4:].lower() == ".jpg" or href[-5:].lower() == ".jpeg":
            if "ecp.gov.pk" in href:
                jpg_links.append(href)
            else:
                jpg_links.append("https://www.ecp.gov.pk" + href)
    return jpg_links

def download_jpg(link, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    res = requests.get(link)
    fname = folder + os.path.basename(link)
    if res.status_code == 200:
        with open(fname, 'wb') as f:
            f.write(res.content)
        return None
    else:
        return link
        

def main(source, outf):
    links = find_jpgs(source)
    failed_dlds = []
    print(".")
    print(source)
    print(len(links))
    for i, link in enumerate(links):
        if i % 10 == 0:
            print(i)
        out = download_jpg(link, outf)
        if out is not None:
            failed_dlds.append(out)

    print(failed_dlds)
    if len(failed_dlds) > 1:
        with open(source + "_failed", "w") as f:
            f.writelines(failed_dlds)
    elif len(failed_dlds):
        with open(source + "_failed", "w") as f:
            f.writelines(failed_dlds)
    

main("html/kp.html", "jpg/kp/")
main("html/fata.html", "jpg/fata/")
main("html/punjab.html", "jpg/punjab/")
main("html/balochistan.html", "jpg/balochistan/")
main("html/sindh.html", "jpg/sindh/")
main("html/islamabad.htm", "jpg/islamabad/")

# One link is wrong
download_jpg("https://www.ecp.gov.pk/Documents/delimitation2018/22-6-18/T.T.Singh%20New.jpg", "jpg/punjab/")
