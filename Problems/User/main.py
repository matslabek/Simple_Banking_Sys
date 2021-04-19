class User:
    n_active = 0
    users = []

    def __init__(self, active, user_name):
        self.active = active
        self.user_name = user_name