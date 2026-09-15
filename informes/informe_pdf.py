import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from informes.informe import Informe

class InformePDF(Informe):
    """
    Genera informes formateados en PDF utilizando ReportLab.
    """
    def generar(self, ruta_archivo: str) -> bool:
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)

            doc = SimpleDocTemplate(
                ruta_archivo,
                pagesize=letter,
                rightMargin=36,
                leftMargin=36,
                topMargin=36,
                bottomMargin=36
            )
            elementos = []
            estilos = getSampleStyleSheet()

            # Estilo del Título
            estilo_titulo = ParagraphStyle(
                'TituloPersonalizado',
                parent=estilos['Title'],
                fontName='Helvetica-Bold',
                fontSize=18,
                leading=22,
                textColor=colors.HexColor('#1E3A8A'),
                alignment=0
            )

            # Encabezado del documento
            elementos.append(Paragraph(f"<b>ECOTECH Solutions</b>", estilos['Normal']))
            elementos.append(Paragraph(f"<b>Reporte:</b> {self.titulo}", estilo_titulo))
            elementos.append(Paragraph(f"<b>Fecha de emisión:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", estilos['Italic']))
            elementos.append(Spacer(1, 15))

            if not self.datos:
                elementos.append(Paragraph("No hay información registrada para este informe.", estilos['Normal']))
            else:
                # Construir encabezados y filas de la tabla dinámicamente desde los diccionarios
                encabezados = list(self.datos[0].keys())
                tabla_datos = [encabezados]

                for item in self.datos:
                    fila = [str(item.get(col, '')) for col in encabezados]
                    tabla_datos.append(fila)

                # Definir tabla con formato profesional
                tabla = Table(tabla_datos, hAlign='LEFT')
                tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')])
                ]))
                elementos.append(tabla)

            doc.build(elementos)
            print(f"Informe PDF generado exitosamente en: {ruta_archivo}")
            return True

        except Exception as e:
            print(f"Error al generar el informe PDF: {e}")
            return False