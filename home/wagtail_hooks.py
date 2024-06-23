from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from home.models import PotteryCategory

class PotteryCategorySnippetViewSet(SnippetViewSet):
    model = PotteryCategory
    ordering = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

class PotteryMenuGroup(SnippetViewSetGroup):
    menu_label = "Pottery Categories"
    menu_icon = "suitcase"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (
        PotteryCategorySnippetViewSet,

    )


register_snippet(PotteryMenuGroup)