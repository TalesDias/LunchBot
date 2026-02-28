import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

with open("prompts/menu_formatter.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Aqui está o cardápio de hoje:\n\n{menu_text}\n\nCrie a mensagem para o grupo.")
])

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

def get_formatted_time() -> str:
    import locale 
    from datetime import datetime as dt

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    return dt.now().strftime("%A - %d de %B")

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

def get_formatted_menu(menu: dict) -> str:
    menu_text = format_menu_for_llm(menu)
    return chain.invoke({"menu_text": menu_text})


if __name__ == "__main__":
    from scraper import get_todays_menu
    menu = get_todays_menu()
    result = get_formatted_menu(menu)
    print(result)