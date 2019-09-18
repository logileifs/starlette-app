from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse

import uvicorn

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory="front/static"))


@app.route('/', methods=['get'])
async def signup_get(request):
	return FileResponse('front/static/index.html', media_type='html')


if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8989)
