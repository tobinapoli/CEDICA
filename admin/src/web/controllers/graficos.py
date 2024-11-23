
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
import io
import plotly.express as px
import plotly.io as pio
import pandas as pd
from src.core.board.jinete_amazona import JineteAmazona
from src.web.handlers.auth import check_permission, login_required


bp = Blueprint("graficos", __name__, url_prefix="/graficos")


@bp.route("/", methods=['GET'])
@login_required
@check_permission("index_graficos")
def index():
    return render_template("graficos/index.html")

@bp.route('/graficos', methods=['GET'])
@login_required
@check_permission("view_graficos")
def graficos():
    
    graph_html = grafico_bar_chart_gente_por_provincia(config=config_propuesta)
    graph_html2 = grafico_pie_chart_discapacidad(config=config_discapacidad)
    graph_html3 = grafico_bar_becado(config=config_becado)

    return render_template('graficos/graficos/graficos.html', graph_html=graph_html, graph_html2=graph_html2, graph_html3=graph_html3)


def grafico_pie_chart_discapacidad(as_pdf = False, config=None):   
    conteos_tipo_discapacidad = JineteAmazona.contar_por_tipo_discapacidad()
    
    categorias2 = [categoria.value for categoria in conteos_tipo_discapacidad.keys() if categoria is not None]
    cantidades2 = list(conteos_tipo_discapacidad.values())
    fig = px.pie(names=categorias2, values=cantidades2, title='Distribución de Discapacidades')
    
    if as_pdf:
        return fig  
    graph_html = pio.to_html(fig, full_html=False, config=config)
    return graph_html


def grafico_bar_chart_gente_por_provincia(as_pdf=False, config=None):
    conteos_propuestas = JineteAmazona.contar_por_provincia()


    categorias = [
        provincia.nombre if hasattr(provincia, 'nombre') 
        else str(provincia).split('.')[-1].replace('_', ' ').title() 
        for provincia, _ in conteos_propuestas
    ]
    cantidades = [cantidad for _, cantidad in conteos_propuestas]

    if not categorias or not cantidades:
        fig = px.bar(
            x=['Sin datos disponibles'], 
            y=[0],
            labels={'x': 'Provincia', 'y': 'Número de Jinete Amazonas'},
            title='No hay datos para mostrar'
        )
        fig.update_layout(
            yaxis_title='Número de Jinete Amazonas',
            xaxis_title='Provincia',
            plot_bgcolor='white',
            showlegend=False
        )
        if as_pdf:
            return fig
        return pio.to_html(fig, full_html=False, config=config)


    data = pd.DataFrame({
        'Provincia': categorias,
        'Número de Jinete Amazonas': cantidades
    })


    fig = px.bar(
        data, 
        x='Provincia', 
        y='Número de Jinete Amazonas',
        title='Ranking de Provincias con más Jinetes y Amazonas'
    )
    fig.update_layout(
        yaxis_title='Número de Jinete Amazonas',
        xaxis_title='Provincia',
        plot_bgcolor='white',
        showlegend=False
    )
    fig.update_yaxes(tick0=0, dtick=1)  


    if as_pdf:
        return fig
    graph_html = pio.to_html(fig, full_html=False, config=config)
    return graph_html

def grafico_bar_becado(as_pdf = False, config=None):
    becados = JineteAmazona.contar_por_becados()
    no_becados = JineteAmazona.contar_por_no_becados()
    fig = px.bar(x=['Becados', 'No Becados'], y=[becados, no_becados], title='Distribución de Becados')
    fig.update_yaxes(tick0=0, dtick=1)
    fig.update_layout(
        dragmode='pan',
        xaxis=dict(
            fixedrange=True
        ),
        yaxis=dict(
            fixedrange=True
        )
    )
    if as_pdf:
        return fig  
    graph_html = pio.to_html(fig, full_html=False, config=config)   
    return graph_html

# Descargar a PDF

@bp.get('/download/propuesta')
@login_required
@check_permission("view_graficos")
def download_propuesta_pdf():
    fig = grafico_bar_chart_gente_por_provincia(as_pdf = True)
    buffer = io.BytesIO()
    fig.write_image(buffer, format="pdf")
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="propuesta_trabajo.pdf", mimetype="application/pdf")

@bp.get('/download/discapacidad')
@login_required
@check_permission("view_graficos")
def download_discapacidad_pdf():
    fig = grafico_pie_chart_discapacidad(as_pdf = True)
    buffer = io.BytesIO()
    fig.write_image(buffer, format="pdf")
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="discapacidad.pdf", mimetype="application/pdf")

@bp.get('/download/becados')
@login_required
@check_permission("view_graficos")
def download_becados_pdf():
    fig = grafico_bar_becado(as_pdf = True)
    buffer = io.BytesIO()
    fig.write_image(buffer, format="pdf")
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="becados.pdf", mimetype="application/pdf")


config_discapacidad = {"displayModeBar": True, "displaylogo": False, "responsive": True}
config_propuesta = {"displayModeBar": False, "displaylogo": False, "responsive": True}
config_becado = {"displayModeBar": False, "displaylogo": False, "responsive": True}