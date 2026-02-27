from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)


prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that formats university restaurant menus for a WhatsApp message.

        STRICT FORMATTING RULES:
        - Do NOT use markdown. No **, no ##, no -, no *.
        - Use WhatsApp native formatting only: *bold* for section headers, _italic_ if needed.
        - Use emojis to make it visually scannable.
        - Keep it concise. Students read this on their phones.
        - If there is no menu for a meal, say so clearly.

        OUTPUT EXAMPLE:
        🍽️ *Today's Menu — Monday, Jan 13*

        ☀️ *Lunch*
        Normal: Rice, beans, grilled chicken, salad
        Vegan: Rice, beans, grilled tofu, salad

        🌙 *Dinner*
        Normal: Pasta, tomato sauce, meatballs
        Vegan: Pasta, tomato sauce, mushrooms"""),
            ("human", "Here is today's raw menu data:\n\n{menu_text}\n\nFormat it following the rules above.")
])
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

if __name__ == "__main__":
    mock_menu = """
    Lunch - Normal: Rice, beans, grilled chicken, salad, orange juice
    Lunch - Vegan: Rice, beans, grilled tofu, salad, orange juice
    Dinner - Normal: Pasta, tomato sauce, meatballs, salad
    Dinner - Vegan: Pasta, tomato sauce, mushrooms, salad
    """

    result = chain.invoke({"menu_text": mock_menu})
    print(result)
