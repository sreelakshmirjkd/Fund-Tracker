from django.shortcuts import render, redirect

from django.views.generic import View

from expense.forms import ExpenseCreateForm, SignUpForm, LoginForm

from expense.models import Transaction

from django.db.models import Sum

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from expense.decorators import signin_required

from django.utils.decorators import method_decorator

from django.contrib import messages

from django.db.models import Q 

# Create your views here.

# ExpenseAdd
# ExpenseList
# ExpenseDetail
# ExpenseUpdate
# ExpenseDelete
# ExpenseSummary(filter)

# old method

# class ExpenseCreateView(View):

#     def get(self, request, *args, **kwargs):

#         form = ExpenseCreateForm()  # object

#         return render(request, "expense_add.html", {"form": form})


# new method

@method_decorator(signin_required, name="dispatch") # dispatch to select get/post function.
class ExpenseCreateView(View):

    template_name = "expense_add.html"

    form_class = ExpenseCreateForm

    def get(self, request, *args, **kwargs):


        # if not request.user.is_authenticated: # --> used decorators instead
             
        #      return redirect("signin")



        # step 1 - create form_instance

        form = self.form_class()

        return render(request, self.template_name, {"form":form})
    
    # sending response - request itself - using render function.
    # render must have atleast 2 paraeters -- response, template
    # client request is converted by python into its readable format like dict, list, str etc.


    def post(self, request, *args, **kwargs):

        form_instance = self.form_class(request.POST) 

        if form_instance.is_valid():


            # user connection method 1
            # ========================

            # data = form_instance.cleaned_data

            # Transaction.objects.create(**data,owner=request)   # Foreign key--- username and password-- # In the post data key:value. But in ORM key=value. So ** is used to unpack the data.

            # user connection method 2 -- simple method
            # ========================
          
            
            form_instance.instance.owner=request.user # Foreign key --- username and password connection-- form_instance is Expense create form. The model given here, Transaction is the instance. 
            
            # Next we take the owner field from the instance.

            form_instance.save() # Foreign key--- username and password connection--owner field missing which is added in the form. --> integrity error.



            
            # create will work since instance is not given with request.POST
            
            messages.success(request,"New expense has been added.")

            return redirect("listexpense") # or give the url withun two slashes.

    # render -- request, template_name, context
    # redirect -- name in urls.py

@method_decorator(signin_required, name="dispatch") # dispatch to select get/post function.
class ExpenseListView(View):

    template_name = "expense_list.html"

    def get(self, request, *args, **kwargs):

        search_text = request.GET.get("search-text")

        selected_category = request.GET.get("category","all")


        if search_text:

            qs = Transaction.objects.filter(owner=request.user) # data of login user


            qs = qs.filter(Q(category__contains=search_text)|Q(title__contains=search_text)) # double underscore "__contains". exzct match - category only i.e., filter optionfrom model/form

        elif selected_category == "all" and search_text==None:

            qs = Transaction.objects.filter(owner=request.user)

        else:

            qs = Transaction.objects.filter(category=selected_category, owner=request.user)
             

        qs_category = Transaction.objects.all().values_list("category", flat=True).distinct()

        # print(qs_category)

        # ----  <QuerySet [('Food',), ('Food',), ('Rent',)]>
        # To remove excess brackets -- to flat --> flat=True
        # -- <QuerySet ['Food', 'Food', 'Rent']> 
        # -- <QuerySet ['Food', 'Rent']> --> distinct()

        return render(request, self.template_name, {"data":qs, "category_filter":qs_category, "selected_category":selected_category})
    

@method_decorator(signin_required, name="dispatch") # dispatch to select get/post function.
class ExpenseDetailView(View):

    template_name="expense_detail.html"

    def get(self, request, *args, **kwargs):

        id = kwargs.get("pk")        

        qs = Transaction.objects.get(id=id)

        return render(request, self.template_name, {"data":qs})

@method_decorator(signin_required, name="dispatch") # dispatch to select get/post function.
class ExpenseDeleteView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        Transaction.objects.get(id=id).delete()

        messages.success(request,"Expense has been removed.")

        return redirect("listexpense") 

    # Form
    # ====
    
        
    # class ExpenseUpdateView(View):

    #     template_name="expense_update.html"

    #     form_class = ExpenseCreateForm

    #     def get(self, request, *args, **kwargs):

    #         id = kwargs.get("pk")

    #         trans_obj = Transaction.objects.get(id=id) # query set - initial will not identify this. Convert it into a dictionary.



    #         instance_dictionary = {

    #             "title": trans_obj.title,
    #             "amount": trans_obj.amount,
    #             "category": trans_obj.category,
    #             "payment_method": trans_obj.payment_method,
    #             "priority": trans_obj.priority

    #         }

    #         form_instance = self.form_class(initial=instance_dictionary) 
            
    #         --- initial should be a dict. both within ""

    #         ----------------------------------------


@method_decorator(signin_required, name="dispatch") # dispatch to select get/post function.   
class ExpenseUpdateView(View):

    template_name="expense_update.html"

    form_class = ExpenseCreateForm

    def get(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        trans_obj = Transaction.objects.get(id=id)

        form_instance = self.form_class(instance=trans_obj) # instance - to initialise

        return render(request, self.template_name, {"form":form_instance})
    
    # Form
    # ====

    # def post(self, request, *args, **kwargs):

    #     form_instance = self.form_class(request.POST)

    #     id = kwargs.get("pk")

    #     if form_instance.is_valid():

    #         data = form_instance.cleaned_data   # ---- Form

    #         Transaction.objects.filter(id=id).update(**data)   # ----- Form

    #         return redirect("listexpense")
        
    #     return render(request, self.template_name, {"form": form_instance})




    # ModelForm
    # =========

    def post(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        transaction_object = Transaction.objects.get(id=id)

        form_instance = self.form_class(request.POST, instance=transaction_object)

        if form_instance.is_valid():

            form_instance.save()  # update will work since instance is given with request.POST -- i.e., form is initialised

            messages.success(request, "Data had been updated.")

            return redirect("listexpense")
        
        messages.error(request, "Failed to update the data!")

        return render(request, self.template_name, {"form": form_instance})



    # Expense Summary
    # ===============

    # 1. Total Expense
    # 2. Category Summary
    # 3. Priority Summary

    # aggregate -- Sum, Max, Min, Avg, Count are in django.db.models
    # annotate -- to group based on category
    # --------------------

@method_decorator(signin_required, name="dispatch")
class ExpenseSummaryView(View):

    template_name = "expense_summary.html"

    def get(self, request, *args, **kwargs):

        expense_total = Transaction.objects.filter(owner=request.user).aggregate(total=Sum("amount"))

        category_summary = Transaction.objects.filter(owner=request.user).values("category").annotate(total=Sum("amount"))

        payment_summary = Transaction.objects.filter(owner=request.user).values("payment_method").annotate(total=Sum("amount"))

        priority_summary =Transaction.objects.filter(owner=request.user).values("priority").annotate(total=Sum("amount"))

        context = {

            "total_expense":expense_total.get("total"),

            "category_summary": category_summary,

            "payment_summary": payment_summary,

            "priority_summary": priority_summary,

        }

        return render(request, self.template_name, context)


class SignUpView(View):

    template_name = 'register.html'

    form_class = SignUpForm

    def get(self, request, *args, **kwargs):

        form_instance = self.form_class

        return render(request, self.template_name, {"form":form_instance})
        

    def post(self, request, *args, **kwargs):

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            data = form_instance.cleaned_data # if we are not taking cleaned data, the password will get saved as a string

            User.objects.create_user(**data) # create_user -- to encrypt password

            print("Registered Successfully")

            return redirect("signin")
        
        return render(request, self.template_name, {"form":form_instance})

class SignInView(View):

    template_name = "sign_in.html"

    form_class = LoginForm    

    def get(self, request, *args, **kwargs):

        form_instance = self.form_class()

        return render(request, self.template_name, {"form":form_instance})
    
    def post(self, request, *args, **kwargs):

        # extract username and password
        # check their validity
        # start session

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            user_name = form_instance.cleaned_data.get("username")
            pass_word = form_instance.cleaned_data.get("password") # not encrypted plain password

            # we need to check this password after encryption with the already existing encrypted password

            user_object = authenticate(request, username=user_name, password=pass_word)

            # checks credentials and login here.

            if user_object:

                login(request, user_object)

                # login - to start session

                print(request.user) # only after session -- 

                return redirect("summaryexpense")
            
        return render(request, self.template_name, {"form":form_instance})

@method_decorator(signin_required, name="dispatch")
class SignOutView(View):

    def get(self, request, *args, **kwargs):

        logout(request)

        return redirect("signin")






        




