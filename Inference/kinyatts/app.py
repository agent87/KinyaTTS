from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse
from generator import Generator

# Setup the TTS engine once when the app starts
Generator.setup()

# FastAPI setup
app = FastAPI()

@app.post("/generate-audio/")
async def generate_audio(text: str = Form(...)):
    generator = Generator(text)
    if generator.response["status_code"] != 0:
        raise HTTPException(status_code=generator.response["status_code"], detail=generator.response["error"])
    return StreamingResponse(generator.audio_buffer, media_type="audio/wav")

# To run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)