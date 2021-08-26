from django.http import HttpResponseBadRequest


def required_ajax(f):
    """
    AJAX request required decorator
    use it in your views:

    @required_ajax
    def my_view(request):
    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
