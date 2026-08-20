import time

from rss_reader import get_news

from storage import (
    load_sent_news,
    save_sent_news,
    load_users
)

from users import update_last_send

from sender import (
    send_message,
    send_photo
)

from utils import (
    add_emoji
)

from category_engine import detect_category_advanced

from ai import translate_news


MAX_SENT_NEWS = 5000

CHECK_INTERVAL = 10


def get_all_channels():

    users = load_users()

    channels = []

    for user_id, user_data in users.items():

        for channel in user_data.get("channels", []):

            if channel.get("status") != "active":
                continue

            channel["user_id"] = user_id

            channel.setdefault("interval", 10)
            channel.setdefault("last_send", 0)
            channel.setdefault("categories", ["همه"])
            channel.setdefault("send_image", True)
            channel.setdefault("show_emoji", True)
            channel.setdefault("footer_text", "")

            channels.append(channel)

    return channels



def build_message(news, channel):

    title = news.get("title", "").strip()

    try:
        title = translate_news(title)
    except Exception:
    	pass


    if channel.get("show_emoji", True):

        try:
            title = add_emoji(title)

        except Exception:
            pass


    message = title


    footer = channel.get(
        "footer_text",
        ""
    ).strip()


    if footer:

        message += f"\n\n{footer}"


    return message



def can_send(channel):

    now = time.time()

    last_send = channel.get(
        "last_send",
        0
    )

    interval = int(
        channel.get(
            "interval",
            10
        )
    ) * 60


    return (
        now - last_send
    ) >= interval



def run():

    print(
        "🚀 AutoNewsBot MultiChannel Started..."
    )


    sent_news = set(
        load_sent_news()
    )


    while True:


        try:


            news_list = get_news()


            channels = get_all_channels()



            if not news_list:

                print(
                    "⚠️ خبری پیدا نشد"
                )

                time.sleep(
                    CHECK_INTERVAL
                )

                continue



            for channel in channels:


                if not can_send(channel):

                    continue



                for latest_news in news_list:


                    link = latest_news.get(
                        "link",
                        ""
                    ).strip()



                    if not link:

                        continue



                    if link in sent_news:

                        continue



                    category = detect_category_advanced(
                        latest_news.get(
                            "title",
                            ""
                        ), 
                        latest_news.get("source", "")
                    )



                    categories = channel.get(
                        "categories",
                        ["همه"]
                    )



                    if (
                        "همه" not in categories
                        and category not in categories
                    ):
                        continue

                    message = build_message(
                        latest_news,
                        channel
                    )

                    image = latest_news.get("image")

                    try:

                        if (
                            channel.get("send_image", True)
                            and image
                        ):

                            result = send_photo(
                                channel["id"],
                                image,
                                message
                            )

                        else:

                            result = send_message(
                                channel["id"],
                                message
                            )

                        if result:

                            sent_news.add(link)

                            update_last_send(
                                channel["user_id"],
                                channel["id"],
                                time.time()
                            )

                            save_sent_news(
                                list(sent_news)[-MAX_SENT_NEWS:]
                            )

                            category_name = ", ".join(
                                channel.get(
                                    "categories",
                                    ["همه"]
                                )
                            )

                            next_send = channel.get(
                                "interval",
                                10
                            )

                            print(
                                f"""
✅ ارسال شد به {channel['id']}
📂 دسته: {category_name}
⏰ ارسال بعدی: {next_send} دقیقه دیگر
"""
                            )

                            break

                    except Exception as e:
                        print("❌ خطا در ارسال:", e)

            time.sleep(
                CHECK_INTERVAL
            )

        except Exception as e:

            print(
                "❌ خطای اصلی:",
                e
            )

            time.sleep(
                CHECK_INTERVAL
            )


if __name__ == "__main__":

    run()