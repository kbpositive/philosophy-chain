import requests
import time
from collections import defaultdict
from functools import reduce


class Philosophy_Tree:
    def __init__(self):
        self.memo = defaultdict(list)

    def children(self, request):
        return [
            link[6:].split()[0][:-1] for link in filter(wiki_link, get_titles(request))
        ]

    def chain(self, query):
        if query in self.memo:
            return self.reduce_print(query)
        words = [f"{query} -> "]
        last = query
        cur = self.children(requests.get(f"https://en.wikipedia.org/wiki/{query}"))[:1]
        if not cur:
            return
        else:
            cur = cur[0]
        print(cur)
        if cur in self.memo:
            self.memo[last].extend([cur, self.memo[cur]])
            return self.reduce_print(cur)
        self.memo[last].extend([cur, self.memo[cur]])
        last = cur
        time.sleep(0.5)
        while cur.lower() != "philosophy":
            words.append(f"{cur} -> ")
            cur = self.children(requests.get(f"https://en.wikipedia.org/wiki/{cur}"))[
                :1
            ]
            if not cur:
                return
            else:
                cur = cur[0]
            print(cur)
            if cur in self.memo:
                self.memo[last].extend([cur, self.memo[cur]])
                return self.reduce_print(cur)
            self.memo[last].extend([cur, self.memo[cur]])
            last = cur
            time.sleep(0.5)
        words.append(cur)
        return "".join(words)

    def reduce_print(self, query):
        if not self.memo[query]:
            return
        print(self.memo[query][0])
        cur = self.memo[query][1]
        while cur:
            print(cur[0])
            cur = cur[1]


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


if __name__ == "__main__":
    pt = Philosophy_Tree()
    while True:
        pt.chain(input())
        print()
# TODO: add cycle detection for examples like chain("s'more")
