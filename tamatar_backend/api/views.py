import os
import uuid
from PIL import Image, UnidentifiedImageError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
from .ml.predictor import predict_image

ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png']

def is_valid_image(file):
    """Validate uploaded file is an image.

    This checks both the file extension and attempts to open/verify
    the file using Pillow. If Pillow cannot identify or verify the
    image, the function returns False.
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False

    try:
        img = Image.open(file)
        img.verify()
    except (UnidentifiedImageError, OSError):
        return False
    finally:
        try:
            file.seek(0)
        except Exception:
            pass

    return True


@api_view(['POST'])
def predict(request):
    if 'image' not in request.FILES:
        return Response(
            {"error": "No image provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    image = request.FILES['image']

    default_limit = 5 * 1024 * 1024 # 5 MB max upload
    max_size = getattr(settings, 'MAX_IMAGE_UPLOAD_SIZE', None)
    if max_size is None:
        max_size = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', None) or default_limit

    if image.size > max_size:
        return Response(
            {"error": "Uploaded file is too large", "max_size_bytes": max_size},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file type
    if not is_valid_image(image):
        return Response(
            {"error": "Invalid file type. Only JPG, JPEG, PNG allowed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Save temporarily
    ext = os.path.splitext(image.name)[1].lower()
    safe_name = f"{uuid.uuid4().hex}{ext}"
    file_path = default_storage.save(os.path.join('temp', safe_name), image)

    try:
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        try:
            response_data = predict_image(full_path)
        except Exception as e:
            return Response(
                {"error": "Internal server error while processing image"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(response_data, status=status.HTTP_200_OK)
    finally:
        # attempt to remove the temporary file (ignore deletion errors)
        try:
            default_storage.delete(file_path)
        except Exception:
            pass
