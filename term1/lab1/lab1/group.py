import datetime


class Groups(object):

    def __init__(self):
        self.groups = []

    def is_empty(self):
        if self.groups:
            return False
        else:
            return True

    def contains(self, name):
        for group in self.groups:
            if group.name == name:
                return True
        return False

    def add(self, group):
        self.groups.append(group)

    def delete(self, name):
        for group in self.groups:
            if group.name == name:
                self.groups.remove(group)
                return 0
        return 1

    def delete_captain(self, student_id):
        for group in self.groups:
            if group.captain == student_id:
                group.captain = ""
                return 0
        return 1

    def update(self, new_group):
        for group in self.groups:
            if group.name == new_group.name:
                self.groups.remove(group)
                self.groups.append(new_group)
                return 0
        return 1

    def print_name(self, name):
        for group in self.groups:
            if group.name == name:
                group.print_itself()
                return 0
        return 1

    def print_all(self):
        for group in self.groups:
            group.print_itself()


class Group(object):

    def __init__(self, name, creation_date=datetime.datetime.now().date(), captain=""):
        self.captain = captain
        self.creation_date = creation_date
        self.name = name

    def print_itself(self):
        if self.captain == "":
            cap = "absent (to add a captain use command 'gr_update')"
        else:
            cap = self.captain
        print ("Name: %s, Creation date: %s, Captain of the group: %s" % (self.name, self.creation_date, cap))
