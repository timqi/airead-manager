from flask.ext.login import current_user
from flask.ext.principal import Principal, identity_loaded, RoleNeed, Identity
from contextlib import contextmanager

__author__ = 'airead'

principal = Principal()


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    if len(identity.provides) != 0:  # for unit test
        return

    # Set the identity user object
    identity.auth_user = current_user

    print 'identity.auth_user', identity.auth_user.user

    user = current_user.user
    permissions = user.get_permissions()

    tags = [p.tag for p in permissions]
    print 'tags: ', tags

    for tag in tags:
        identity.provides.add(RoleNeed(tag))


# for unit test
@contextmanager
def role_set(role):
    @principal.identity_loader
    def _():
        print 'role set2 run'
        identity = Identity('test')
        identity.provides.add(role)
        return identity

    yield
    principal.identity_loaders.popleft()
