import fastapi
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import paper_array_generator

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEYS =["Jhealoj1nVqjU5K95KylKySUg0fdOOJ-8XhrMmf6ogZGbPU0x_jAaFTrAAlxx_yL_2eYMHVhw_JtGGhMf8M3jSzC-2s5I7GAY2QVI1xRhVLwjtz5R1QI42vp6LtinZe8"]

@app.post("/generate_paper")
def generate_paper(data: dict):

    if data["API_KEY"] not in API_KEYS:
        raise fastapi.HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    else:
        pdf = paper_array_generator.generate_paper_array({
            "MARKS": data["MARKS"],
            "DIFFICULTY": data["DIFFICULTY"]
        })

        return Response(
            content=pdf,
            media_type="application/pdf"
        )