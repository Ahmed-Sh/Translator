from bs4 import BeautifulSoup
import requests
import sys

languages = {
    1: "Arabic",
    2: "German",
    3: "English",
    4: "Spanish",
    5: "French",
    6: "Hebrew",
    7: "Japanese",
    8: "Dutch",
    9: "Polish",
    10: "Portuguese",
    11: "Romanian",
    12: "Russian",
    13: "Turkish"
}


def user_inputs():
    args = sys.argv
    translate_from = args[1]
    translate_to = args[2]
    word = args[3]
    return translate_from, translate_to, word


def translator(from_l, to_l, my_word):
    direction = from_l + "-" + to_l
    url = f'https://context.reverso.net/translation/{direction}/{my_word}'
    headers = {'user-agent': 'my-app/0.0.1'}
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
        exit()
    try :
        translations = [str.strip(span.text) for span in soup.select_one('#no-results').select('.wide-container.message')][:1]
        if "not found in Context" in translations[0]:
            print(f"Sorry, unable to find {my_word}")
            exit()
    except AttributeError:
        pass
    translations = [str.strip(a.text) for a in soup.select_one('#translations-content').select('a')][:1]
    examples = [str.lstrip(a.text) for a in soup.select_one('#examples-content').select('.text')][:2]
    return translations, examples


def translate_print(tr, ex, y):
    h1 = f"\n{y} Translations:"
    words = (i for i in tr)
    h2 = f"\n{y} Examples:"
    examples = (ex[i] + ':' if i % 2 == 0 else (ex[i] + "\n") for i in range(len(ex)))
    return h1, words, h2, examples


def create_file(path, content):
    with open(path, 'a+', encoding="utf-8") as f:
        print(content, file=f, flush=True, end='\n')


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())


def processing(h1, words, h2, examples, z):
    content = list()
    content.append(h1)
    for i in words:
        content.append(i)
    content.append(h2)
    for i in examples:
        content.append(i)
    final = "\n".join(content)
    create_file(f"{z}.txt", final)


def run():
    x, y, z = user_inputs()
    if y == "all":
        lang = [languages[i].lower() for i in languages.keys() if x != languages[i].lower()]
        for i in lang:
            y = i
            tr, ex = translator(x, y, z)
            h1, words, h2, examples = translate_print(tr, ex, y)
            processing(h1, words, h2, examples, z)
    elif y.capitalize() not in languages.values():
        print(f"Sorry, the program doesn't support {y}")
        exit()

    else:
        tr, ex = translator(x, y, z)
        h1, words, h2, examples = translate_print(tr, ex, y)
        processing(h1, words, h2, examples, z)
    read_file(f"{z}.txt")


run()
