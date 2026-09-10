import json
import os
from typing import List, Dict, Tuple
from modelos import Empleado, Gerente, Departamento, Proyecto, RegistroTiempo

ARCHIVO_DATOS = "datos_ecotech.json"

def guardar_datos(empleados: List, departamentos: List, proyectos: List, registros_tiempo: List):
    """Serializa las listas de objetos y las guarda en un archivo JSON."""
    datos = {
        "empleados": [],
        "departamentos": [],
        "proyectos": [],
        "registros_tiempo": []
    }

    # Serializar Empleados y Gerentes
    for emp in empleados:
        es_gerente = isinstance(emp, Gerente)
        d_emp = {
            "tipo": "gerente" if es_gerente else "empleado",
            "id_usuario": emp.id_usuario,
            "nombre": emp.nombre,
            "email": emp.email,
            "tarifa_hora": emp.tarifa_hora,
            "cargo": getattr(emp, "cargo", "Empleado")
        }
        if es_gerente:
            d_emp["bono_liderazgo"] = emp.bono_liderazgo
        datos["empleados"].append(d_emp)

    # Serializar Departamentos
    for dept in departamentos:
        datos["departamentos"].append({
            "id_departamento": dept.id_departamento,
            "nombre": dept.nombre,
            "id_gerente": dept.gerente.id_usuario if dept.gerente else None,
            "ids_empleados": [e.id_usuario for e in dept.empleados]
        })

    # Serializar Proyectos
    for proy in proyectos:
        datos["proyectos"].append({
            "id_proyecto": proy.id_proyecto,
            "nombre": proy.nombre,
            "presupuesto": proy.presupuesto,
            "estado": proy.estado
        })

    # Serializar Registros de Tiempo
    for reg in registros_tiempo:
        datos["registros_tiempo"].append({
            "id_registro": reg.id_registro,
            "id_empleado": reg.empleado.id_usuario,
            "id_proyecto": reg.proyecto.id_proyecto,
            "horas_trabajadas": reg.horas_trabajadas,
            "fecha": reg._fecha,
            "descripcion": reg._descripcion
        })

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def cargar_datos() -> Tuple[List, List, List, List]:
    """Carga los datos desde el archivo JSON y reconstruye las instancias de objetos."""
    if not os.path.exists(ARCHIVO_DATOS):
        return [], [], [], []

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except Exception:
        return [], [], [], []

    empleados = []
    mapa_empleados: Dict[int, Empleado] = {}

    # Deserializar Empleados / Gerentes
    for d in datos.get("empleados", []):
        if d.get("tipo") == "gerente":
            emp = Gerente(d["id_usuario"], d["nombre"], d["email"], d["tarifa_hora"], d.get("bono_liderazgo", 0.0))
        else:
            emp = Empleado(d["id_usuario"], d["nombre"], d["email"], d["cargo"], d["tarifa_hora"])
        empleados.append(emp)
        mapa_empleados[emp.id_usuario] = emp

    # Deserializar Departamentos
    departamentos = []
    for d in datos.get("departamentos", []):
        gerente = mapa_empleados.get(d.get("id_gerente")) if d.get("id_gerente") is not None else None
        dept = Departamento(d["id_departamento"], d["nombre"], gerente)
        for id_emp in d.get("ids_empleados", []):
            if id_emp in mapa_empleados:
                dept.agregar_empleado(mapa_empleados[id_emp])
        departamentos.append(dept)

    # Deserializar Proyectos
    proyectos = []
    mapa_proyectos: Dict[int, Proyecto] = {}
    for d in datos.get("proyectos", []):
        proy = Proyecto(d["id_proyecto"], d["nombre"], d["presupuesto"], d.get("estado", "Planificación"))
        proyectos.append(proy)
        mapa_proyectos[proy.id_proyecto] = proy

    # Deserializar Registros de Tiempo
    registros_tiempo = []
    for d in datos.get("registros_tiempo", []):
        emp = mapa_empleados.get(d["id_empleado"])
        proy = mapa_proyectos.get(d["id_proyecto"])
        if emp and proy:
            proy.asignar_miembro(emp)
            reg = RegistroTiempo(d["id_registro"], emp, proy, d["horas_trabajadas"], d.get("fecha"), d.get("descripcion", ""))
            registros_tiempo.append(reg)

    return empleados, departamentos, proyectos, registros_tiempo