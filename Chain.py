import requests
import time


def wiki_link(link):
    if (
        link[:6] == "/wiki/"
        and link[6:].split()[0][:-1] != "Wikipedia:Citation_needed"
        and link[6:].split()[0][:-1][:4] != "Help"
    ):
        return True
    return False


def get_titles(request):
    return [
        paragraph
        for paragraph in (
            request.text.split("<h2>")[0]
            .split('"mw-toc-heading"')[0]
            .split("</table>")[-1]
            .split("</cite>")[-1]
        ).split("<p")
        if paragraph and paragraph[0] == ">"
    ][0].split('<a href="')


def children(request):
    return [link[6:].split()[0][:-1] for link in filter(wiki_link, get_titles(request))]


def chain(query):
    words = [f"{query} -> "]
    cur = children(requests.get(f"https://en.wikipedia.org/wiki/{query}"))[0]
    time.sleep(0.5)
    print(cur)
    while cur.lower() != "philosophy":
        words.append(f"{cur} -> ")
        cur = children(requests.get(f"https://en.wikipedia.org/wiki/{cur}"))[0]
        time.sleep(0.5)
        print(cur)
    words.append(cur)
    return "".join(words)


if __name__ == "__main__":
    while True:
        chain(input())
# TODO: add cycle detection for examples like chain("s'more")
