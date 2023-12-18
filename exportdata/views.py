from django.shortcuts import render, redirect
from django.http import HttpResponse
from .resources import PenerimaResource
from penerima.models import Penerima
from exportdata.filters import PenerimaFilter
from dtks.models import Bansos

from django.contrib.auth.decorators import login_required
from account.decorators import unauthenticated_user, allowed_users

import pandas as pd
from django_pandas.io import read_frame
import xlsxwriter
import pandas.io.formats.excel
import io
from datetime import datetime


@login_required(login_url='account:login')
@allowed_users(allowed_roles=['Superadmin', 'Admin'])
def index(request):
    penerima_filter=PenerimaFilter(request.POST, queryset=Penerima.objects.all())
    bansos = Bansos.objects.all()
    context={
        'title':'Export Data',
        'bansos':bansos,
        'form':penerima_filter.form,
    }
    return render(request, 'exportdata/index.html', context)

def export(request):
    penerima_resource = PenerimaResource()
    penerima_filter=PenerimaFilter(request.POST, queryset=Penerima.objects.all())
    queryset=penerima_filter.qs

    df = read_frame(queryset, fieldnames=['id', 'anggota__nama_art', 'bansos__nama_bansos', 'tahun', 'status'])
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # Even though the final file will be in memory the module uses temp
    # files during assembly for efficiency. To avoid this on servers that
    # don't allow temp files, for example the Google APP Engine, set the
    # 'in_memory' Workbook() constructor option as shown in the docs.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    bold.set_font_size(12)
    f1=workbook.add_format({'bold':True, 'border':2, 'border_color':'black'})
    f2=workbook.add_format({'border':1, 'border_color':'black'})
    # Adjust the column width.
    worksheet.set_column(1, 20, 20)

    worksheet.write('A1', 'DATA PENERIMA BANTUAN SOSIAL DARI DINSOSDALDUKKBP3A KABUPATEN PURBALINGGA', bold)
    headings = ('No', 'NIK', 'Nama Anggota', ' Jenis Bansos', 'Tahun', 'Status')
    worksheet.write_row('A3', headings, f1)
    # worksheet.write('A3', 'ID', f1)
    # worksheet.write('B3', 'NIK', f1)
    # worksheet.write('C3', 'Nama Anggota', f1)
    # worksheet.write('D3', 'Jenis Bansos', f1)
    # worksheet.write('E3', 'Tahun', f1)
    # worksheet.write('F3', 'Status', f1)
    f1=workbook.add_format({'bold':True, 'border':2, 'border_color':'black'})
    f2=workbook.add_format({'border':2, 'border_color':'black'})
    header1 = '&CDINSOSDALDUKKBP3A'
    footer1 = '&L&D &T &R&P'
    worksheet.set_landscape()
    worksheet.set_paper(9) #A4 paper
    worksheet.set_header(header1)
    worksheet.set_footer(footer1)
    data = []
    for d in queryset:
        data.append((d.anggota.nik, d.anggota.nama_art, d.bansos.nama_bansos, d.tahun, d.status, d.anggota.rumah.koordinat_lat, d.anggota.rumah.koordinat_long))


    # Write some test data.
    row = 3
    col = 0
    no = 1
    for nik, nama, bansos, tahun, status, lat, long in data:
        koordinat = lat+','+long
        # Convert the date string into a datetime object.
        worksheet.write (row, col, no, f2)
        worksheet.write (row, col + 1, nik, f2)
        worksheet.write (row, col + 2, nama, f2)
        worksheet.write (row, col + 3, bansos, f2)
        worksheet.write (row, col + 4, tahun, f2)
        worksheet.write (row, col + 5, status, f2)
        row += 1
        no += 1

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    # Set up the Http response.
    filename = "Data Penerima.xlsx"
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response

    # dataset = penerima_resource.export(queryset)
    # response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="Daftar Penerima.xls"'
    # return response
