from django.shortcuts import redirect
#  use decorators to use for all purposes where signin is mandatory.

from django.contrib import messages

def signin_required(fn):

    def wrapper(request,*args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request,"Invalid session. Please login!") # give before redirect. Message should be added to the template shown after redirecting.
            #  no need to pas through context since it is using context_processor in django.
            return redirect("signin")
        
        else:

            return fn(request, *args, **kwargs)
        
    return wrapper  # inner function is called by outer function.  - name referencing just to work that function.

# To apply it in views, import this function and method_decorator.
# Don't add decorator onthe top of class_name since, we need to decorate methods.
# method_decorator - decorator in django.
# we use the name "dispatch" since it's the name of method used in django.
# don't change the name "dispatch".