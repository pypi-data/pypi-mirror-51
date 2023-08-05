import textwrap
from collections import namedtuple
from operator import attrgetter
import calendar
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate

import click
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import BaseHeuristic
from halo import Halo
from selectolax.parser import HTMLParser
from tabulate import tabulate
import github3

NEXT_BUTTON_SELECTOR = "#dependents > div.paginate-container > div > a"
ITEM_SELECTOR = "#dependents > div.Box > div.flex-items-center"
REPO_SELECTOR = "span > a.text-bold"
STARS_SELECTOR = "div > span:nth-child(1)"
GITHUB_URL = "https://github.com"


class OneDayHeuristic(BaseHeuristic):

    def update_headers(self, response):
        date = parsedate(response.headers["date"])
        expires = datetime(*date[:6]) + timedelta(days=1)
        return {"expires": formatdate(calendar.timegm(expires.timetuple())), "cache-control": "public"}

    def warning(self, response):
        msg = "Automatically cached! Response is Stale."
        return '110 - "%s"' % msg


def already_added(repo_url, repos):
    for repo in repos:
        if repo.url == repo_url:
            return True


@click.command()
@click.argument("url")
@click.option('--repositories/--packages', default=True, help="Sort repositories or packages (default repositories)")
@click.option('--description', is_flag=True, help="Show description of packages or repositories (performs additional request per repository)")
@click.option("--show", default=10, help="Number of showing repositories (default=10)")
@click.option("--more-than", default=5, help="Minimum number of stars (default=5)")
@click.option("--token", envvar="GHTOPDEP_TOKEN")
def cli(url, repositories, show, more_than, description, token):
    if description and token:
        gh = github3.login(token=token)
        CacheControl(gh.session, cache=FileCache(".ghtopdep_cache"), heuristic=OneDayHeuristic())
        Repo = namedtuple("Repo", ["url", "stars", "description"])
    elif description and not token:
        print("Please provide token")
    else:
        Repo = namedtuple("Repo", ["url", "stars"])

    def fetch_description(relative_url):
        _, owner, repository = relative_url.split("/")
        repository = gh.repository(owner, repository)
        repo_description = " "
        if repository.description:
            repo_description = textwrap.shorten(repository.description, width=60, placeholder="...")
        return repo_description

    destination = "repository"
    destinations = "repositories"
    if not repositories:
        destination = "package"
        destinations = "packages"
    page_url = "{}/network/dependents?dependent_type={}".format(url, destination.upper())

    repos = []
    more_than_zero = 0
    repo_count = 0
    spinner = Halo(text="Fetching information about {}".format(destinations), spinner="dots")
    spinner.start()
    sess = requests.session()
    cached_sess = CacheControl(sess, cache=FileCache(".ghtopdep_cache"), heuristic=OneDayHeuristic())
    while True:
        r = cached_sess.get(page_url)
        parsed_node = HTMLParser(r.text)
        dependents = parsed_node.css(ITEM_SELECTOR)
        repo_count += len(dependents)
        for i in dependents:
            repo_stars_list = i.css(STARS_SELECTOR)
            # only for ghost or private? packages
            if repo_stars_list:
                repo_stars = i.css(STARS_SELECTOR)[0].text().strip()
                repo_stars_num = int(repo_stars.replace(",", ""))
            else:
                continue

            if repo_stars_num != 0:
                more_than_zero += 1
            if repo_stars_num >= more_than:
                relative_repo_url = i.css(REPO_SELECTOR)[0].attributes["href"]
                repo_url = "{}{}".format(GITHUB_URL, relative_repo_url)

                # can be listed same package
                is_already_added = already_added(repo_url, repos)
                if not is_already_added and repo_url != url:
                    if description:
                        repo_description = fetch_description(relative_repo_url)
                        repos.append(Repo(repo_url, repo_stars_num, repo_description))
                    else:
                        repos.append(Repo(repo_url, repo_stars_num))

        node = parsed_node.css(NEXT_BUTTON_SELECTOR)
        if len(node) == 2:
            page_url = node[1].attributes["href"]
        elif len(node) == 0 or node[0].text() == "Previous":
            spinner.stop()
            break
        elif node[0].text() == "Next":
            page_url = node[0].attributes["href"]

    sorted_repos = sorted(repos[:show], key=attrgetter("stars"), reverse=True)
    if sorted_repos:
        if description:
            print(tabulate(sorted_repos, headers=["URL", "Stars", "Description"], tablefmt="grid"))
        else:
            print(tabulate(sorted_repos, headers=["URL", "Stars"], tablefmt="grid"))
        print("found {} {} others {} is private".format(repo_count, destinations, destinations))
        print("found {} {} with more than zero star".format(more_than_zero, destinations))
    else:
        print("Doesn't find any {} that math search request".format(destination))
