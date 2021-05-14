from quart import Quart, request, redirect
import asyncpg
import asyncio
import random
from dotenv import load_dotenv
import os
app = Quart(__name__)
load_dotenv()


loop = asyncio.get_event_loop()
DB_CONNECTION = loop.run_until_complete(
    (asyncpg.create_pool(f'postgres://postgres:{os.getenv("POSTGRES_PASS")}@localhost:5432/pastesite', loop=loop))
)


words = open('words.txt').read().splitlines()



def generate_id() -> str:
    selected_words = [random.choice(words).title() for i in range(3)]
    return ''.join(selected_words)

@app.route(rule='/')
async def root():
    return "Hello. This is my paste site. It's kinda basic."


@app.route('/pastes/<id>')
async def pastes(id):
    async with DB_CONNECTION.acquire() as conn:
        async with conn.transaction():
            content = await conn.fetchval('SELECT content from pastes where id = $1', id)
    if content is None:
        return ":( A paste with that id does not exist"
    return content

@app.route('/test')
async def test():
    thing = generate_id()
    return thing

@app.route('/upload', methods=['GET'])
async def upload():
    id = generate_id()
    content = request.args.get('content')
    if not content:
        return 'The content parameter is required', 400
    async with DB_CONNECTION.acquire() as conn:
        async with conn.transaction():
            await conn.execute('INSERT INTO PASTES VALUES($1, $2)', id, content)
    return {'id': f'{id}'}



app.run()
