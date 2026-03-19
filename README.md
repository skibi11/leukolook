# LeukoLook | AI-Powered Leukocoria Detection

An AI-powered web and mobile application designed to analyze pediatric eye photos and detect early signs of leukocoria, serving as an accessible screening tool for parents and guardians. 

![Vue.js](https://img.shields.io/badge/Vue.js-35495E?logo=vue.js&logoColor=4FC08D)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000)

## 📖 Overview
Early detection of leukocoria (an abnormal white reflection from the retina) is critical for pediatric eye health. LeukoLook bridges the gap between complex medical AI models and everyday accessibility. The application provides a dark-mode, intuitive interface that allows users to either upload existing gallery photos or use their device's camera for real-time analysis using custom-trained TensorFlow models.

*Note: This project was developed as an academic deliverable for the College of Computer Studies at Mindanao State University - Iligan Institute of Technology.*

## 🏗️ System Architecture & Tech Stack

The application is structured using a decoupled architecture to ensure seamless communication between the client interface, the backend routing, and the heavy machine-learning inference layer.

* **Frontend Client:** Built with **Vue 3** and **TypeScript** (via Vite) for a highly responsive, type-safe user interface.
* **Backend API:** Engineered with **Django REST Framework (DRF)** and **FastAPI** to handle complex routing, image preprocessing, and secure data transfer.
* **AI / Machine Learning:** Custom models developed using **TensorFlow/Keras** and **Roboflow**. 
* **Hosting & Deployment:** The frontend and backend are deployed via **Vercel** and **Render**, while the AI inference model is securely hosted on **Hugging Face Spaces** for optimized computational performance.

## 👨‍💻 My Contributions

As a Core Developer on this multidisciplinary academic team, my specific architectural responsibilities included:
1.  **Frontend Engineering:** Architecting and building the entire Vue 3 and TypeScript client-side interface, focusing on camera integration, file-handling UX, and responsive design.
2.  **Backend Logic:** Developing the core routing and data-handling logic within the Django application to bridge the user interface with the machine learning model.
3.  **Model Deployment:** Managing the infrastructure to extract the TensorFlow model and successfully host it on Hugging Face Spaces to expose a reliable inference endpoint.

## 🚀 Local Development Setup

To run this project locally, you will need Node.js and Python installed on your machine.

### 1. Frontend Setup (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

### 2. Backend Setup (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python manage.py runserver
```
