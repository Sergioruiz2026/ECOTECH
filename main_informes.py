import os
from repositorios.proyecto_repository import ProyectoRepository
from repositorios.empleado_repository import EmpleadoRepository
from informes.informe_pdf import InformePDF
from informes.informe_excel import InformeExcel

def probar_generacion_informes():
    print("=== PROBANDO MÓDULO DE INFORMES (ECOTECH) ===")

    # 1. Instanciar repositorios
    repo_proyectos = ProyectoRepository()
    repo_empleados = EmpleadoRepository()

    # 2. Extraer datos reales desde la BD SQLite
    # (Para el reporte, convertimos los datos a diccionarios)
    proyectos = repo_proyectos.obtener_todos() if hasattr(repo_proyectos, 'obtener_todos') else []
    
    # En caso de no tener obtener_todos aún en el repo, preparamos datos de prueba/simulación
    datos_proyectos = [
        {
            "ID Proy": p.id_proyecto,
            "Nombre Proyecto": p.nombre,
            "Presupuesto ($)": f"{p.presupuesto:,.2f}",
            "Estado": p.estado
        }
        for p in proyectos
    ] if proyectos else [
        {"ID Proy": 1, "Nombre Proyecto": "Planta Solar Eco1", "Presupuesto ($)": "45,000.00", "Estado": "En Proceso"},
        {"ID Proy": 2, "Nombre Proyecto": "Auditoría Verde 2026", "Presupuesto ($)": "12,500.00", "Estado": "Completado"},
        {"ID Proy": 3, "Nombre Proyecto": "Eficiencia Hídrica", "Presupuesto ($)": "28,000.00", "Estado": "Planificado"}
    ]

    # Carpeta donde se guardarán los reportes
    carpeta_salida = "salida_reportes"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # 3. Generar Informe en PDF
    ruta_pdf = os.path.join(carpeta_salida, "Reporte_Proyectos_ECOTECH.pdf")
    informe_pdf = InformePDF(titulo="Consolidado General de Proyectos", datos=datos_proyectos)
    exito_pdf = informe_pdf.generar(ruta_pdf)

    # 4. Generar Informe en Excel
    ruta_excel = os.path.join(carpeta_salida, "Reporte_Proyectos_ECOTECH.xlsx")
    informe_excel = InformeExcel(titulo="Consolidado General de Proyectos", datos=datos_proyectos)
    exito_excel = informe_excel.generar(ruta_excel)

    # Resumen de resultados
    if exito_pdf and exito_excel:
        print("\n¡Prueba exitosa! Revisa la carpeta 'salida_reportes/' en la raíz de tu proyecto.")
    else:
        print("\nHubo un problema al generar alguno de los informes.")

if __name__ == "__main__":
    probar_generacion_informes()