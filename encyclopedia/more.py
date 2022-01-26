import re
from encyclopedia.views import SearchForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util
from random import choice
from markdown2 import markdown





   def article(request, title):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search"]
            if title in util.list_entries():
                return render(request, "encyclopedia/article.html", {
                    "article": markdown(util.get_entry(title)),
                    "form": SearchForm(),
                    "title": title
                })
            elif util.search_match(title):
                return render(request, "encyclopedia/search_art.html", {
                    "search": util.search_match(title),
                    "form": SearchForm()
                })
            else:
                return render(request, "encyclopedia/noArticle.html", {
                    "title": title,
                    "form": SearchForm()
                })
        else:
            return render(request, "encyclopedia/article", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/article.html", {
            "article": util.get_entry(title),
            "form": SearchForm(),
            "title": title
        })
