import locale
import os
from datetime import datetime as dt
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

temperature = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=temperature)

with open("prompts/menu_formatter.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        (
            "human",
            """Aqui está o cardápio de hoje:\n\n
            {menu_text}\n\n
            {mirage_instruction}\n\n
            Crie a mensagem para o grupo.""",
        ),
    ]
)


output_parser = StrOutputParser()
chain = prompt | llm | output_parser


def get_formatted_time() -> str:
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    now = dt.now(ZoneInfo("America/Sao_Paulo"))

    return now.strftime("%A - %d de %B")


def format_menu_for_llm(menu: dict) -> str:
    lines = []

    lines.append(get_formatted_time())

    for meal, options in menu.items():
        lines.append(f"{meal}:")
        for diet, dishes in options.items():
            lines.append(f"  {diet}:")
            for category, item in dishes.items():
                lines.append(f"    {category}: {item}")
        lines.append("")

    # Making sure it gets the right day
    lines.append(get_formatted_time())

    return "\n".join(lines)


def get_mirage_line() -> str:
    now = dt.now(ZoneInfo("America/Sao_Paulo"))
    # Mentions the Mirage every first Thursday
    if now.weekday() == 3 and now.day <= 7:
        return """Hoje é dia de mencionar o Mirage! 
                    Inclua uma referência ao Miragem na frase final 🍸"""
    else:
        return "Não mencione o Mirage hoje."


def get_formatted_menu(menu: dict) -> str:
    menu_text = format_menu_for_llm(menu)
    mirage_line = get_mirage_line()

    question = prompt.format_messages(
        menu_text=menu_text, mirage_instruction=mirage_line
    )[1].content

    return chain.invoke(
        {"menu_text": menu_text, "mirage_instruction": mirage_line}
    ), question


if __name__ == "__main__":
    from scraper import get_todays_menu

    menu = get_todays_menu()
    result, question = get_formatted_menu(menu)

    print(question)
    print(result)
