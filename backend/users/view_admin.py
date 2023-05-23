from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Documents
from users.serializer import DocumentSerializer, DocumentDetailSerializer


class DocumentsList(ListAPIView):
    queryset = Documents.objects.all().order_by("-created_at")
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated]


class DocumentsDetail(RetrieveAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated]


class ChangeDocumentVerdict(APIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = request.data.get("pk")
        reason = request.data.get("reason", "")
        action = request.data.get("action")

        documents = Documents.objects.get(pk=pk)
        documents.notes = reason
        documents.status = 1 if action == 1 else 2 # 1 == accepted, 2 == rejected
        documents.save()

        if action == 1:
            user = documents.user
            user.verified = True
            user.save()

        return Response(DocumentDetailSerializer(documents, context=self.get_renderer_context()).data)
