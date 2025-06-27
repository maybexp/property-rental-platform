import requests
from bs4 import BeautifulSoup

url = "https://www.dba.dk/boliger/lejebolig/lejelejlighed/lejelejligheder"

def get_listing_details(listing):
    link_tag = listing.select_one("a.listingLink")
    url = link_tag["href"]
    image_src = listing.select_one("img.image-thumbnail")["src"]
    title = link_tag.select_one("span.text").text.strip()
    price = listing.select_one("span.price").text.strip()
    date = listing.select_one("span.date").text.strip()

    return {
        "url": url,
        "image_src": image_src,
        "title": title,
        "price": price,
        "date": date
    }

def get_all_listings():
    all_listings = []

    page = 1
    while len(all_listings) < 100:
        response = requests.get(url, params={"page": page})
        soup = BeautifulSoup(response.text, "html.parser")
        listing_tags = soup.select("tr.dbaListing.listing.hasInsertionFee.topListing")

        if not listing_tags:
            break

        for listing in listing_tags:
            listing_details = get_listing_details(listing)
            all_listings.append(listing_details)

            if len(all_listings) >= 100:
                break

        page += 1

    return all_listings

listings = get_all_listings()
brr = 0
for listing in listings:
    print("Titel:", listing["title"])
    print("Pris:", listing["price"])
    print("Dato:", listing["date"])
    print("Billede:", listing["image_src"])
    print("URL:", listing["url"])
    brr +=1
    print(brr)
    print("-----------------------------------")
