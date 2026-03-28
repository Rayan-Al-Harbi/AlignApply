from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from api.schemas import AnalyzeRequest, AnalyzeResponse
from api.utils import build_response, extract_text_from_file
from graph import app as app_graph

app = FastAPI(
    title="Job Application Intelligence",
    version="0.1.0",
)


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_application(request: AnalyzeRequest):
    try:
        initial_state = {
            "job_description": request.job_description,
            "cv_text": request.cv_text,
        }

        final_state = app_graph.invoke(initial_state)

        return build_response(final_state)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_with_upload(
    job_description: str = Form(...),
    cv_file: UploadFile = File(...),
):
    cv_text = await extract_text_from_file(cv_file)

    if not cv_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the uploaded file.",
        )

    initial_state = {
        "job_description": job_description,
        "cv_text": cv_text,
    }

    final_state = app_graph.invoke(initial_state)
    return build_response(final_state)