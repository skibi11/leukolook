# LeukoLook

An AI-powered web application that analyzes pediatric eye photos to detect early signs of leukocoria — an accessible screening tool for parents and guardians.

## Repository Structure

```
leukolook/
├── frontend/   # Vue 3 + TypeScript + Vite (deployed on Vercel)
├── backend/    # Django REST Framework API Gateway (deployed on Render)
├── api/        # FastAPI computer vision inference service (hosted on Hugging Face Spaces)
└── model/      # Trained MobileNetV1 model weights (hosted on Hugging Face Hub)
```

## Tech Stack

- **Frontend**: Vue 3, TypeScript, Vite
- **Backend**: Django REST Framework, MySQL, JWT Auth
- **AI Service**: FastAPI, TensorFlow/Keras, Roboflow, OpenCV
- **Deployment**: Vercel (frontend), Render (backend), Hugging Face (api + model)

## Deployment

Each service is deployed independently:

| Service | Platform | Root Directory |
|---------|----------|----------------|
| Frontend | Vercel | `frontend/` |
| Backend | Render | `backend/` |
| AI API | Hugging Face Spaces | `api/` |
| Model | Hugging Face Hub | `model/` |
