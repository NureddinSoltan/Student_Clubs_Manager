<form action="{% url 'search_view' %}"  method="POST">
								{% csrf_token %}
								<div class="row gtr-uniform gtr-50">
									<div class="col-8 col-12-xsmall"><input type="text" name="search" placeholder="البحث.." class="search-input special_text" /></div>
									<div class="col-4 col-12-xsmall" style="padding-top: 1em !important;"><input type="submit" value="بحث" class="fit primary search-input-button special_text" /></div>
								</div>
							</form>

def search_view(request, *args, **kwargs):
    search_key_word = request.POST["search"]
    if request.method == 'POST':
        articles = Article.objects.filter(Q(content__contains=search_key_word) | Q(title__contains=search_key_word))

    return render(request, 'search/search.html', {'title': search_key_word, 'articles': articles})