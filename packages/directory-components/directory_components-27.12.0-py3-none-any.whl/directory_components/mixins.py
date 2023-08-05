from collections import namedtuple

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from directory_constants.choices import COUNTRY_CHOICES
from directory_constants import urls

from directory_components import helpers, forms


class CountryDisplayMixin:
    country_form_class = forms.CountryForm

    def get_context_data(self, *args, **kwargs):
        country_code = helpers.get_user_country(self.request)

        # if there is a country already detected we can hide the selector
        hide_country_selector = bool(country_code)
        country_name = dict(COUNTRY_CHOICES).get(country_code, '')

        country = {
            # used for flag icon css class. must be lowercase
            'code': country_code.lower(),
            'name': country_name,
        }

        country_form_kwargs = self.get_country_form_kwargs()

        return super().get_context_data(
            hide_country_selector=hide_country_selector,
            country=country,
            country_selector_form=self.country_form_class(
                **country_form_kwargs),
            *args, **kwargs
        )

    def get_country_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_country_form_initial_data(self.request),
            **kwargs,
        }


class EnableTranslationsMixin:
    template_name_bidi = None
    language_form_class = forms.LanguageForm

    def __init__(self, *args, **kwargs):
        dependency = 'directory_components.middleware.ForceDefaultLocale'
        if getattr(settings, 'MIDDLEWARE', []):
            assert dependency in settings.MIDDLEWARE
        else:
            assert dependency in settings.MIDDLEWARE_CLASSES
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        language_form_kwargs = self.get_language_form_kwargs()

        context['language_switcher'] = {
            'show': True,
            'form': self.language_form_class(**language_form_kwargs)
        }
        return context

    def get_language_form_kwargs(self, **kwargs):
        return {
            'initial': forms.get_language_form_initial_data(),
            **kwargs,
        }


class CMSLanguageSwitcherMixin:

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        form = forms.LanguageForm(
            initial={'lang': translation.get_language()},
            language_choices=self.page['meta']['languages']
        )
        show_language_switcher = (
            len(self.page['meta']['languages']) > 1 and
            form.is_language_available(translation.get_language())
        )
        return super().get_context_data(
            language_switcher={'form': form, 'show': show_language_switcher},
            *args,
            **kwargs
        )


class GA360Mixin:
    def __init__(self):
        self.ga360_payload = {}

    def set_ga360_payload(self, page_id, business_unit, site_section,
                          site_subsection=None):
        self.ga360_payload['page_id'] = page_id
        self.ga360_payload['business_unit'] = business_unit
        self.ga360_payload['site_section'] = site_section
        if site_subsection:
            self.ga360_payload['site_subsection'] = site_subsection

    def get_context_data(self, *args, **kwargs):
        self.ga360_payload['site_language'] = translation.get_language()

        try:
            self.ga360_payload['user_id'] = str(self.request.sso_user.id)
            self.ga360_payload['login_status'] = True
        except AttributeError:
            self.ga360_payload['user_id'] = None
            self.ga360_payload['login_status'] = False

        return super().get_context_data(
            ga360=self.ga360_payload,
            *args,
            **kwargs
        )


Page = namedtuple('Page', 'name title url sub_pages')
HeaderItem = namedtuple('HeaderItem', 'title url is_active')


class InternationalHeaderMixin:
    # header_section and header_subsection can be set in the views.
    header_section = ""
    header_subsection = ""

    pages = [
        Page(
            name='invest',
            title=_('Invest'),
            url=urls.SERVICES_INVEST,
            sub_pages=[]
        ),
        Page(
            name='uk_setup_guides',
            title=_('UK setup guide'),
            url=urls.GREAT_INTERNATIONAL_HOW_TO_SETUP_IN_THE_UK,
            sub_pages=[]
        ),
        Page(
            name='find_a_supplier',
            title=_('Find a UK supplier'),
            url=urls.SERVICES_FAS,
            sub_pages=[]
        ),
        Page(
            name='industries',
            title=_('Industries'),
            url=urls.GREAT_INTERNATIONAL_INDUSTRIES,
            sub_pages=[]
        ),
    ]

    def get_active_page(self):
        return next(
            (page for page in self.pages if page.name == self.header_section),
            None
        )

    def get_context_data(self, *args, **kwargs):

        header_items = [
            HeaderItem(
                title=page.title,
                url=page.url,
                is_active=page.name == self.header_section)
            for page in self.pages
        ]

        active_page = self.get_active_page()
        sub_pages = active_page.sub_pages if active_page else []

        sub_header_items = [
            HeaderItem(title=page.title,
                       url=page.url,
                       is_active=page.name == self.header_subsection)
            for page in sub_pages
        ]

        return super().get_context_data(
            header_items=header_items,
            sub_header_items=sub_header_items,
            pages=self.pages,
            *args,
            **kwargs
        )
