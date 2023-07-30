def main_index(request):
    """

    @type request: HttpRequest
    """

    from django.shortcuts import render

    return render(request, 'base.html', {
    })
