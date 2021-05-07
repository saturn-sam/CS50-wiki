from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random

from . import util
from .forms import SearchForm, EditForm, CreateWikiForm

markdown_processor = Markdown()

def index(request):
    entries = util.list_entries()
    searched = []
    wiki_item = ''
    if request.method == "POST":
        form_search = SearchForm(request.POST)
        if form_search.is_valid():
            wiki_item = form_search.cleaned_data["page"]
        
            for i in entries:
                if wiki_item in entries:
                    wiki_page = util.get_entry(wiki_item)
                    wiki_page_converted = markdown_processor.convert(wiki_page)
                    
                    context = {
                        'page': wiki_page_converted,
                        'title': wiki_item,
                        'form': SearchForm()
                    }

                    return render(request, "encyclopedia/entry.html", context)

              
                if wiki_item.lower() in i.lower(): 
                    searched.append(i)

            context = {
                'searched': searched, 
                'form': SearchForm(),
                'wiki_item':wiki_item
            }            
            return render(request, "encyclopedia/wiki_search.html", context)

        else:
            return render(request, "encyclopedia/index.html", {"form": form_search})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries, "form":SearchForm()
        })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        wiki_page = util.get_entry(title)
        wiki_page_converted = markdown_processor.convert(wiki_page) 

        context = {
            'page': wiki_page_converted,
            'title': title,
            'form': SearchForm()
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        context ={
            "form":SearchForm(),
            'message': f"Wiki page '{title}' not found."
        }
        return render(request, "encyclopedia/error.html", context)

def edit_wiki(request, title):
    if request.method == 'GET':
        wiki_page = util.get_entry(title)
        if wiki_page:
            context = {
                'form': SearchForm(),
                'edit': EditForm(initial={'content': wiki_page}),
                'title': title
            }

            return render(request, "encyclopedia/edit_wiki.html", context)
        else:
            context ={
                "form":SearchForm(),
                'message':f"Requested '{title}' page was not found."
            }
            return render(request, "encyclopedia/error.html", context)            

    else:
        form = EditForm(request.POST) 
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            wiki_page = util.get_entry(title)
            wiki_page_converted = markdown_processor.convert(wiki_page)

            context = {
                'form': SearchForm(),
                'page': wiki_page_converted,
                'title': title
            }
            return HttpResponseRedirect(reverse('entry', kwargs={'title':title}))

def create_wiki(request):
    if request.method == 'POST':
        form = CreateWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                context = {
                    "form": SearchForm(), 
                    "message": f"Page '{title}' already exist"
                }
                return render(request, "encyclopedia/error.html", context)
            else:
                util.save_entry(title,content)
                wiki_page = util.get_entry(title)
                wiki_page_converted = markdown_processor.convert(wiki_page)

                context = {
                    'form': SearchForm(),
                    'page': wiki_page_converted,
                    'title': title
                }

                return render(request, "encyclopedia/entry.html", context)
    else:
        context = {
            "form": SearchForm(), 
            "new_wiki": CreateWikiForm()
        }
        return render(request, "encyclopedia/create_wiki.html", context)

def random_page(request):
    if request.method == 'GET':
        wiki_entries = util.list_entries()
        random_num = random.randint(0, len(wiki_entries) - 1)        
        random_title = wiki_entries[random_num]
        random_wiki_page = util.get_entry(random_title)
        random_wiki_page_converted = markdown_processor.convert(random_wiki_page)

        context = {
            'form': SearchForm(),
            'page': random_wiki_page_converted,
            'title': random_title
        }

        return render(request, "encyclopedia/entry.html", context)