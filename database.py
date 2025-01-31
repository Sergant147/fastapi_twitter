from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from message import Message
from student import Student
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataBaseLayer:
    def __init__(self):
        self.engine = create_engine("postgresql://postgres:mysecretpassword@localhost/mydb", echo=True)
        Base.metadata.create_all(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def read_students(self):
        return self.session.query(Student).all()

    def read_messages(self):
        return self.session.query(Message).all()

    def add_student(self, student):
        self.session.add(student)
        self.session.commit()
        return student

    def add_message(self, id, likes, dislikes, content, author_id):
        message = Message(id, likes, dislikes, content, author_id)
        self.session.add(message)
        self.session.commit()
        self.recalculate_score(author_id)
        return message

    def delete_message(self, id):
        message = self.session.query(Message).filter_by(id=id).first()
        if message:
            author_id = message.author_id
            self.session.delete(message)
            self.session.commit()
            self.recalculate_score(author_id)
        return id

    def delete_user(self, name):
        user = self.session.query(Student).filter_by(name=name).first()
        if user:
            user_id = user.id
            self.session.delete(user)
            for message in self.read_messages():
                if message.author_id == user.id:
                    self.session.delete(message)
            self.session.commit()
            self.recalculate_score(user_id)
        return name

    def edit_user(self, user_id, new_name, new_age):
        user = self.session.query(Student).filter_by(id=user_id).first()
        if user:
            user.name = new_name
            user.age = new_age
            self.session.commit()
        return user

    def edit_message(self, message_id, new_content):
        message = self.session.query(Message).filter_by(id=message_id).first()
        if message:
            message.content = new_content
            self.session.commit()
        return message

    def subscribe(self, who_subscribes, subscribes_who):
        subscriber = self.session.query(Student).filter_by(id=who_subscribes).first()
        subscribed = self.session.query(Student).filter_by(id=subscribes_who).first()
        if subscriber and subscribed:
            subscriber.subscriptions += 1
            subscribed.subscribed += f"{subscriber.id},"
            self.session.commit()
        return who_subscribes, subscribes_who

    def unsubscribe(self, who_subscribes, subscribes_who):
        subscriber = self.session.query(Student).filter_by(id=who_subscribes).first()
        subscribed = self.session.query(Student).filter_by(id=subscribes_who).first()
        if subscriber and subscribed:
            subscriber.subscriptions -= 1
            subscribed.subscribed = subscribed.subscribed.replace(f"{subscriber.id},", "")
            self.session.commit()
        return who_subscribes, subscribes_who

    def like(self, message_id, you_id):
        message = self.session.query(Message).filter_by(id=message_id).first()
        if message:
            message.likes += 1
            self.session.commit()
            self.recalculate_score(message.author_id)
        return message_id, you_id

    def dislike(self, message_id, you_id):
        message = self.session.query(Message).filter_by(id=message_id).first()
        if message:
            message.dislikes += 1
            self.session.commit()
            self.recalculate_score(message.author_id)
        return message_id, you_id

    def recalculate_score(self, user_id):
        user = self.session.query(Student).filter_by(id=user_id).first()
        if user:
            messages = self.session.query(Message).filter_by(author_id=user.id).all()
            score = sum(message.likes for message in messages) - sum(message.dislikes for message in messages)
            user.score = score
