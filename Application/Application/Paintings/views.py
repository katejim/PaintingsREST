import string
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
from django.shortcuts import Http404

from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        rez = ""
        for el in data:
            rez += "id: " + str(el['id']) + " name: " + el['name'] + " link: " + el['link'] + " type:" + el[
                'type'] + "\n"

        return rez


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
def TasksPUTViewSet(request, stringType, priceValue, format=None):
    queryset = get_list_or_404(Pictures.objects.filter(type=stringType).filter(price__gte=priceValue))
    serializer = AllPicturesSerializer(queryset, data=request.data, many=True)
    if serializer.is_valid():
        tasks[len(tasks)] = serializer.data
        if request.accepted_renderer.format == 'html':
            return Response({'id': len(tasks) - 1, 'price': priceValue, 'type': stringType, 'action': 'added'},
                            template_name='tasksModify.html')
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def TasksPOSTViewSet(request, taskID, stringType, priceValue, format=None):
    # check existence of task
    queryset = tasks.get(int('0' + taskID))
    if queryset == None:
        if request.accepted_renderer.format == 'html':
            return Response(status=status.HTTP_400_BAD_REQUEST, template_name='tasksModify.html')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    queryset = get_list_or_404(Pictures.objects.filter(type=stringType).filter(price__gte=priceValue))
    serializer = AllPicturesSerializer(queryset, data=request.data, many=True)
    if serializer.is_valid():
        tasks[int('0' + taskID)] = serializer.data
        if request.accepted_renderer.format == 'html':
            return Response({'id': taskID, 'price': priceValue, 'type': stringType, 'action': 'updated'},
                            template_name='tasksModify.html')
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def TasksDELETEViewSet(request, taskID, format=None):
    queryset = tasks.get(int('0' + taskID))
    if queryset == None:
        if request.accepted_renderer.format == 'html':
            return Response(status=status.HTTP_400_BAD_REQUEST, template_name='tasksModify.html')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    del tasks[int('0' + taskID)]
    if request.accepted_renderer.format == 'html':
        return Response({'id': taskID}, template_name='tasksDelete.html')
    return Response(queryset)


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer, PlainTextRenderer))
def AllTasksViewSet(request, format=None):
    return Response({'tasks': tasks}, template_name='tasks.html')


def page_not_found_view(request):
    raise Http404