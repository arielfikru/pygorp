from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PyGoRP AI Service",
    description="AI/ML service for PyGoRP application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TextAnalysisRequest(BaseModel):
    text: str
    analysis_type: str = "sentiment"  # sentiment, keywords, summary
    options: Optional[Dict[str, Any]] = None

class ImageAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    image_data: Optional[str] = None  # base64 encoded
    analysis_type: str = "classification"

class MLModelRequest(BaseModel):
    model_name: str
    input_data: Dict[str, Any]
    parameters: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    request_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None

# Mock AI functions (replace with actual ML models)
async def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Mock sentiment analysis"""
    await asyncio.sleep(0.5)  # Simulate processing time

    # Simple mock logic
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor"]

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.9, 0.5 + (positive_count * 0.1))
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.9, 0.5 + (negative_count * 0.1))
    else:
        sentiment = "neutral"
        confidence = 0.6

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "scores": {
            "positive": positive_count / max(len(text.split()), 1),
            "negative": negative_count / max(len(text.split()), 1),
            "neutral": 1 - (positive_count + negative_count) / max(len(text.split()), 1)
        }
    }

async def extract_keywords(text: str, max_keywords: int = 5) -> Dict[str, Any]:
    """Mock keyword extraction"""
    await asyncio.sleep(0.3)

    # Simple mock keyword extraction
    words = text.lower().split()
    word_freq = {}

    for word in words:
        if len(word) > 3:  # Only consider words longer than 3 characters
            word_freq[word] = word_freq.get(word, 0) + 1

    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:max_keywords]

    return {
        "keywords": [word for word, freq in keywords],
        "frequencies": {word: freq for word, freq in keywords}
    }

async def generate_summary(text: str, max_length: int = 100) -> Dict[str, Any]:
    """Mock text summarization"""
    await asyncio.sleep(0.8)

    words = text.split()
    if len(words) <= max_length:
        summary = text
    else:
        summary = " ".join(words[:max_length]) + "..."

    return {
        "summary": summary,
        "original_length": len(words),
        "summary_length": len(summary.split()),
        "compression_ratio": len(summary.split()) / len(words)
    }

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pygorp-ai-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/analyze/text", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest, background_tasks: BackgroundTasks):
    """Analyze text using various AI models"""
    request_id = f"text_{datetime.utcnow().timestamp()}"
    start_time = datetime.utcnow()

    try:
        if request.analysis_type == "sentiment":
            result = await analyze_sentiment(request.text)
        elif request.analysis_type == "keywords":
            result = await extract_keywords(request.text)
        elif request.analysis_type == "summary":
            result = await generate_summary(request.text)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported analysis type: {request.analysis_type}")

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        return AnalysisResponse(
            request_id=request_id,
            status="completed",
            result=result,
            confidence=result.get("confidence"),
            processing_time=processing_time
        )

    except Exception as e:
        logger.error(f"Error processing text analysis: {str(e)}")
        return AnalysisResponse(
            request_id=request_id,
            status="failed",
            error=str(e)
        )

@app.post("/api/v1/analyze/image", response_model=AnalysisResponse)
async def analyze_image(request: ImageAnalysisRequest):
    """Analyze images using computer vision models"""
    request_id = f"image_{datetime.utcnow().timestamp()}"
    start_time = datetime.utcnow()

    try:
        # Mock image analysis
        await asyncio.sleep(1.0)

        if request.analysis_type == "classification":
            result = {
                "predictions": [
                    {"label": "cat", "confidence": 0.85},
                    {"label": "animal", "confidence": 0.92},
                    {"label": "pet", "confidence": 0.78}
                ],
                "dominant_color": "#8B4513",
                "image_quality": "high"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported analysis type: {request.analysis_type}")

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        return AnalysisResponse(
            request_id=request_id,
            status="completed",
            result=result,
            confidence=0.85,
            processing_time=processing_time
        )

    except Exception as e:
        logger.error(f"Error processing image analysis: {str(e)}")
        return AnalysisResponse(
            request_id=request_id,
            status="failed",
            error=str(e)
        )

@app.post("/api/v1/ml/predict", response_model=AnalysisResponse)
async def ml_prediction(request: MLModelRequest):
    """Make predictions using trained ML models"""
    request_id = f"ml_{datetime.utcnow().timestamp()}"
    start_time = datetime.utcnow()

    try:
        # Mock ML prediction
        await asyncio.sleep(0.7)

        # Simulate different model behaviors
        if request.model_name == "regression":
            result = {
                "prediction": 42.5,
                "feature_importance": {
                    "feature1": 0.3,
                    "feature2": 0.25,
                    "feature3": 0.45
                }
            }
        elif request.model_name == "classification":
            result = {
                "prediction": "class_A",
                "probabilities": {
                    "class_A": 0.7,
                    "class_B": 0.2,
                    "class_C": 0.1
                }
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unknown model: {request.model_name}")

        processing_time = (datetime.utcnow() - start_time).total_seconds()

        return AnalysisResponse(
            request_id=request_id,
            status="completed",
            result=result,
            confidence=0.8,
            processing_time=processing_time
        )

    except Exception as e:
        logger.error(f"Error processing ML prediction: {str(e)}")
        return AnalysisResponse(
            request_id=request_id,
            status="failed",
            error=str(e)
        )

@app.get("/api/v1/models")
async def list_models():
    """List available ML models"""
    return {
        "models": [
            {
                "name": "sentiment_analyzer",
                "type": "text_analysis",
                "description": "Analyzes sentiment in text"
            },
            {
                "name": "keyword_extractor",
                "type": "text_analysis",
                "description": "Extracts keywords from text"
            },
            {
                "name": "image_classifier",
                "type": "computer_vision",
                "description": "Classifies images"
            },
            {
                "name": "regression_model",
                "type": "regression",
                "description": "Predicts continuous values"
            },
            {
                "name": "classification_model",
                "type": "classification",
                "description": "Predicts categorical values"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting PyGoRP AI Service on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
