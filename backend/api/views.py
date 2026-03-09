# in api/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

HF_PIPELINE_URL = "https://skibi11-leukolook-api.hf.space/detect/"

class EyeDetectionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # --- START OF CORRECTION ---

            # Create a dictionary for the files payload.
            # This tells the 'requests' library to send it as a multipart/form-data file upload.
            files = {'image': (image_file.name, image_file.read(), image_file.content_type)}

            # Send the file upload request to the Hugging Face Space
            # Note: We use the 'files=' parameter here, NOT 'json='
            response = requests.post(HF_PIPELINE_URL, files=files)
            
            # --- END OF CORRECTION ---

            response.raise_for_status()

            # Forward the final JSON result back to the frontend
            return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            # Handle errors from the Hugging Face service
            try:
              error_content = e.response.json()
            except:
              error_content = {"error": "The analysis service is currently unavailable."}
            return Response(error_content, status=status.HTTP_503_SERVICE_UNAVAILABLE)