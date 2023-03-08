from django.shortcuts import render
from django.http import FileResponse
from rest_framework.views import APIView


class GenerateZIP(APIView):
    def post(self, request):
        pass

    def get(self, request):
        return FileResponse(
            open('/home/mahmoud/Downloads/riyadh_eval_datadropcsv.gz', 'rb'),
            as_attachment=True,
            filename='riyadh_eval_datadropcsv.gz'
        )



