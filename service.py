from database import DataBaseLayer
from student import Student
from message import Message


class Service:
    def __init__(self):
        self.database = DataBaseLayer()
        self.last_id = self.get_last_student_id()
        self.last_message_id = self.get_last_message_id()

    def get_last_student_id(self):
        last_student = self.database.session.query(Student).order_by(Student.id.desc()).first()
        return last_student.id if last_student else 0

    def get_last_message_id(self):
        last_message = self.database.session.query(Message).order_by(Message.id.desc()).first()
        return last_message.id if last_message else 0

    def get_all_students(self):
        return self.database.read_students()

    def get_all_messages(self):
        return self.database.read_messages()

    def add_student(self, name, age, details):
        student = Student(self.last_id + 1, 0, "", 0, name, int(age), details)
        self.database.add_student(student)
        self.last_id += 1
        return student

    def add_message(self, content, author_id):
        result = self.database.add_message(self.last_message_id + 1, 0, 0, content, author_id)
        self.last_message_id += 1
        return result

    def delete_message(self, message_id):
        return self.database.delete_message(message_id)

    def delete_user(self, id):
        return self.database.delete_user(id)

    def edit_message(self, content, message_id):
        return self.database.edit_message(message_id, content)

    def edit_user(self, id, new_name, new_age):
        return self.database.edit_user(id, new_name, new_age)

    def like_message(self, message_id, me_id):
        return self.database.like(message_id, me_id)

    def dislike_message(self, message_id, me_id):
        return self.database.dislike(message_id, me_id)

    def subscribe(self, ws, sw):
        return self.database.subscribe(ws, sw)

    def unsubscribe(self, ws, sw):
        return self.database.unsubscribe(ws, sw)
