from flask.ext.login import current_user
from flask.ext.principal import Principal, identity_loaded, RoleNeed

__author__ = 'airead'

principal = Principal()


def get_user_permissions(user):
    permissions = set()
    groups = set()
    for assoc in user.groups:
        g = assoc.group
        groups.add(g)
    print 'user %s has groups: %s' % (user, groups)

    for group in groups:
        for assoc in group.permissions:
            p = assoc.permission
            permissions.add(p)
    print 'user %s has permissions: %s' % (user, permissions)

    return permissions


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.auth_user = current_user

    print 'identity.auth_user', identity.auth_user.user

    user = current_user.user
    permissions = get_user_permissions(user)

    ## Add the UserNeed to the identity
    #if hasattr(current_user, 'id'):
    #    identity.provides.add(UserNeed(current_user.id))
    #
    ## Assuming the User model has a list of roles, update the
    ## identity with the roles that the user provides
    #if hasattr(current_user, 'roles'):
    #    for role in current_user.roles:
    #        identity.provides.add(RoleNeed(role.name))
    #
    ## Assuming the User model has a list of posts the user
    ## has authored, add the needs to the identity
    #if hasattr(current_user, 'posts'):
    #    for post in current_user.posts:
    #        identity.provides.add(EditBlogPostNeed(unicode(post.id)))