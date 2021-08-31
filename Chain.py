import requests
import time


def children(request):
    titles = [
        paragraph
        for paragraph in (
            request.text.split("<h2>")[0]
            .split('"mw-toc-heading"')[0]
            .split("</table>")[-1]
            .split("</cite>")[-1]
        ).split("<p")
        if paragraph[0] == ">"
    ][0]
    return [
        link[6:].split()[0][:-1]
        for link in titles.split('<a href="')
        if link[:6] == "/wiki/"
        and link[6:].split()[0][:-1] != "Wikipedia:Citation_needed"
        and link[6:].split()[0][:-1][:4] != "Help"
    ]


query = "Emotion"
print(query)
cur = children(requests.get(f"https://en.wikipedia.org/wiki/{query}"))[0]
time.sleep(0.5)
while cur.lower() != "philosophy":
    print(cur)
    cur = children(requests.get(f"https://en.wikipedia.org/wiki/{cur}"))[0]
    time.sleep(0.5)
print(cur)

""" output:

Emotion
Mental_state
Mind
Thought
Ideas
Philosophy """