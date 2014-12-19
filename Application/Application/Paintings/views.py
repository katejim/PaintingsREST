from django.core.context_processors import request
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, JSONPRenderer, XMLRenderer, TemplateHTMLRenderer
from Application.Paintings.models import Pictures
from rest_framework.response import Response
from Application.Paintings.serializer import AllPicturesSerializer
from rest_framework import renderers
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

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
        return Response({'pictures': content.data}, template_name='pictures.html')
    return Response(content.data)


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def PicturesTypedViewSet(request, stringType, format=None):
    queryset = get_list_or_404(Pictures.objects.filter(type=stringType))
    content = AllPicturesSerializer(queryset, many=True)
    if request.accepted_renderer.format == 'html':
        return Response({'pictures': content.data}, template_name='typed.html')
    return Response(content.data)


tasks = {}
@api_view(['PUT'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def TasksPUTViewSet(request, stringType, stringName, format=None):
    queryset = get_object_or_404(Pictures.objects.filter(type=stringType), name=stringName)
    serializer = AllPicturesSerializer(queryset, data=request.data)
    if serializer.is_valid():
        tasks[len(tasks)] = serializer.data
        if request.accepted_renderer.format == 'html':
            return Response({'id': len(tasks)-1, 'name': serializer.data['name'], 'type':serializer.data['type'],
                         'link':serializer.data['link'], 'action': 'added'}, template_name='tasksModify.html')
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def TasksPOSTViewSet(request, taskID, stringType, stringName, format=None):
    queryset = tasks.get(int('0' + taskID))
    if queryset == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    queryset['name'] = stringName
    queryset['type'] = stringType
    if request.accepted_renderer.format == 'html':
        return Response({'id': taskID, 'name':queryset['name'], 'type':queryset['type'],
                         'link':queryset['link'], 'action': 'updated'}, template_name='tasksModify.html')
    return Response(queryset)

@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def TasksDELETEViewSet(request, taskID, format=None):
    queryset = tasks.get(int('0' + taskID))
    if queryset == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    del tasks[int('0' + taskID)]
    if request.accepted_renderer.format == 'html':
        return Response({'id': taskID, 'name':queryset['name'], 'type':queryset['type'],
                         'link':queryset['link'], 'action': 'deleted'}, template_name='tasksModify.html')
    return Response(queryset)

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def AllTasksViewSet(request, format=None):
    return Response({'tasks': tasks}, template_name='tasks.html')
