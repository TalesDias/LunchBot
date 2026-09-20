from scraper import get_weekly_menu
from whatsapp import send_message


def format_message(menus: dict) -> str:

    days_str = ["Menu da Semana 🍽\n\n"]

    for week_name, day in menus.items():
        lines = [week_name.capitalize()]

        for label, emoji, meal in (("Almoço", "☀️", day["Almoço"]), ("Jantar", "🌙", day["Jantar"])):
            sides = [meal[side].get("Prato Principal") for side in ("Vegano", "Normal")]
            pratos = [p for p in sides if p]
            lines.append(f"{emoji} {label}: " + (" | ".join(pratos) if pratos else "Essa refeição não está presente"))

        days_str.append("\n".join(lines) + "\n\n")

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
