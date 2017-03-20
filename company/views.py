from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Postform
# Create your views here.
def post_list(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Postform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            instance=form.save(commit=False)
            instance.save()
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form=Postform()
    return render(request, 'company/tempform.html', {'form':form})