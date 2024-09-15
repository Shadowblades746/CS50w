from random import choice

from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/InvalidEntryPage.html", {
            "title": entry
        })

    return render(request, "encyclopedia/entryPage.html", {
        "title": entry,
        "entryText": markdown(util.get_entry(entry)),
    })


def search(request):
    if request.method == 'POST':
        if util.get_entry(request.POST['q']) is None:
            searchResults = []
            for word in util.list_entries():
                if request.POST.get('q').lower() in word.lower():
                    searchResults.append(word)
            return render(request, "encyclopedia/searchResults.html", {
                "entries": searchResults
            })
        return render(request, "encyclopedia/entryPage.html", {
            "title": request.POST['q'],
            "entryText": markdown(util.get_entry(request.POST['q'])),
        })


def newPage(request):
    if request.method == "POST":
        if util.get_entry(request.POST['q']) is None:
            util.save_entry(request.POST['q'], request.POST["c"])
            return render(request, "encyclopedia/entryPage.html", {
                "title": request.POST['q'],
                "entryText": markdown(util.get_entry(request.POST['q'])),
            })
        return render(request, "encyclopedia/invalidNewPage.html", {
            "title": request.POST['q'],
        })
    return render(request, "encyclopedia/newPage.html", {})


def editPage(request):
    if request.method == "POST":
        util.save_entry(request.POST["title"], request.POST["c"])
        return render(request, "encyclopedia/entryPage.html", {
            "title": request.POST["title"],
            "entryText": markdown(util.get_entry(request.POST["title"])),
        })
    return render(request, "encyclopedia/editPage.html", {
        "title": request.GET['title'],
        "content": util.get_entry(request.GET['title']),
    })


def randomPage(request):
    randomEntry = choice(util.list_entries())
    return render(request, "encyclopedia/entryPage.html", {
        "title": randomEntry,
        "entryText": markdown(util.get_entry(randomEntry)),
    })
