import sys
from modelos import Empleado, Gerente, Departamento, Proyecto, RegistroTiempo, guardar_datos, cargar_datos

# Cargar datos guardados previamente desde el archivo JSON
empleados, departamentos, proyectos, registros_tiempo = cargar_datos()

# Sincronizar secuencias de ID según el valor máximo existente
id_usuario_seq = max([e.id_usuario for e in empleados], default=0) + 1
id_depto_seq = max([d.id_departamento for d in departamentos], default=0) + 1
id_proyecto_seq = max([p.id_proyecto for p in proyectos], default=0) + 1
id_registro_seq = max([r.id_registro for r in registros_tiempo], default=0) + 1


def auto_guardar():
    """Guarda automáticamente el estado actual en JSON."""
    guardar_datos(empleados, departamentos, proyectos, registros_tiempo)


def solicitar_numero(mensaje: str, tipo=float):
    while True:
        try:
            return tipo(input(mensaje))
        except ValueError:
            print("Entrada no válida. Ingrese un número.")


def registrar_empleado_o_gerente():
    global id_usuario_seq
    print("\n--- REGISTRAR EMPLEADO / GERENTE ---")
    print("1. Empleado General\n2. Gerente")
    tipo = input("Selecciona tipo (1/2): ").strip()

    nombre = input("Nombre completo: ").strip()
    email = input("Correo electrónico: ").strip()
    tarifa = solicitar_numero("Tarifa por hora ($): ", float)

    if tipo == "1":
        cargo = input("Cargo / Puesto: ").strip()
        nuevo = Empleado(id_usuario_seq, nombre, email, cargo, tarifa)
        empleados.append(nuevo)
    elif tipo == "2":
        bono = solicitar_numero("Bono de liderazgo ($): ", float)
        nuevo = Gerente(id_usuario_seq, nombre, email, tarifa_hora=tarifa, bono_liderazgo=bono)
        empleados.append(nuevo)
    else:
        print("Opción inválida.")
        return

    id_usuario_seq += 1
    auto_guardar()
    print(f"[{nombre}] registrado con éxito.")


def crear_departamento():
    global id_depto_seq
    print("\n--- CREAR DEPARTAMENTO ---")
    nombre = input("Nombre del departamento: ").strip()
    gerentes_disponibles = [e for e in empleados if isinstance(e, Gerente)]
    gerente_asignado = None

    if gerentes_disponibles:
        for idx, g in enumerate(gerentes_disponibles, 1):
            print(f"{idx}. {g.nombre}")
        if input("¿Asignar gerente? (s/n): ").strip().lower() == "s":
            idx_g = solicitar_numero("Número de gerente: ", int) - 1
            if 0 <= idx_g < len(gerentes_disponibles):
                gerente_asignado = gerentes_disponibles[idx_g]

    nuevo_depto = Departamento(id_depto_seq, nombre, gerente_asignado)
    departamentos.append(nuevo_depto)
    id_depto_seq += 1
    auto_guardar()
    print(f"Departamento '{nombre}' creado.")


def crear_proyecto():
    global id_proyecto_seq
    print("\n--- CREAR PROYECTO ---")
    nombre = input("Nombre del proyecto: ").strip()
    presupuesto = solicitar_numero("Presupuesto ($): ", float)

    proyectos.append(Proyecto(id_proyecto_seq, nombre, presupuesto))
    id_proyecto_seq += 1
    auto_guardar()
    print(f"Proyecto '{nombre}' creado.")


def registrar_horas_trabajo():
    global id_registro_seq
    print("\n--- REGISTRAR TIEMPO DE TRABAJO ---")
    if not empleados or not proyectos:
        print("Requiere al menos un empleado y un proyecto registrados.")
        return

    for idx, e in enumerate(empleados, 1):
        print(f"{idx}. {e.nombre} ({e.cargo})")
    idx_emp = solicitar_numero("Número de empleado: ", int) - 1

    for idx, p in enumerate(proyectos, 1):
        print(f"{idx}. {p.nombre}")
    idx_proy = solicitar_numero("Número de proyecto: ", int) - 1

    if 0 <= idx_emp < len(empleados) and 0 <= idx_proy < len(proyectos):
        emp, proy = empleados[idx_emp], proyectos[idx_proy]
        horas = solicitar_numero("Horas trabajadas: ", float)
        desc = input("Descripción (opcional): ").strip()

        proy.asignar_miembro(emp)
        reg = RegistroTiempo(id_registro_seq, emp, proy, horas, descripcion=desc)
        registros_tiempo.append(reg)
        id_registro_seq += 1
        auto_guardar()
        print(f"Registro creado. Costo laboral: ${reg.calcular_costo_laboral():.2f}")


def listar_resumen_general():
    print("\n" + "=" * 50)
    print("             RESUMEN GENERAL - ECOTECH             ")
    print("=" * 50)
    print(f"\n--- EMPLEADOS ({len(empleados)}) ---")
    for e in empleados:
        print(f" • {e.obtener_detalles()}")
    print(f"\n--- DEPARTAMENTOS ({len(departamentos)}) ---")
    for d in departamentos:
        print(f" • {d.obtener_detalles()}")
    print(f"\n--- PROYECTOS ({len(proyectos)}) ---")
    for p in proyectos:
        print(f" • {p.obtener_detalles()}")
    print(f"\n--- REGISTROS DE TIEMPO ({len(registros_tiempo)}) ---")
    for r in registros_tiempo:
        print(f" • {r.obtener_detalles()}")
    print("=" * 50)


def menu_principal():
    while True:
        print("\n" + " SYSTEMA DE GESTIÓN ECOTECH ".center(40, "="))
        print("1. Registrar Empleado / Gerente")
        print("2. Crear Departamento")
        print("3. Crear Proyecto")
        print("4. Registrar Horas Trabajadas")
        print("5. Ver Resumen General del Sistema")
        print("6. Salir")
        print("=" * 40)

        opcion = input("Selecciona una opción (1-6): ").strip()
        if opcion == "1":
            registrar_empleado_o_gerente()
        elif opcion == "2":
            crear_departamento()
        elif opcion == "3":
            crear_proyecto()
        elif opcion == "4":
            registrar_horas_trabajo()
        elif opcion == "5":
            listar_resumen_general()
        elif opcion == "6":
            auto_guardar()
            print("\nDatos guardados en 'datos_ecotech.json'. ¡Hasta luego!")
            sys.exit()


if __name__ == "__main__":
    menu_principal()