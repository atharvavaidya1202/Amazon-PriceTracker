from bs4 import BeautifulSoup
from requests import get
import lxml

def get_product_info(url):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept-Language" : "en",
    }
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    name = soup.select_one(selector="#productTitle").getText()
    name = name.strip()

    rate = soup.select_one(selector="#acrPopover").getText()
    rate = float(rate.strip().split()[0])

    rating = soup.select_one(selector="#acrCustomerReviewText").getText()
    j = ""
    for i in (rating.strip().split()[0]).split(','):
        j = j+i
    rating = int(j)

    price = soup.select_one(selector="#priceblock_ourprice").getText()
    price = float(price.strip().split()[0][1:])

    image = soup.find("img", id="landingImage")["data-a-dynamic-image"].split('"')[1]

    return (name, price, rate, rating, image)

if __name__ == '__main__':
    url = "https://www.amazon.in/OnePlus-13R-Smarter-Lifetime-Warranty/dp/B0DPS62DYH/ref=pb_allspark_purchase_sims_desktop_d_sccl_4_2/261-2542452-3443229?pd_rd_w=suymz&content-id=amzn1.sym.bf23bdc7-6f20-4210-b1c5-da3acd88edba&pf_rd_p=bf23bdc7-6f20-4210-b1c5-da3acd88edba&pf_rd_r=MTKB60ZAJCEPA4RX030N&pd_rd_wg=PINPi&pd_rd_r=29bbbb49-61d0-4e03-aa8c-418da6abb519&pd_rd_i=B0DPS62DYH&th=1"
    print(get_product_info(url))
