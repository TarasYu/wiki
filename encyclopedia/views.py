from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util
from random import choice
from markdown2 import markdown
from django.core import validators


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'searchform'}), label="Пошук Вікі", validators = [validators.validate_slug])
  

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label="Назва")
    content = forms.CharField(widget=forms.Textarea, label="Зміст")

class EditForm(forms.Form):
    editContent =forms.CharField( widget=forms.Textarea, label="")
    editTitle = forms.CharField(widget=forms.HiddenInput)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


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
         return(request, "encyclopedia/article.html", {
             "form": form
         })
   if util.get_entry(title):
      return render(request, "encyclopedia/article.html", {
        "article": markdown(util.get_entry(title)),
        "form": SearchForm(),
        "title": title
   })
   else:
      return render(request, "encyclopedia/noArticle.html", {
          "title": title,
          "form": SearchForm()
      })
       
        

def new_page(request): 
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            titlePage = form.cleaned_data["title"]
            contentPage = form.cleaned_data["content"].encode('utf-8')
            if titlePage in util.list_entries():
                return render(request, "encyclopedia/save_page.html", {
                    "form": SearchForm(),
                    "title": titlePage
                    })
            else:
                util.save_entry(titlePage, contentPage)
                return HttpResponseRedirect(f"{titlePage}")
            
        else: 
            return(request, "encyclopedia/new_page.html", {
                "form": form
            })
    else:
        q=request.GET.get('q')
        if q:
            return render(request, "encyclopedia/new_page.html", {
            "pageForm": NewPageForm({'title': q, 'content': f'#{q}'}),
            "form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "pageForm": NewPageForm(),
                "form": SearchForm()
            })

def editEntry(request, title):   
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html",
        {
            "title": title,
            "form": SearchForm(),
            "editForm": EditForm({'editContent': content, 'editTitle': title}),
        
        })

def save_edited(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["editTitle"]
            content = form.cleaned_data["editContent"].encode('utf-8')
            util.save_entry(title, content)
            return HttpResponseRedirect(f"{title}")
        else:
            return render(request, "encyclopedia/save_edited", {
                "form": form
            })
            
def random_page(request):
    mylist = util.list_entries()
    random = choice(mylist)
    return HttpResponseRedirect(f"{random}")         
        
