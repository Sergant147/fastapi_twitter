from fastapi import FastAPI
import uvicorn
from service import Service

app = FastAPI()
service = Service()


@app.get("/about", tags=['Get'])
def about_us():
    return "A clone of Twitter"


@app.get("/student", tags=['Get'])
def get_the_list_of_all_the_students():
    return service.get_all_students()


@app.get("/message", tags=['Get'])
def get_the_list_of_all_the_message():
    return service.get_all_messages()


@app.post("/student/add/{name}/{age}/{details}", tags=['Post'])
def add_a_student(name, age, details):
    return service.add_student(name, age, details)


@app.post("/message/add/{author_id}/{content}", tags=['Post'])
def add_a_message(author_id, content):
    return service.add_message(content, int(author_id))


@app.delete("/message/remove/{message_id}", tags=['Delete'])
def delete_a_message(message_id):
    return service.delete_message(message_id)


@app.delete("/student/delete/{name}", tags=['Delete'])
def delete_a_student_and_his_messages(name):
    return service.delete_user(name)


@app.put("/student/edit/{id}/{name}/{age}", tags=['Put'])
def edit_a_user(id, name, age):
    return service.edit_user(id, name, age)


@app.put("/message/edit/{id}/{content}", tags=['Put'])
def edit_a_message(id, content):
    return service.edit_message(content, id)


@app.post("/message/like/{who_likes_id}/{message_id}", tags=['Post'])
def like_a_message(who_likes_id, message_id):
    return service.like_message(message_id, who_likes_id)


@app.post("/message/dislike/{who_dislikes_id}/{message_id}", tags=['Post'])
def dislike_a_message(who_dislikes_id, message_id):
    return service.dislike_message(message_id, who_dislikes_id)


@app.post("/student/subscribe/{who_subscribes}/{student_id}", tags=['Post'])
def subscribe(who_subscribes, student_id):
    return service.subscribe(who_subscribes, student_id)


@app.post("/student/unsubscribe/{who_unsubscribes}/{student_id}", tags=['Post'])
def unsubscribe(who_unsubscribes, student_id):
    return service.unsubscribe(who_unsubscribes, student_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
