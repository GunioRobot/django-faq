import datetime
from django.views.generic.list_detail import object_detail, object_list
<<<<<<< HEAD:faq/views.py
from faq.models import Question

def question_detail(request, slug, template_name='faq/question_detail.html',
                    extra_context=None):
    """
    Displays an invidual question.
    """
    return object_detail(
        request,
        template_name = template_name,
        extra_context = extra_context or {},
        slug = slug,
        slug_field = 'slug',
        queryset = Question.objects.active(),
    )

def question_list(request, template_name='faq/question_list.html',
                  extra_context=None):
    """
    Displays a list of all the questions.
    
    """
    # NOTE:
    # this below is NOT NEEDED really so I would remove but I think it's a
    # good example for people to see how they could "extend" their existing
    # extra_context using a parameter value to allow developers to make their
    # app more reusable we set the below dict value and then allow the user
    # to pass along their own if they we then populate the user supplied
    # extra_context using the update method

    if extra_context is None:
        extra_context = {}
    extra = {
        'created_on': datetime.datetime.now()
    }
    extra.update(extra_context)
=======
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models import Question
from forms import SubmitFAQForm

def question_detail(request, slug, template_name='faq/question_detail.html', extra_context={}):
    """
    Displays an individual question.
    
    """

    return object_detail(
        request,
        template_name = template_name,
        extra_context = extra_context,
        slug = slug,
        slug_field = 'slug',
        queryset = Question.objects.active(user=request.user),
    )    
        
def question_list( request, template_name='faq/question_list.html',
					extra_context={}, group=False):
    '''
    Displays a list of all the questions.
    '''
    
    # NOTE:
    # The code shown here is NOT REALLY NEEDED, but it is a good example
	# of extending an app using extra_content and such.
    # Specifically note how we set the dict value and then allow the user
	# to pass along their own additional extra_context using 'update'.

    query_set = Question.objects.active(group=group,user=request.user)
    last_update = query_set.values('updated_on').order_by('-updated_on',)[0]
    
    extra = { 'updated_on': last_update['updated_on'] }
 
    extra.update( extra_context )
      
>>>>>>> 5103a3f9e904b2c0ee327ce6cf0b3894a046d42a:faq/views.py
    return object_list(
        request,
        template_name = template_name,
        extra_context = extra,
<<<<<<< HEAD:faq/views.py
        queryset = Question.objects.active(),
    )
=======
        queryset = query_set
    )

def faq_list( request, template_name='faq/faq_list.html', extra_context={} ):
    '''
    Display a typical FAQ view without group headers.
	Shows how to "extend" or "override" the default view supplied above.
	We also make sure this view is also overridable.
    '''
    
    extra = { 'page_title': 'FAQs' }
    extra.update( extra_context )

    return question_list( request, template_name=template_name, extra_context=extra )

def faq_list_by_group( request,
                       template_name='faq/faq_list_by_group.html',
                       extra_context={} ):

    extra = { 'page_title': 'Grouped FAQs' }
    extra.update( extra_context )
    
    return question_list( request, group=True,
                          template_name=template_name, extra_context=extra
						)

def submit_faq( request, form_class=SubmitFAQForm, 
             template_name="faq/submit_question.html",
             success_url="/", extra_context={} ):
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            question = form.save()
            if request.user.is_authenticated():
                slug = question.slug
                question.slug = slug.replace("anon",request.user.username)
                question.created_by = request.user
                # Now set up a confirmation message for the user
                request.user.message_set.create(
                    message="Your question was submitted and will be reviewed by the site administrator for possible inclusion in the FAQ." )
            question.save()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    context = { 'form': form }
    context.update( extra_context )
    return render_to_response( template_name, context,
                              context_instance = RequestContext( request ))

>>>>>>> 5103a3f9e904b2c0ee327ce6cf0b3894a046d42a:faq/views.py
