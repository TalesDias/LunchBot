# LunchBot

## Summary

The LunchBot posts UNICAMP's restaurant menu everyday at around 8AM. The menu is scrapped from the official website, a message is crafted by a GPT model and finally posted to a Whatsapp group using GREEN-API.

*Currently only available for the restaurants at Limeira, but it could be extend it to Campinas if the demand exists.*

## How it works

The code is conceptually divided into four sections, the scrapping, the formatting, the sending and the glue code.

**The scrapping** is done on `scraper.py` it using `Beautiful Soup`, by first finding the lunch and dinner sections, then in each one the normal and the vegetarian options and finally processing the table to read the menu, before returning the whole menu in JSON format.

**The formatting** is done on `lang_proc.py` where first the menu JSON is processed into a single string before being fed to langchain. Langchain then uses the GPT model and the prompt provided at `prompts/menu_formater.md` to generate a custom message, which will be sent to the user.

**The sending** is done on `whatsapp.py` and its quite literaly just using the `requests` library to send an HTTP request with the menu to GREEN-API so it can sent it to the requested group.

**The glue** is present on `main.py` and it basically runs all three above scripts in order, sending the formatted message to the group chat. This is the file that GitHub Actions runs everyday at 8AM, the rules of which are defined in `.github/workflows/post_menu.yml`

## Running locally

```bash
# clone and set up environment
git clone https://github.com/your-username/lunch-bot
cd lunch-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=...
GREEN_API_INSTANCE_ID=...
GREEN_API_TOKEN=...
GREEN_API_GROUP_ID=...
MODEL_TEMPERATURE=0.2
```

```bash
python main.py
```

## Deployment

The bot runs on GitHub Actions with a cron trigger. To run it yourself, set up the same variables from `.env` as repository secrets.

The workflow runs daily at 11:00 UTC (08:00 Brasília).

## Design Choices 

I had two goals when making my choices for this project: Making it actually useful and not spending a penny for it. Based on this, those were my choices:

- **Whatsapp:** Very few students use Telegram or other messaging apps, there was no other option.

- **GREEN-API:** At first, it was obvious that using `selenium` or a similar tool was the way to go, as the official Whatsapp API doesn't offer a free or developer plan, but apparently this violates the TOS, which forced me to search for alternatives. GREEN-API presented itself with a free plan and easy API, which was just enough for this project.

- **Groq:** While trying to use a local `ollama` model, I had some troubles with long iteration times, and as I didn't want to spend weeks developing it, switching to cloud was the obvious choice, and Groq just had the best free plan on my opinion.

- **GitHub Actions:** A good free alternative for the scheduler, plus it's painless to setup if you're already using Github.

## Inspiration

That Whatsapp message with the daily menu is also something I really missed since the last bot was deactivated (RIP Feed Bandeco), this project recreates exactly that. But even though it would be sufficient to just print a formated version of the menu, I wanted to stir things up and add something... different, and when the idea of letting a GPT craft the message crossed my mind, I knew I had to do it because it just sounded very funny.

## What I learned

Apart from mourning the last bot, another big driver to actually make this project was to get something simple to introduce me to LangChain. The main things I've learned are:

- **LCEL chains** — `prompt | llm | output_parser` composition pattern
- **Prompt engineering** — few-shot examples, tone directives, explicit formatting rules
- **Provider abstraction** — swap Ollama for Groq by changing only one line
- **GitHub Actions as a cron runner** — schedule tasks without extra infrastructure