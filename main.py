import socketio
import uvicorn
from models import User
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

app = socketio.ASGIApp(sio)


rooms: list = ['Общая', 'Спорт', 'Игры', 'Книги']
users: dict[str, User] = {}



@sio.on('get_rooms')
async def get_rooms(sid, data):
    await sio.emit('rooms', rooms, to=sid)

@sio.on('join')
async def join_to_room(sid, data):
    users[sid] = User(room=data['room'], name=data['name'])
    await sio.emit('move', {'room': data['room']}, to=sid, room=data['room'])
    await sio.enter_room(sid, data['room'])
    await sio.save_session(sid, users[sid])

@sio.on('leave')
async def leave_room(sid, data):
    get_me = await sio.get_session(sid)
    await sio.leave_room(sid, get_me.room)

@sio.event
async def disconnect(sid):
    try:
        del users[sid]
    except KeyError:
        pass

@sio.on('send_message')
async def send_message_in_room(sid, data):
    get_me = users[sid]
    if not data['text']:
        pass
    else:
        await sio.emit('message', room=get_me.room, data={
            'author': get_me.name,
            'name':get_me.name, 'text': data['text'], 
            'room': get_me.room
            })




if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
