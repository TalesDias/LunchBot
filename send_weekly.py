from scraper import get_weekly_menu
from whatsapp import send_message


def format_message(menus: dict) -> str:

    days_str = ["Menu da Semana 🍽\n\n"]

    for week_name, day in menus.items():
        has_lunch = "Prato Principal" in day["Almoço"]["Vegano"]
        has_dinner = "Prato Principal" in day["Jantar"]["Vegano"]
        week_name = week_name.capitalize()

        if has_dinner and has_lunch:
            day_str = f"""{week_name}
☀️ Almoço: {day["Almoço"]["Vegano"]["Prato Principal"]} | {
                day["Almoço"]["Normal"]["Prato Principal"]
            }
🌙 Jantar: {day["Jantar"]["Vegano"]["Prato Principal"]} | {
                day["Jantar"]["Normal"]["Prato Principal"]
            }\n
"""

        elif has_dinner and not has_lunch:
            day_str = f"""{week_name}
☀️ Almoço: Essa refeição não está presente
🌙 Jantar: {day["Jantar"]["Vegano"]["Prato Principal"]} | {
                day["Jantar"]["Normal"]["Prato Principal"]
            }\n
"""

        elif has_lunch and not has_dinner:
            day_str = f"""{week_name}
☀️ Almoço: {day["Almoço"]["Vegano"]["Prato Principal"]} | {
                day["Almoço"]["Normal"]["Prato Principal"]
            }
🌙 Jantar: Essa refeição não está presente\n
"""

        else:
            day_str = f"{week_name}\nNenhuma refeição presente neste dia"

        days_str.append(day_str)

    return "".join(days_str)


if __name__ == "__main__":
    print("Trying to fetch weekly menu.....")
    menus = get_weekly_menu()
    print(f"Menu fetched! Days found: {len(menus)}\n")

    print("Formatting message.....")
    message = format_message(menus)
    print(f"Message generated! Result: {message}\n")

    print("Sending message to WhatsApp.....")
    res = send_message(message)
    if not res:
        raise RuntimeError("Failed to send WhatsApp message!!!")
    print("Message sent!\n")
    print("Until next week :P\n")
