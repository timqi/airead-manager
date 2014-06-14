define [], () ->
  Roles =
    admin: 'admin'
    guest: 'guest'
    databaseManager: 'databaseManager'
    databaseSetting: 'databaseSetting'
    systemSetting: 'systemSetting'
    holidayManager: 'holidayManager'
    userManager: 'userManager'
    groupManager: 'groupManager'

  return {
    Roles: Roles
  }