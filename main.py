import sys
sys.path.append("./src/apis")
sys.path.append("./src/Models")
sys.path.append("./src/datalayer")
from phrase_api import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)