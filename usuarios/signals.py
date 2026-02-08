from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import Chain
from .models import Documentos


@receiver(post_save, sender=Documentos)
def post_save_documentos(sender, instance, created, **kwargs):
    if created:
        # IMPORT TARDIO (lazy import)
        from ia.tasks import ocr_and_markdown_file, rag_documentos

        chain = Chain()
        chain.append(ocr_and_markdown_file, instance.id)
        chain.append(rag_documentos, instance.id)
        chain.run()
