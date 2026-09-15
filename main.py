#Incluye un menú interactivo en consola que permite gestionar empleados, gerentes,
#departamentos, proyectos y registros de tiempo interactuando directamente 
#con todas las clases creadas.

import sys
from modelos import Usuario, Empleado, Gerente, Departamento, Proyecto, RegistroTiempo, guardar_datos, cargar_datos

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


def solicitar_numero(mensaje: str, tipo=float, minimo=None):
    while True:
        try:
            valor = tipo(input(mensaje))
            if minimo is not None and valor <= minimo:
                raise ValueError
            return valor
        except ValueError:
            if minimo is None:
                print("Entrada no válida. Ingrese un número.")
            else:
                print(f"Entrada no válida. Ingrese un número mayor que {minimo}.")


def solicitar_confirmacion(mensaje):
    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().casefold()
        if respuesta in ("s", "n"):
            return respuesta
        print("Respuesta no válida. Escriba 's' para sí o 'n' para no.")


def registrar_empleado_o_gerente():
    global id_usuario_seq
    print("\n--- REGISTRAR EMPLEADO / GERENTE ---")
    print("1. Empleado General\n2. Gerente")
    tipo = input("Selecciona tipo (1/2): ").strip()
    if tipo not in ("1", "2"):
        print("Opción inválida.")
        return

    nombre = input("Nombre completo: ").strip()
    while True:
        email = input("Correo electrónico: ").strip()
        if Usuario.PATRON_EMAIL.fullmatch(email.lower()):
            break
        print("Correo inválido. Ingrese un correo con formato correcto, por ejemplo usuario@dominio.com.")
    tarifa = solicitar_numero("Tarifa por hora ($): ", float, minimo=0)

    if tipo == "1":
        cargo = input("Cargo / Puesto: ").strip()
        nuevo = Empleado(id_usuario_seq, nombre, email, cargo, tarifa)
        empleados.append(nuevo)
    else:
        bono = solicitar_numero("Bono de liderazgo ($): ", float, minimo=0)
        nuevo = Gerente(id_usuario_seq, nombre, email, tarifa_hora=tarifa, bono_liderazgo=bono)
        empleados.append(nuevo)

    id_usuario_seq += 1
    auto_guardar()
    print(f"[{nombre}] registrado con éxito.")


def solicitar_nombre_departamento():
    """Permite reutilizar un departamento existente o introducir uno nuevo."""
    if departamentos:
        print("\nDepartamentos existentes:")
        for idx, departamento in enumerate(departamentos, 1):
            print(f"{idx}. {departamento.nombre}")
        print("0. Crear un departamento nuevo")

        while True:
            opcion = input("Selecciona un departamento o 0 para crear uno: ").strip()
            if opcion == "0":
                break
            try:
                indice = int(opcion) - 1
            except ValueError:
                indice = -1
            if 0 <= indice < len(departamentos):
                print(f"El departamento '{departamentos[indice].nombre}' ya existe.")
                return None
            print("Opción inválida. Seleccione un departamento de la lista o 0.")

    while True:
        nombre = input("Nombre del departamento: ").strip()
        if not nombre:
            print("El nombre del departamento no puede estar vacío.")
            continue
        if len(nombre) > 100:
            print("El nombre del departamento no puede superar 100 caracteres.")
            continue
        if any(nombre.casefold() == departamento.nombre.casefold() for departamento in departamentos):
            print("Ese departamento ya existe. Selecciónelo de la lista.")
            continue
        return nombre


def crear_departamento():
    global id_depto_seq
    print("\n--- CREAR DEPARTAMENTO ---")
    nombre = solicitar_nombre_departamento()
    if nombre is None:
        return

    gerentes_disponibles = [e for e in empleados if isinstance(e, Gerente)]
    gerente_asignado = None

    if gerentes_disponibles:
        for idx, g in enumerate(gerentes_disponibles, 1):
            print(f"{idx}. {g.nombre}")
        asignar_gerente = solicitar_confirmacion("¿Asignar gerente?")

        if asignar_gerente == "s":
            while gerente_asignado is None:
                idx_g = solicitar_numero("Número de gerente: ", int) - 1
                if 0 <= idx_g < len(gerentes_disponibles):
                    gerente_asignado = gerentes_disponibles[idx_g]
                else:
                    print("Número de gerente inválido.")

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


def seleccionar_elemento(elementos, mensaje):
    """Devuelve el elemento seleccionado o None si no hay elementos."""
    if not elementos:
        print("No hay elementos registrados.")
        return None
    for indice, elemento in enumerate(elementos, 1):
        print(f"{indice}. {elemento}")
    while True:
        opcion = input(mensaje).strip()
        try:
            indice = int(opcion) - 1
        except ValueError:
            indice = -1
        if 0 <= indice < len(elementos):
            return elementos[indice]
        print("Opción inválida.")


def modificar_empleado():
    empleado = seleccionar_elemento(empleados, "Número de empleado/gerente: ")
    if empleado is None:
        return

    nombre = input(f"Nombre [{empleado.nombre}]: ").strip()
    if nombre:
        empleado.nombre = nombre
    email = input(f"Correo [{empleado.email}]: ").strip()
    if email:
        while not Usuario.PATRON_EMAIL.fullmatch(email.lower()):
            print("Correo inválido. Intente nuevamente.")
            email = input("Correo: ").strip()
        empleado.email = email
    tarifa = input(f"Tarifa por hora [{empleado.tarifa_hora}]: ").strip()
    if tarifa:
        try:
            empleado.tarifa_hora = float(tarifa)
        except ValueError:
            print("Tarifa inválida; se conserva el valor anterior.")
    if isinstance(empleado, Gerente):
        bono = input(f"Bono de liderazgo [{empleado.bono_liderazgo}]: ").strip()
        if bono:
            try:
                empleado.bono_liderazgo = float(bono)
            except ValueError:
                print("Bono inválido; se conserva el valor anterior.")
    else:
        cargo = input(f"Cargo [{empleado.cargo}]: ").strip()
        if cargo:
            empleado.cargo = cargo
    auto_guardar()
    print("Empleado actualizado correctamente.")


def modificar_departamento():
    departamento = seleccionar_elemento(departamentos, "Número de departamento: ")
    if departamento is None:
        return
    nombre = input(f"Nombre [{departamento.nombre}]: ").strip()
    if nombre and not any(
        nombre.casefold() == otro.nombre.casefold() and otro is not departamento
        for otro in departamentos
    ):
        departamento.nombre = nombre
    elif nombre:
        print("Ese nombre ya pertenece a otro departamento.")
    auto_guardar()
    print("Departamento actualizado correctamente.")


def modificar_proyecto():
    proyecto = seleccionar_elemento(proyectos, "Número de proyecto: ")
    if proyecto is None:
        return
    nombre = input(f"Nombre [{proyecto.nombre}]: ").strip()
    if nombre:
        proyecto._nombre = nombre
    presupuesto = input(f"Presupuesto [{proyecto.presupuesto}]: ").strip()
    if presupuesto:
        try:
            proyecto.presupuesto = float(presupuesto)
        except ValueError:
            print("Presupuesto inválido; se conserva el valor anterior.")
    estado = input(f"Estado [{proyecto.estado}]: ").strip()
    if estado:
        proyecto.estado = estado
    auto_guardar()
    print("Proyecto actualizado correctamente.")


def modificar_registro():
    registro = seleccionar_elemento(registros_tiempo, "Número de registro: ")
    if registro is None:
        return
    horas = input(f"Horas trabajadas [{registro.horas_trabajadas}]: ").strip()
    if horas:
        try:
            registro.horas_trabajadas = float(horas)
        except ValueError:
            print("Horas inválidas; se conserva el valor anterior.")
    descripcion = input(f"Descripción [{registro._descripcion}]: ").strip()
    if descripcion:
        registro._descripcion = descripcion
    auto_guardar()
    print("Registro actualizado correctamente.")


def modificar_datos():
    print("\n--- MODIFICAR DATOS ---")
    print("1. Empleado / Gerente\n2. Departamento\n3. Proyecto\n4. Registro de tiempo")
    opcion = input("Selecciona una opción: ").strip()
    acciones = {
        "1": modificar_empleado,
        "2": modificar_departamento,
        "3": modificar_proyecto,
        "4": modificar_registro,
    }
    accion = acciones.get(opcion)
    if accion:
        accion()
    else:
        print("Opción inválida.")


def eliminar_datos():
    print("\n--- ELIMINAR DATOS ---")
    print("1. Empleado / Gerente\n2. Departamento\n3. Proyecto\n4. Registro de tiempo")
    opcion = input("Selecciona una opción: ").strip()
    colecciones = {"1": empleados, "2": departamentos, "3": proyectos, "4": registros_tiempo}
    coleccion = colecciones.get(opcion)
    if coleccion is None:
        print("Opción inválida.")
        return
    elemento = seleccionar_elemento(coleccion, "Número del elemento: ")
    if elemento is None:
        return
    confirmacion = solicitar_confirmacion(f"¿Confirmar eliminación de '{elemento}'?")
    if confirmacion == "n":
        print("Eliminación cancelada.")
        return

    coleccion.remove(elemento)
    if opcion == "1":
        for departamento in departamentos:
            departamento.remover_empleado(elemento.id_usuario)
            if departamento.gerente is elemento:
                departamento.gerente = None
        registros_tiempo[:] = [r for r in registros_tiempo if r.empleado is not elemento]
    elif opcion == "3":
        registros_tiempo[:] = [r for r in registros_tiempo if r.proyecto is not elemento]
    auto_guardar()
    print("Elemento eliminado correctamente.")


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
        print("6. Modificar datos")
        print("7. Eliminar datos")
        print("8. Salir")
        print("=" * 40)

        opcion = input("Selecciona una opción (1-8): ").strip()
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
            input("\nPresione Enter para volver al menú principal...")
        elif opcion == "6":
            modificar_datos()
        elif opcion == "7":
            eliminar_datos()
        elif opcion == "8":
            auto_guardar()
            print("\nDatos guardados en 'datos_ecotech.json'. ¡Hasta luego!")
            sys.exit()


if __name__ == "__main__":
    menu_principal()