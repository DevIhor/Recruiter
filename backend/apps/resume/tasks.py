# import os
# import pytesseract
# from PIL import Image
# from config.celery import app
# from tempfile import TemporaryDirectory
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from apps.resume.models import CurriculumVitae
# from pdf2image import convert_from_path
# from django.conf import settings


# @receiver(post_save, sender=CurriculumVitae, dispatch_uid="start-ocr-process")
# def ocr_process(sender, instance, created, **kwargs):
#     """Runs an OCR process"""
#     print(f"Hello - {instance.processed_by_tesseract}")
#     if not instance.processed_by_tesseract:
#         run_ocr_task.delay(cv_path=instance.file.url, cv_id=instance.id)


# @app.task(bind=True, default_retry_delay=1 * 60)
# def run_ocr_task(self, cv_path: str, cv_id: int):
#     """Reads content of the file"""

#     image_file_list = []
#     dir_name = os.path.dirname(cv_path)
#     file_path = os.path.join(settings.BASE_DIR, cv_path)

#     with TemporaryDirectory() as tempdir:
#         pdf_pages = convert_from_path(file_path, 500)

#         for page_num, page in enumerate(pdf_pages, start=1):
#             filename = f"{tempdir}\page_{page_num:03}.jpg"
#             page.save(filename, "JPEG")
#             image_file_list.append(filename)

#     with open(os.path.join(dir_name, "text.txt"), "a") as output_file:
#         for image_file in image_file_list:

#             text = str(((pytesseract.image_to_string(Image.open(image_file)))))
#             text = text.replace("-\n", "")

#             output_file.write(text)
