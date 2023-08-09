from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin


class HomeView(TemplateView):
    template_name = "core/index.html"


class AboutPageView(TemplateView):
    template_name = "core/about.html"


class ModalMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        confirm_id = kwargs.get("id")

        if not confirm_id:
            return HttpResponse(content="<p>No Value for id provided.</p>", status=400)

        context["confirm_id"] = confirm_id
        return context
