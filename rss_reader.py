import feedparser

from config import RSS_FEEDS


def extract_image(entry):
    """
    استخراج عکس از RSS
    """

    # media:content
    media = entry.get("media_content")
    if isinstance(media, list) and media:
        url = media[0].get("url")
        if isinstance(url, str) and url.startswith("http"):
            return url

    # media_thumbnail
    media_thumb = entry.get("media_thumbnail")
    if isinstance(media_thumb, list) and media_thumb:
        url = media_thumb[0].get("url")
        if isinstance(url, str) and url.startswith("http"):
            return url

    # enclosure
    enclosures = entry.get("enclosures")
    if isinstance(enclosures, list) and enclosures:
        url = enclosures[0].get("href")
        if isinstance(url, str) and url.startswith("http"):
            return url

    return None


def get_news():

    all_news = []
    seen_links = set()

    for feed_url in RSS_FEEDS:

        try:

            feed = feedparser.parse(feed_url)

            # اگر هیچ خبری نداشت، برو RSS بعدی
            if not feed.entries:
                continue

            for entry in feed.entries:

                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                if not title or not link:
                    continue

                if link in seen_links:
                    continue

                seen_links.add(link)

                image = extract_image(entry)

                all_news.append({
                    "title": title,
                    "link": link,
                    "image": image, 
                    "source": feed_url
                })

        except Exception as e:

            print(f"❌ خطا در خواندن RSS: {feed_url}")
            print(e)

    return all_news