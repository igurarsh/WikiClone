from django.shortcuts import render
from django.shortcuts import HttpResponse
from django import forms
from . import util

import random
import markdown

# For Converting Markdown To HTML
md = markdown.Markdown()

# For Search Forms
class NewSearchForm(forms.Form):
    q = forms.CharField(label="search",
    widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

def index(request):
    q = NewSearchForm()

    # Checking if the request sent is POST
    if request.method == "POST":
        form = NewSearchForm(request.POST)

        # Getting all the page enteries
        entries = util.list_entries()

        # searching according to user
        if form.is_valid():
            q = form.cleaned_data["q"]
            serach_result = []
            # case if the user entered ttile is available or is substring of ttile
            for i in entries:
                # if user entered string is in enteries
                if q.lower() == i.lower():
                    return title_pag(request,q) 
                # checking if its at least sub string 
                len_user = len(q)
                len_word = len(i)
                counter = 0
                # running for loop to see the matches
                for x in range(0,len_user):
                    if len_word >= len_user:
                        if q[x].lower() == i[x].lower():
                            counter = counter + 1
                            if counter == len_user:
                                serach_result.append(i)
    
            # checking if our result query has some matches
            if serach_result is not None:
                return render(request, "encyclopedia/index.html", {
                    "entries": serach_result,
                    "form": NewSearchForm()
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

# Converts the markdown file into html page 
def title_pag(request,title):
    if (util.get_entry(title)!= None):
        return render(request,"encyclopedia/title.html",{
            "title":title,"para": md.convert(util.get_entry(title))
        })
    else:
        return render(request,"encyclopedia/title.html",{
            "title":title,"para":title+" Not Found"
        })

# Function to the new page
def new_page(request):
    if request.method == 'POST':
        page_data = request.POST.get('usr_data_page')
        page_title = request.POST.get('usr_page_title')

        if not page_data or not page_title:
            return HttpResponse("Please make sure to fill both fields correctly")

        # getting old data to see if entry exists or not 
        list_data = util.list_entries()
        for i in list_data:
            if page_title == i:
                return HttpResponse("Entry already exits")
        
        # if all the validations passed then save the data 
        util.save_entry(page_title,page_data)

        # now redirects the page 
        return title_pag(request,page_title)


    return render(request,"encyclopedia/create_page.html")

# Function to edit page
def edit_page(request,title):
    
    if util.get_entry(title) is None:
        return HttpResponse("Entry does not exists")


    if request.method == 'POST':
        page_data = request.POST.get('edit_data_page')
        page_title = request.POST.get('edit_page_title')

        if not page_data or not page_title:
            return HttpResponse("Please make sure to fill both fields correctly")        
        # if all the validations passed then save the data 
        util.save_entry(page_title,page_data)
        # now redirects the page 
        return title_pag(request,page_title)

    return render(request,"encyclopedia/edit_entry.html",{
        "tit":title,"para": util.get_entry(title)
    })


# Random Page Functionality
def any_page(request):
    entries = util.list_entries()
    max_size = len(entries)
    lucky_num = random.randint(0,max_size-1)
    if request.method == "GET":
        return title_pag(request,entries[lucky_num])
    return index(request)