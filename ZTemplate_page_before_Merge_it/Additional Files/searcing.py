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




		function usernameForm(event) {
      event.preventDefault();
      const usernameInputValue =
        document.getElementById("usernameInput").value;
      if (usernameInputValue.trim() !== "") {
        document.getElementById("usernameForm").classList.add("hidden");
        document.getElementById("radioContainer").classList.remove("hidden");
        document.getElementById("showVotes").classList.remove("hidden");
      } else {
        alert("Username field is mandatory. Please enter a username.");
      }
    }

    <div class="row mt-5 justify-content-center">
      <div id="usernameForm">
        <h2>Enter Username</h2>
        <form id="usernameInputForm" onsubmit="usernameForm(event)">
          <input type="text" id="usernameInput" placeholder="Enter Username" class="form-control mb-2" />
          <button type="submit" class="btn btn-primary">
            Next
          </button>
        </form>
      </div>

   <div id="radioContainer" class="hidden">
        <!-- The select field will be inserted here -->
      </div>
      <div id="showVotes" class="row justify-content-center mt-5 hidden">
        <div class="col-8">


        swal({
                                type: 'success',
                                text: 'تم تسليم السؤال'
                            }
                            ).then(function () {
                                window.location = "{% url 'student_questions' %}";
                            });
<head>
    <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/sweetalert/dist/sweetalert.css">
</head>