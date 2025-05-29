import sys
import os

from apis import app
import uvicorn

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
    uvicorn.run(app, host="0.0.0.0", port=8088)