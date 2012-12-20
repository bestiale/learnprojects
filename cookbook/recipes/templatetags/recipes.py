from django import template
from ..forms import CommentForm

register = template.Library()

@register.tag(name='is_author')
def do_is_author(parser, token):
    """The ``{% is_author %}`` tag displays the first section, if the user is
    the author of the recipe or a staff member. Otherwise the second section
    is displayed.

    ::

        {% is_author user recipe %}
            The user is owner of this recipe or a staff member.
        {% else %}
            The user has no right to edit this recipe.
        {% endis_author %}
    """
    try:
        tag_name, user, recipe = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%s requires a Recipe and an User as arguments' 
            % token.contents.split()[0])
    nodelist_true = parser.parse(('else', 'endis_author'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endis_author',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IsAuthorNode(user, recipe, nodelist_true, nodelist_false)

class IsAuthorNode(template.Node):
    def __init__(self, user, recipe, nodelist_true, nodelist_false):
        self.user = template.Variable(user)
        self.recipe = template.Variable(recipe)
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        try:
            user = self.user.resolve(context)
            recipe = self.recipe.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if recipe.author.id == user.id or user.is_staff:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

@register.inclusion_tag('recipes/comments.html', takes_context=True)
def show_comments(context, recipe):
    context.update({
        'comments': recipe.comments.all()
    })
    return context