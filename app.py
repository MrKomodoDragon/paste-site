from quart import Quart, request, redirect, render_template, flash, url_for
import asyncpg
import asyncio
import random
from dotenv import load_dotenv
import os

# the words list was yoinked from the mystbin repo
# here: https://raw.githubusercontent.com/PythonistaGuild/MystBin/dev-staging/mystbin/rest/utils/words.txt
words = open('words.txt').read().splitlines()

app = Quart(__name__, template_folder='templates/')

load_dotenv()
loop = asyncio.get_event_loop()

DB_CONNECTION = loop.run_until_complete(
    (asyncpg.create_pool(f'postgres://postgres:{os.getenv("POSTGRES_PASS")}@localhost:5432/pastesite', loop=loop))
)

def generate_id() -> str:
    selected_words = [random.choice(words).title() for _ in range(3)]
    return ''.join(selected_words)


@app.route('/', methods=['GET', 'POST'])
async def home():

    if request.method == "POST":
        paste_id = generate_id()
        content  = await request.form
        content  = content.get('content')
    
        if content:
            async with DB_CONNECTION.acquire() as conn:
                async with conn.transaction():
                    await conn.execute('INSERT INTO PASTES VALUES($1, $2)', paste_id, content)
            return redirect(url_for("pastes", paste_id=paste_id))

    return await render_template("index.html")


@app.route('/pastes/<str:paste_id>')
async def pastes(paste_id: str):
    async with DB_CONNECTION.acquire() as conn:
        async with conn.transaction():
            content = await conn.fetchval('SELECT content FROM pastes WHERE id = $1', paste_id)
    if content:
        return await render_template("view.html", content=content, paste_id=paste_id)
    else:
        return await render_template("notfound.html")


if __name__ == '__main__':
    app.run(loop=loop, debug=True)