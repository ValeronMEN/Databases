import datetime


class Students(object):

    def __init__(self):
        self.students = {}
        self.id = 1

    def is_empty(self):
        if self.students:
            return False
        else:
            return True

    def contains(self, user_id):
        return user_id in self.students

    def add(self, student):
        self.students[self.id] = student
        self.id += 1

    def delete(self, user_id):
        return self.students.pop(user_id, None)

    def delete_by_group_name(self, group_name):
        keys = self.students.keys()
        for key in keys:
            if self.students.get(key).group_name == group_name:
                self.students.pop(key)

    def update(self, user_id, student):
        self.students[user_id] = student

    def print_id(self, user_id):
        print ("ID: %s" % user_id)
        self.students.get(user_id).print_itself()
        return 0

    def print_all(self):
        if self.is_empty():
            return 1
        keys = self.students.keys()
        for key in keys:
            print ("ID: %s" % key)
            self.students.get(key).print_itself()
        return 0

    def print_group(self, group_name):
        if self.is_empty():
            return 1
        keys = self.students.keys()
        for key in keys:
            if self.students.get(key).group_name == group_name:
                print ("ID: %s" % key)
                self.students.get(key).print_itself()
        return 0

    def print_the_youngest(self):
        if self.is_empty():
            return 1
        min_date = datetime.date(1899, 01, 01)
        keys = self.students.keys()
        for key in keys:
            current_birthday_key = self.students.get(key).birthday
            if current_birthday_key > min_date:
                min_date = current_birthday_key
        for key in keys:
            student_the_youngest = self.students.get(key)
            if student_the_youngest.birthday == min_date:
                print ("ID: %s" % key)
                student_the_youngest.print_itself()
                break
        return 0

    def get(self, user_id):
        return self.students.get(user_id)


class Student(object):

    def __init__(self, name, surname, birthday, group_name):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.group_name = group_name

    def __str__(self):
        return "name=%s, surname=%s, birthday=%s, group_name=%s" % (self.name, self.surname, self.birthday,
                                                                    self.group_name)

    def print_itself(self):
        print ("Name: %s, Surname: %s, Birthday: %s, Group: %s" % (self.name, self.surname, self.birthday,
                                                                   self.group_name))
