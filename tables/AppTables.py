from anvil.tables.basefunction import BaseFunction

TABLES = dict(
    expenses=dict(
        status='string',
        description='string',
        created='datetime',
        amount='number',
        merchant='string',
        attachment='media',
        submitted_by='liveObject',
        reject_message='string',
    ),
    users=dict(
        email='string',
        enabled='bool',
        last_login='datetime',
        password_hash='string',
        n_password_failures='number',
        confirmed_email='bool',
        signed_up='datetime',
        email_confirmation_key='string',
        role='string',
    ),
)


class AppTables:
    def __init__(self):
        self.expenses = BaseFunction('expenses', TABLES['expenses'])
        self.users = BaseFunction('users', TABLES['users'])


app_tables = AppTables()
