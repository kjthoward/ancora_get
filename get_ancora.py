import gzip
import os
import pdb
import re
import shutil

import requests
from bs4 import BeautifulSoup

base_url = "https://ancora.genereg.net/downloads/"
html_page = requests.get(base_url).text
soup = BeautifulSoup(html_page, features="html.parser")
print(f"{'Collecting species list':-^60}")
for link in soup.findAll("a"):
    # pdb.set_trace()
    species_name = link.get("href")

    if species_name.startswith("http") or not species_name.endswith("/"):
        continue

    if species_name != "/":
        species_url = base_url + species_name
        species_html_page = requests.get(species_url).text
        species_soup = BeautifulSoup(species_html_page, features="html.parser")
        print(
            f"{f'Collecting list of {species_name.removesuffix("/")} _vs_ files':-^60}"
        )
        for link in species_soup.findAll("a"):
            vs_name = link.get("href")
            if vs_name.startswith("?") or vs_name.startswith("/"):
                continue
            outdir = os.path.join(os.getcwd(), species_name, vs_name)
            os.makedirs(outdir, exist_ok=True)
            vs_url = species_url + "/" + vs_name
            vs_html_page = requests.get(vs_url).text
            vs_soup = BeautifulSoup(vs_html_page, features="html.parser")
            print(
                f"{f'Downloading files for {species_name.removesuffix("/")}_{vs_name.removesuffix("/")}':-^60}"
            )
            for vs_link_name in vs_soup.findAll("a"):
                vs_link = vs_link_name.get("href")
                if (
                    vs_link.endswith(".bed")
                    or vs_link.endswith(".wig")
                    or vs_link.endswith(".bed.gz")
                    or vs_link.endswith(".wig.gz")
                ):
                    print(f"Downloading: {vs_link}")
                    open(os.path.join(outdir, vs_link), "wb").write(
                        requests.get(vs_url + "/" + vs_link).content
                    )
