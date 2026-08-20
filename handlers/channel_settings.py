# ==========================
# Channel Settings Handler
# Version 1.5.1
# ==========================

from bale import CallbackQuery

from client import bot

from keyboards import (
    channel_settings_menu,
    channel_settings_bottom_menu,
    delete_channel_menu, 
    category_menu, 
    send_time_menu
)

from users import (
    delete_channel,
    toggle_channel_image, 
    toggle_channel_emoji, 
    get_user, 
    update_categories, 
    update_send_time
)

from handlers.channel import show_channels

from states import (
    set_state,
    get_state,
    clear_state
)


@bot.event
async def on_callback(callback: CallbackQuery):

    data = callback.data

    print(data)
    
    
# ==========================
    # انتخاب دسته بندی
    # ==========================

    if data.startswith("cat_select_"):

        category = data.replace(
            "cat_select_",
            "",
            1
        )

        state = get_state(
            callback.from_user.id
        )

        selected = state["data"].get(
            "categories",
            []
        )

        if category == "همه":

            selected = ["همه"]

        else:

            if "همه" in selected:
                selected.remove("همه")

            if category in selected:
                selected.remove(category)
            else:
                selected.append(category)

        state["data"]["categories"] = selected

        set_state(
            callback.from_user.id,
            state["state"],
            state["data"]
        )

        await callback.message.edit(
            "🏷 دسته‌بندی خبر\n\n"
            "دسته‌های موردنظر را انتخاب کنید.\n\n"
            f"✅ انتخاب شده: {', '.join(selected) if selected else 'هیچ‌کدام'}",
            components=category_menu()
        )

        return


  # ==========================
    # باز کردن تنظیمات کانال
    # ==========================

    if data.startswith("channel_"):

        channel_id = data.replace("channel_", "", 1)

        user = get_user(callback.from_user.id)

        send_image = True
        show_emoji = True

        for channel in user["channels"]:

            if channel["id"] == channel_id:

                send_image = channel.get("send_image", True)
                show_emoji = channel.get("show_emoji", True)
                break


        await callback.message.reply(
            f"⚙️ تنظیمات کانال\n\n{channel_id}",
            components=channel_settings_menu(
                channel_id,
                send_image,
                show_emoji
            )
        )


        await callback.message.reply(
            "لیست کانال‌های شما",
            components=channel_settings_bottom_menu()
        )

        return


    # ==========================
    # زمان ارسال
    # ==========================

    if data.startswith("time_"):

        channel_id = data.replace(
            "time_",
            "",
            1
        )

        await callback.message.reply(
            "⏰ تنظیم زمان ارسال اخبار\n\n"
            "لطفاً یکی از زمان‌های زیر را انتخاب کنید.",
            components=send_time_menu(channel_id)
        )

        return

# ==========================
    # ذخیره زمان ارسال
    # ==========================

    if data.startswith("stime_"):

        try:

            parts = data.split("_", 2)

            interval = int(parts[1])

            channel_id = parts[2].strip()


            result = update_send_time(
                callback.from_user.id,
                channel_id,
                interval
            )


            if result:

                user = get_user(
                    callback.from_user.id
                )

                send_image = True
                show_emoji = True


                for channel in user.get(
                    "channels",
                    []
                ):

                    if channel.get("id") == channel_id:

                        send_image = channel.get(
                            "send_image",
                            True
                        )

                        show_emoji = channel.get(
                            "show_emoji",
                            True
                        )

                        break


                await callback.message.reply(
                    f"✅ زمان ارسال کانال {channel_id} روی {interval} دقیقه تنظیم شد."
                )


                await callback.message.edit(
                    f"⚙️ تنظیمات کانال\n\n{channel_id}",
                    components=channel_settings_menu(
                        channel_id,
                        send_image,
                        show_emoji
                    )
                )


            else:

                await callback.message.reply(
                    "❌ خطا در ذخیره زمان ارسال."
                )


        except Exception as e:

            print(
                "❌ خطا در تغییر زمان ارسال:",
                e
            )

            await callback.message.reply(
                "❌ خطا در تغییر زمان ارسال."
            )


        return



# ==========================
    # روشن / خاموش عکس
    # ==========================

    if data.startswith("img_"):

        channel_id = data.replace("img_", "", 1)

        toggle_channel_image(
            callback.from_user.id,
            channel_id
        )

        user = get_user(callback.from_user.id)

        send_image = True
        show_emoji = True

        for channel in user["channels"]:

            if channel["id"] == channel_id:

                send_image = channel.get("send_image", True)
                show_emoji = channel.get("show_emoji", True)
                break

        await callback.message.edit(
            f"⚙️ تنظیمات کانال\n\n{channel_id}",
            components=channel_settings_menu(
                channel_id,
                send_image,
                show_emoji
            )
        )

        return


    # ==========================
    # روشن / خاموش ایموجی
    # ==========================

    if data.startswith("emoji_"):

        channel_id = data.replace("emoji_", "", 1)

        toggle_channel_emoji(
            callback.from_user.id,
            channel_id
        )

        user = get_user(callback.from_user.id)

        send_image = True
        show_emoji = True

        for channel in user["channels"]:

            if channel["id"] == channel_id:

                send_image = channel.get("send_image", True)
                show_emoji = channel.get("show_emoji", True)
                break

        await callback.message.edit(
            f"⚙️ تنظیمات کانال\n\n{channel_id}",
            components=channel_settings_menu(
                channel_id,
                send_image,
                show_emoji
            )
        )

        return
        
        
# ==========================
    # ذخیره دسته بندی
    # ==========================

    if data == "cat_save":

        print("CAT SAVE CLICKED")

        state = get_state(
            callback.from_user.id
        )

        if state["state"] != "category_select":
            return

        channel_id = state["data"]["channel_id"]

        categories = state["data"].get(
            "categories",
            ["همه"]
        )

        result = update_categories(
            callback.from_user.id,
            channel_id,
            categories
        )

        print(result)

        if result:

            await callback.message.reply(
                "✅ دسته‌بندی‌ها با موفقیت ذخیره شدند."
            )

            user = get_user(callback.from_user.id)

            send_image = True
            show_emoji = True

            for channel in user["channels"]:

                if channel["id"] == channel_id:

                    send_image = channel.get(
                        "send_image",
                        True
                    )

                    show_emoji = channel.get(
                        "show_emoji",
                        True
                    )

                    break

            await callback.message.reply(
                f"⚙️ تنظیمات کانال\n\n{channel_id}",
                components=channel_settings_menu(
                    channel_id,
                    send_image,
                    show_emoji
                )
            )

        else:

            await callback.message.reply(
                "❌ خطا در ذخیره دسته‌بندی‌ها."
            )

        clear_state(
            callback.from_user.id
        )

        return

    # ==========================
    # دسته بندی خبر
    # ==========================

    if data.startswith("cat_"):

        channel_id = data.replace(
            "cat_",
            "",
            1
        )

        set_state(
            callback.from_user.id,
            "category_select",
            {
                "channel_id": channel_id,
                "categories": []
            }
        )

        await callback.message.reply(
            "🏷 دسته‌بندی خبر\n\n"
            "دسته‌های موردنظر را انتخاب کنید.",
            components=category_menu()
        )

        return
    

    # ==========================
    # درخواست حذف کانال
    # ==========================

    if data.startswith("delete_"):

        channel_id = data.replace("delete_", "", 1)


        await callback.message.reply(
            "⚠️ آیا مطمئن هستید که می‌خواهید این کانال را حذف کنید؟",
            components=delete_channel_menu(channel_id)
        )

        return



    # ==========================
    # تایید حذف کانال
    # ==========================

    if data.startswith("yesdel_"):

        channel_id = data.replace("yesdel_", "", 1)

        user_id = callback.from_user.id


        result = delete_channel(
            user_id,
            channel_id
        )


        if not result:

            await callback.message.reply(
                "❌ کانال پیدا نشد."
            )


        class FakeMessage:
            pass


        fake_message = FakeMessage()

        fake_message.from_user = callback.from_user
        fake_message.reply = callback.message.reply


        await show_channels(fake_message)

        return



    # ==========================
    # لغو حذف
    # ==========================

    if data.startswith("nodel_"):


        class FakeMessage:
            pass


        fake_message = FakeMessage()

        fake_message.from_user = callback.from_user
        fake_message.reply = callback.message.reply


        await show_channels(fake_message)

        return
        
     