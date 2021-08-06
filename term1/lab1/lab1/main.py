import cPickle as Pickle
import group
import student
import module

groups_class = group.Groups()
students_class = student.Students()
try:
    students_file = open('students.db', 'rb')
except IOError as e:
    print("File 'students.db' can't be opened")
else:
    with students_file:
        students_class = Pickle.load(students_file)
        students_file.close()
try:
    groups_file = open('groups.db', 'rb')
except IOError as e:
    print("File 'groups.db' can't be opened")
else:
    with groups_file:
        groups_class = Pickle.load(groups_file)
        groups_file.close()
print ("Enter the command. For help type 'help'")
while True:
    command = raw_input("> ")
    if command == "help":
        print('''Help menu:
            > type 'quit' to quit
            > type 'st_add' to create a new student
            > type 'gr_add' to create a new group
            > type 'st_read_all' to observe all students
            > type 'gr_read_all' to observe all groups
            > type 'gr_read' to observe all students in the current group
            > type 'st_update' to update the student information
            > type 'gr_update' to update the group information
            > type 'st_delete' to delete the student
            > type 'gr_delete' to delete the group
            > type 'st_read_the_youngest' to search for the youngest student''')
    elif command == "gr_read":
        name = raw_input("Enter the name of the group to observe:\n")
        if not groups_class.contains(name):
            print ("Error! This group doesn't exist")
        else:
            students_class.print_group(name)
    elif command == "st_read":
        user_id = raw_input("Enter the ID of the student to observe:\n")
        if not students_class.contains(int(user_id, 10)):
            print ("Error! This student doesn't exist")
        else:
            students_class.print_id(int(user_id, 10))
    elif command == "gr_read_all":
        if not groups_class.is_empty():
            groups_class.print_all()
        else:
            print ("This table is empty")
    elif command == "st_read_all":
        if not students_class.is_empty():
            students_class.print_all()
        else:
            print ("This table is empty")
    elif command == "st_add":
        group_name = raw_input("Enter the group name where the new student will be stored:\n")
        if not groups_class.contains(group_name):
            print ("Error! This group doesn't exist")
        else:
            name = raw_input("Enter the name of the new student:\n")
            surname = raw_input("Enter the surname:\n")
            birthday = raw_input("Enter the birthday (YYYY MM DD):\n")
            students_class.add(student.Student(name, surname, module.date_check(birthday), group_name))
            print (name + " was added")
    elif command == "gr_add":
        group_name = raw_input("Enter the name of the new group:\n")
        groups_class.add(group.Group(group_name))
        print (group_name + " was added")
    elif command == "st_read_the_youngest":
        if students_class.print_the_youngest() == 1:
            print ("There's no student in the table")
    elif command == "st_update":
        student_id = raw_input("Enter the ID of the student to modify:\n")
        if students_class.contains(int(student_id, 10)):
            students_class.print_id(int(student_id, 10))
            birthday = raw_input("Enter the birthday (YYYY MM DD):\n")
            group_name = raw_input("Enter the group name:\n")
            if groups_class.contains(group_name):
                if students_class.get(int(student_id, 10)).group_name != group_name:
                    groups_class.delete_captain(student_id)
                name = raw_input("Enter the name:\n")
                surname = raw_input("Enter the surname:\n")
                students_class.update(int(student_id, 10),
                                      student.Student(name, surname, module.date_check(birthday),
                                                      group_name))
                print (student_id + " was updated")
            else:
                print ("Error! " + group_name + " is absent in the student table")
        else:
            print ("Error! " + student_id + " hasn't been found")
    elif command == "gr_update":
        group_name = raw_input("Enter the name of the group to modify:\n")
        if groups_class.print_name(group_name) == 0:
            creation_date = raw_input("Enter the date of the group creation (YYYY MM DD):\n")
            user_id = raw_input("Enter the ID of the captain (a student ID):\n")
            if students_class.contains(int(user_id, 10)):
                groups_class.update(group.Group(group_name, module.date_check(creation_date), user_id))
                print (group_name + " was updated")
            else:
                print ("Error! " + user_id + " is absent in the student table")
        else:
            print ("Error! " + group_name + " hasn't been found")
    elif command == "st_delete":
        id_st_to_delete = raw_input("Enter the ID of the student to delete:\n")
        if students_class.delete(int(id_st_to_delete, 10)) is None:
            print(id_st_to_delete + " hasn't been found")
        else:
            print (id_st_to_delete + " was deleted")
            groups_class.delete_captain(id_st_to_delete)
    elif command == "gr_delete":
        name = raw_input("Enter the name of the group to delete:\n")
        if groups_class.delete(name) == 0:
            print (name + " was deleted")
            students_class.delete_by_group_name(name)
        else:
            print(name + " hasn't been found")
    elif command == "quit":
        student_conn = open('students.db', 'wb')
        Pickle.dump(students_class, student_conn)
        student_conn.close()
        group_conn = open('groups.db', 'wb')
        Pickle.dump(groups_class, group_conn)
        group_conn.close()
        break
    else:
        print("Unknown command. For help type 'help'")

