from whatsapp import send_message

if __name__ == "__main__":
    print("Sending failure message")
    res = send_message(
        "⚠️⚠️⚠️ A LunchBot action has failed ⚠️⚠️⚠️\n Check GitHub Actions for details"
    )

    if not res:
        raise RuntimeError("Failed to send WhatsApp message!!!")
    else:
        print("Message sent!\n")
