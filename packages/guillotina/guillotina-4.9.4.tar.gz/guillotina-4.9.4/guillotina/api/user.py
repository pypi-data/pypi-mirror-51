from guillotina import configure
from guillotina.component import get_utility
from guillotina.interfaces import IContainer
from guillotina.interfaces import IApplication
from guillotina.interfaces import IGroups
from guillotina.interfaces import IInteraction


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@user',
    summary='Get information on the currently logged in user',
    responses={
        "200": {
            "description": "Get information on the user",
            "schema": {
                "properties": {}
            }
        }
    })
@configure.service(
    context=IApplication, method='GET',
    permission='guillotina.AccessContent', name='@user',
    summary='Get information on the currently logged in user',
    responses={
        "200": {
            "description": "Get information on the user",
            "schema": {
                "properties": {}
            }
        }
    })
async def get_user_info(context, request):
    """Return information about the logged in user.
    """
    result = {}
    groups = set()
    principal = IInteraction(request).principal
    result[principal.id] = {
        'roles': principal.roles,
        'groups': principal.groups,
        'permissions': principal.permissions,
        'properties': principal.properties
    }
    groups.update(principal.groups)

    group_search = get_utility(IGroups)
    result['groups'] = {}
    for group in groups:
        group_object = group_search.get_principal(group)
        result['groups'][group_object.id] = {
            'roles': group_object.roles,
            'groups': group_object.groups
        }

    return result
