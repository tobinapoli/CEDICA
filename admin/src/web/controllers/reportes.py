
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
import plotly
import plotly.express as px
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from flask import make_response
from src.core.board.cobro import cobro
from src.web.handlers.auth import check_permission, login_required
from collections import Counter
from datetime import datetime
from src.web.controllers.form.reportForm import reportForm
from src.core.board.jinete_amazona import JineteAmazona



bp = Blueprint("reportes", __name__, url_prefix="/reportes")


@bp.route('/reportes', methods=['GET'])

@login_required
@check_permission("index_reportes")
def index_reportes():
    return render_template('graficos/reportes/index.html')

@bp.route('/reportes_cobros', methods=['GET', 'POST'])

@login_required
@check_permission("view_reportes")
def reportes_cobro():
    form = reportForm()
    report_data = []
    grafico = None
    
    if request.method == 'POST' and form.validate_on_submit():
        fecha_inicio_input = form.fecha_inicio.data
        fecha_fin_input = form.fecha_fin.data
        jinete_nombre = form.jinete_nombre.data
        jinete_dni = form.jinete_dni.data
        

        cobros = cobro.get_cobros(fecha_inicio_input, fecha_fin_input, jinete_nombre, jinete_dni)

        if not cobros:
            flash('No se encontraron cobros para las fechas seleccionadas.', 'warning')
            return render_template('graficos/reportes/reportes.html', report_data=[], grafico=None, form=form)
        
        total_monto = sum(cobro_data.monto for cobro_data in cobros)
        medios_de_pago = [cobro_data.medio_de_pago for cobro_data in cobros]
        
        medio_de_pago_counter = Counter(medios_de_pago)
        
        fig = px.bar(
            x=list(medio_de_pago_counter.keys()),
            y=list(medio_de_pago_counter.values()),
            labels={'x': 'Medio de Pago', 'y': 'Cantidad de Usos'},
            title="Medio de Pago Más Utilizado"
        )
        grafico = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        report_data = []
        for cobro_data in cobros:
            cobro_item = {
                'fecha': cobro_data.fecha,
                'monto': cobro_data.monto,
                'medio_de_pago': cobro_data.medio_de_pago,
                'empleado': cobro_data.empleado_id,
                'nombre_jinete': f"{cobro_data.jinete_amazona.nombre} {cobro_data.jinete_amazona.apellido}",
                'dni_jinete': cobro_data.jinete_amazona.dni,
                'observaciones': cobro_data.observaciones
            }
            report_data.append(cobro_item)

        return render_template(
            'graficos/reportes/reportes.html', 
            report_data=report_data, 
            total_monto=total_monto,
            grafico=grafico,
            form=form
        )
    
    return render_template('graficos/reportes/reportes.html', report_data=[], grafico=None, form=form)
    

@bp.route('/reportes_deudores', methods=['GET'])
@login_required
@check_permission("view_reportes")
def reporte_deudores():

    report_data = []
    deudores = JineteAmazona.get_deudores()  
    
    report_data = []
    for jinete in deudores:
        jinete_item = {
            'nombre': f"{jinete.nombre} {jinete.apellido}",
            'dni': jinete.dni,

        }
        report_data.append(jinete_item)

    return render_template(
        'graficos/reportes/reportes_deudores.html', 
        report_data=report_data
    )



@bp.route('/reportes_deudores_pdf', methods=['GET', 'POST'])
@login_required
@check_permission("view_reportes")
def reportes_deudores_pdf():


    report_data = []
    deudores = JineteAmazona.get_deudores()  


    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    
    pdf.setTitle("Reporte de Deudores")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, 800, "Reporte de Deudores")
    pdf.setFont("Helvetica", 12)

    y = 750
    pdf.drawString(150, y, "Nombre")
    pdf.drawString(350, y, "DNI")
    y -= 20

    for jinete in deudores:
        pdf.drawString(150, y, f"{jinete.nombre} {jinete.apellido}")  
        pdf.drawString(350, y, str(jinete.dni))
        y -= 20

    pdf.save()
    pdf_buffer.seek(0)

    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_deudores.pdf'

    return response


@bp.route('/reporte_propuestas', methods=['GET'])
@login_required
@check_permission("view_reportes")
def reporte_propuestas():

    data = JineteAmazona.contar_propuesta_trabajo()
    return render_template('graficos/reportes/reporte_propuestas.html', data=data)


@bp.route('/reporte_propuestas_pdf', methods=['GET'])
@login_required
@check_permission("view_reportes")
def reporte_propuestas_pdf():

    data = JineteAmazona.contar_propuesta_trabajo()
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    
    pdf.setTitle("Reporte de Propuestas de Trabajo")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, 800, "Reporte de Propuestas de Trabajo")
    pdf.setFont("Helvetica", 12)


    y = 750
    pdf.drawString(50, y, "Puesto")
    pdf.drawString(150, y, "Propuesta")
    pdf.drawString(350, y, "Total Solicitudes")
    y -= 20


    puesto = 1
    for propuesta, total in data:
        pdf.drawString(50, y, str(puesto))
        pdf.drawString(150, y, propuesta.value)  
        pdf.drawString(350, y, str(total))
        puesto += 1
        y -= 20

    pdf.save()
    pdf_buffer.seek(0)

    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_propuestas.pdf'

    return response