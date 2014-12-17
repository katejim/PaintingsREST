from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, JSONPRenderer, XMLRenderer, TemplateHTMLRenderer
from Application.Paintings.models import Pictures
from rest_framework.response import Response
from Application.Paintings.serializer import AllPicturesSerializer
from rest_framework import renderers

class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        print(type(data))
        return data


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def PictureViewSet(request, format=None):
    queryset = Pictures.objects.all()
    content = AllPicturesSerializer(queryset, many=True)
    if request.accepted_renderer.format == 'html':
        return Response({'pictures': content.data }, template_name='pictures.html')
    return Response(content.data)
