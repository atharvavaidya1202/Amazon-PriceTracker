from bs4 import BeautifulSoup
from requests import get
import lxml
import re

def get_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # --- Product Name ---
    name_elem = soup.select_one("#productTitle")
    name = name_elem.get_text(strip=True) if name_elem else "N/A"

    # --- Rating (Stars) ---
    rate_elem = soup.select_one("i.a-icon-star span.a-icon-alt")
    if rate_elem:
        text = rate_elem.get_text(strip=True)
        match = re.search(r"\d+(\.\d+)?", text)  # grab first numeric pattern
        rate = float(match.group()) if match else 0.0
    else:
        rate = 0.0

    # --- Number of Ratings (Reviews) ---
    rating_elem = soup.select_one("#acrCustomerReviewText")
    if rating_elem:
        num_str = re.sub(r"[^\d]", "", rating_elem.get_text(strip=True))  # remove commas/words
        rating = int(num_str) if num_str.isdigit() else 0
    else:
        rating = 0

    # --- Price ---
    price_selectors = [
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#priceblock_saleprice",
        "span.a-price span.a-offscreen"
    ]

    price = None
    for selector in price_selectors:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(strip=True)
            match = re.search(r"\d+[\d,]*\.?\d*", text)
            if match:
                price = float(match.group().replace(",", ""))
                break
    if price is None:
        price = 0.0

    # --- Product Image ---
    img_elem = soup.find("img", id="landingImage")
    image = img_elem["src"] if img_elem and "src" in img_elem.attrs else "N/A"

    return (name, price, rate, rating, image)


if __name__ == "__main__":
    url = "https://www.amazon.in/OnePlus-13R-Smarter-Lifetime-Warranty/dp/B0DPS62DYH"
    print(get_product_info(url))
