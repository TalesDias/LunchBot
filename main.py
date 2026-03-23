from lang_proc import get_formatted_menu
from scraper import get_todays_menu
from whatsapp import send_message


def count_meals(menu: dict) -> int:
    count = 0

    if len(menu["Almoço"]["Vegano"]):
        count += 1

    if len(menu["Jantar"]["Vegano"]):
        count += 1

    return count


if __name__ == "__main__":
    print("Trying to fetch todays menu.....")
    menu = get_todays_menu()
    print(f"Menu fetched! Meals found: {count_meals(menu)}\n")

    print("Generating fancy message.....")
    message, question = get_formatted_menu(menu)
    print(f"The question asked was:\n{question}\n")
    print(f"Message generated! Take a look:\n{message}\n")

    print("Sending message to WhatsApp.....")
    res = send_message(message)
    if not res:
        raise RuntimeError("Failed to send WhatsApp message!!!")
    print("Message sent!\n")
    print("Until tomorrow :D\n")
