import uvicorn

from app.creator import create_app
from database import create_all

if __name__ == '__main__':
    create_all()
    app = create_app()
    uvicorn.run(app, host='0.0.0.0', port=8090)
