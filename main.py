#Incluye un menú interactivo en consola que permite gestionar empleados, gerentes,
#departamentos, proyectos y registros de tiempo interactuando directamente 
#con todas las clases creadas.

import os
from datetime import datetime
from database.database import Database

# Importación de Modelos
from modelos.usuario import Usuario
from modelos.empleado import Empleado
from modelos.departamento import Departamento
from modelos.proyecto import Proyecto
from modelos.registro_tiempo import RegistroTiempo

# Importación de Repositorios
from repositorios.empleado_repository import EmpleadoRepository
from repositorios.departamento_repository import DepartamentoRepository
from repositorios.proyecto_repository import ProyectoRepository
from repositorios.registro_repository import RegistroTiempoRepository
from repositorios.usuario_repository import UsuarioRepository

# Importación del Módulo de Informes
from informes.informe_pdf import InformePDF
from informes.informe_excel import InformeExcel

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione ENTER para continuar...")

class MenuApp:
    def __init__(self):
        db = Database()
        db.inicializar_tablas()
        self.repo_usuario = UsuarioRepository(db)
        self.repo_empleado = EmpleadoRepository(db)
        self.repo_departamento = DepartamentoRepository(db)
        self.repo_proyecto = ProyectoRepository(db)
        self.repo_registro = RegistroTiempoRepository(db)
        self.usuario_actual = None  # Almacenará la sesión del usuario activo

    # ==========================================
    # PANTALLA INICIAL: AUTENTICACIÓN
    # ==========================================
    def iniciar_sistema(self):
        while True:
            limpiar_pantalla()
            print("==================================================")
            print("         ECOTECH SOLUTIONS - ACCESO               ")
            print("==================================================")
            print("1. Iniciar Sesión")
            print("2. Registrar Nuevo Usuario")
            print("0. Salir")
            print("--------------------------------------------------")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                if self.iniciar_sesion():
                    self.ejecutar_menu_principal()
            elif opcion == "2":
                self.registrar_usuario()
            elif opcion == "0":
                print("\n¡Gracias por utilizar el sistema de ECOTECH Solutions!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
                pausar()

    def iniciar_sesion(self) -> bool:
        limpiar_pantalla()
        print("--- INICIAR SESIÓN ---")
        email = input("Ingrese su correo electrónico registrado: ").strip()
        
        try:
            # Crear instancia temporal para aplicar la lógica de validación y cifrado
            user_temp = Usuario(0, "Temp", email)
            email_cifrado = user_temp.obtener_email_cifrado()

            # Consultar en la BD por el hash del correo
            conexion = self.repo_usuario.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_usuario, nombre, email FROM usuarios WHERE email = ?", (email_cifrado,))
            row = cursor.fetchone()
            conexion.close()

            if row:
                self.usuario_actual = Usuario(row[0], row[1], email)
                print(f"\n[ÉXITO] ¡Bienvenido(a), {self.usuario_actual.nombre}!")
                pausar()
                return True
            else:
                print("\n[ERROR] Correo electrónico no registrado o credenciales inválidas.")
                pausar()
                return False
        except ValueError as e:
            print(f"\n[ERROR DE VALIDACIÓN]: {e}")
            pausar()
            return False

    def registrar_usuario(self):
        limpiar_pantalla()
        print("--- REGISTRO DE NUEVO USUARIO ---")
        nombre = input("Nombre completo: ").strip()
        email = input("Correo electrónico: ").strip()

        try:
            nuevo_usuario = Usuario(0, nombre, email)
            if self.repo_usuario.crear(nuevo_usuario):
                print(f"\n[ÉXITO] Usuario registrado correctamente. Ya puede iniciar sesión.")
            else:
                print("\n[ERROR] No se pudo completar el registro en la base de datos.")
        except ValueError as e:
            print(f"\n[ERROR DE VALIDACIÓN]: {e}")
        pausar()

    # ==========================================
    # MENÚ PRINCIPAL DEL SISTEMA
    # ==========================================
    def ejecutar_menu_principal(self):
        while True:
            limpiar_pantalla()
            print("==================================================")
            print(f" ECOTECH SOLUTIONS | Usuario Activo: {self.usuario_actual.nombre}")
            print("==================================================")
            print("1. Gestión de Empleados")
            print("2. Gestión de Departamentos")
            print("3. Gestión de Proyectos")
            print("4. Registrar Horas de Trabajo (RegistroTiempo)")
            print("5. Exportar Informes (PDF / Excel)")
            print("0. Cerrar Sesión")
            print("--------------------------------------------------")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.menu_empleados()
            elif opcion == "2":
                self.menu_departamentos()
            elif opcion == "3":
                self.menu_proyectos()
            elif opcion == "4":
                self.menu_registro_tiempo()
            elif opcion == "5":
                self.menu_informes()
            elif opcion == "0":
                print(f"\nCerrando sesión de {self.usuario_actual.nombre}...")
                self.usuario_actual = None
                pausar()
                break
            else:
                print("Opción inválida. Intente nuevamente.")
                pausar()

    # ==========================================
    # 1. MENÚ EMPLEADOS
    # ==========================================
    def menu_empleados(self):
        while True:
            limpiar_pantalla()
            print("--- GESTIÓN DE EMPLEADOS ---")
            print("1. Registrar Empleado / Gerente")
            print("2. Buscar Empleado por ID")
            print("3. Actualizar Empleado")
            print("4. Eliminar Empleado")
            print("0. Volver al Menú Principal")
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                nombre = input("Nombre completo: ").strip()
                email = input("Correo electrónico: ").strip()
                cargo = input("Cargo: ").strip()
                try:
                    tarifa = float(input("Tarifa por hora ($): "))
                    empleado = Empleado(0, nombre, email, cargo, tarifa)
                    if self.repo_empleado.crear(empleado):
                        print(f"\n[ÉXITO] Empleado registrado correctamente con ID: {empleado.id_usuario}")
                    else:
                        print("\n[ERROR] No se pudo guardar el empleado.")
                except ValueError as e:
                    print(f"\n[ERROR DE VALIDACIÓN]: {e}")
                pausar()

            elif opcion == "2":
                try:
                    id_emp = int(input("Ingrese el ID del empleado: "))
                    emp = self.repo_empleado.obtener_por_id(id_emp)
                    if emp:
                        print("\nDatos encontrados:")
                        print(f"ID: {emp.id_usuario} | Nombre: {emp.nombre} | Email Hash: {emp.obtener_email_cifrado()}")
                        print(f"Cargo: {emp.cargo} | Tarifa/Hora: ${emp.tarifa_hora:,.2f}")
                    else:
                        print("\nEmpleado no encontrado.")
                except ValueError:
                    print("\nID debe ser un valor numérico.")
                pausar()

            elif opcion == "3":
                try:
                    id_emp = int(input("Ingrese el ID del empleado a actualizar: "))
                    emp = self.repo_empleado.obtener_por_id(id_emp)
                    if emp:
                        print(f"\nActualizando a: {emp.nombre}")
                        emp.nombre = input(f"Nuevo Nombre [{emp.nombre}]: ").strip() or emp.nombre
                        nuevo_email = input(f"Nuevo Email [{emp.email}]: ").strip()
                        if nuevo_email:
                            emp.email = nuevo_email
                        emp.cargo = input(f"Nuevo Cargo [{emp.cargo}]: ").strip() or emp.cargo
                        
                        tarifa_str = input(f"Nueva Tarifa/Hora [{emp.tarifa_hora}]: ").strip()
                        if tarifa_str:
                            emp.tarifa_hora = float(tarifa_str)

                        if self.repo_empleado.actualizar(emp):
                            print("\n[ÉXITO] Empleado actualizado correctamente.")
                        else:
                            print("\n[ERROR] No se pudo actualizar el empleado.")
                    else:
                        print("\nEmpleado no encontrado.")
                except ValueError as e:
                    print(f"\n[ERROR]: {e}")
                pausar()

            elif opcion == "4":
                try:
                    id_emp = int(input("Ingrese el ID del empleado a eliminar: "))
                    confirm = input(f"¿Está seguro de eliminar al empleado ID {id_emp}? (s/n): ").lower()
                    if confirm == 's':
                        if self.repo_empleado.eliminar(id_emp):
                            print("\n[ÉXITO] Empleado eliminado.")
                        else:
                            print("\n[ERROR] No se pudo eliminar.")
                except ValueError:
                    print("\nID inválido.")
                pausar()

            elif opcion == "0":
                break

    # ==========================================
    # 2. MENÚ DEPARTAMENTOS
    # ==========================================
    def menu_departamentos(self):
        while True:
            limpiar_pantalla()
            print("--- GESTIÓN DE DEPARTAMENTOS ---")
            print("1. Crear Departamento")
            print("2. Buscar Departamento por ID")
            print("3. Actualizar Departamento")
            print("4. Eliminar Departamento")
            print("0. Volver al Menú Principal")
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                nombre = input("Nombre del Departamento: ").strip()
                try:
                    id_gerente = int(input("ID del Gerente a cargo: "))
                    dept = Departamento(0, nombre)
                    if self.repo_departamento.crear(dept):
                        print(f"\n[ÉXITO] Departamento creado con ID: {dept.id_departamento}")
                    else:
                        print("\n[ERROR] No se pudo crear el departamento.")
                except ValueError:
                    print("\n[ERROR] ID de gerente inválido.")
                pausar()

            elif opcion == "2":
                try:
                    id_d = int(input("ID del Departamento: "))
                    d = self.repo_departamento.obtener_por_id(id_d)
                    if d:
                        print(f"\nID: {d.id_departamento} | Nombre: {d.nombre}")
                    else:
                        print("\nDepartamento no encontrado.")
                except ValueError:
                    print("\nID inválido.")
                pausar()

            elif opcion == "3":
                try:
                    id_d = int(input("ID del Departamento a actualizar: "))
                    d = self.repo_departamento.obtener_por_id(id_d)
                    if d:
                        d.nombre = input(f"Nuevo Nombre [{d.nombre}]: ").strip() or d.nombre
                        if self.repo_departamento.actualizar(d):
                            print("\n[ÉXITO] Departamento actualizado.")
                        else:
                            print("\n[ERROR] No se pudo actualizar.")
                    else:
                        print("\nDepartamento no encontrado.")
                except ValueError:
                    print("\nEntrada inválida.")
                pausar()

            elif opcion == "4":
                try:
                    id_d = int(input("ID del Departamento a eliminar: "))
                    if self.repo_departamento.eliminar(id_d):
                        print("\n[ÉXITO] Departamento eliminado.")
                    else:
                        print("\n[ERROR] No se pudo eliminar.")
                except ValueError:
                    print("\nID inválido.")
                pausar()

            elif opcion == "0":
                break

    # ==========================================
    # 3. MENÚ PROYECTOS
    # ==========================================
    def menu_proyectos(self):
        while True:
            limpiar_pantalla()
            print("--- GESTIÓN DE PROYECTOS ---")
            print("1. Crear Proyecto")
            print("2. Buscar Proyecto por ID")
            print("3. Actualizar Proyecto")
            print("4. Eliminar Proyecto")
            print("0. Volver al Menú Principal")
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                nombre = input("Nombre del Proyecto: ").strip()
                try:
                    presupuesto = float(input("Presupuesto ($): "))
                    estado = input("Estado (Planificado/En Proceso/Completado): ").strip() or "Planificado"
                    proy = Proyecto(0, nombre, presupuesto, estado)
                    if self.repo_proyecto.crear(proy):
                        print(f"\n[ÉXITO] Proyecto creado con ID: {proy.id_proyecto}")
                    else:
                        print("\n[ERROR] No se pudo guardar el proyecto.")
                except ValueError:
                    print("\n[ERROR] Presupuesto inválido.")
                pausar()

            elif opcion == "2":
                try:
                    id_p = int(input("ID del Proyecto: "))
                    p = self.repo_proyecto.obtener_por_id(id_p)
                    if p:
                        print(f"\nID: {p.id_proyecto} | Nombre: {p.nombre} | Presupuesto: ${p.presupuesto:,.2f} | Estado: {p.estado}")
                    else:
                        print("\nProyecto no encontrado.")
                except ValueError:
                    print("\nID inválido.")
                pausar()

            elif opcion == "3":
                try:
                    id_p = int(input("ID del Proyecto a actualizar: "))
                    p = self.repo_proyecto.obtener_por_id(id_p)
                    if p:
                        p.nombre = input(f"Nuevo Nombre [{p.nombre}]: ").strip() or p.nombre
                        pres_str = input(f"Nuevo Presupuesto [{p.presupuesto}]: ").strip()
                        if pres_str:
                            p.presupuesto = float(pres_str)
                        p.estado = input(f"Nuevo Estado [{p.estado}]: ").strip() or p.estado

                        if self.repo_proyecto.actualizar(p):
                            print("\n[ÉXITO] Proyecto actualizado.")
                        else:
                            print("\n[ERROR] No se pudo actualizar.")
                    else:
                        print("\nProyecto no encontrado.")
                except ValueError:
                    print("\nEntrada inválida.")
                pausar()

            elif opcion == "4":
                try:
                    id_p = int(input("ID del Proyecto a eliminar: "))
                    if self.repo_proyecto.eliminar(id_p):
                        print("\n[ÉXITO] Proyecto eliminado.")
                    else:
                        print("\n[ERROR] No se pudo eliminar.")
                except ValueError:
                    print("\nID inválido.")
                pausar()

            elif opcion == "0":
                break

    # ==========================================
    # 4. REGISTRO DE TIEMPO
    # ==========================================
    def menu_registro_tiempo(self):
        limpiar_pantalla()
        print("--- REGISTRAR HORAS TRABAJADAS ---")
        try:
            id_emp = int(input("ID del Empleado: "))
            id_proy = int(input("ID del Proyecto: "))
            horas = float(input("Horas trabajadas: "))
            descripcion = input("Descripción de la tarea: ").strip()
            fecha = datetime.now().strftime('%Y-%m-%d')

            empleado = self.repo_empleado.obtener_por_id(id_emp)
            proyecto = self.repo_proyecto.obtener_por_id(id_proy)
            if not empleado or not proyecto:
                raise ValueError("El empleado o el proyecto indicado no existe.")

            reg = RegistroTiempo(0, empleado, proyecto, horas, fecha, descripcion)
            self.repo_registro.crear(reg)
            if reg.id_registro:
                print(f"\n[ÉXITO] Registro de tiempo almacenado correctamente (ID: {reg.id_registro}).")
            else:
                print("\n[ERROR] No se pudo registrar las horas.")
        except ValueError as e:
            print(f"\n[ERROR DE ENTRADA O VALIDACIÓN]: {e}")
        pausar()

    # ==========================================
    # 5. EXPORTAR INFORMES
    # ==========================================
    def menu_informes(self):
        limpiar_pantalla()
        print("--- EXPORTAR INFORMES GENERALES ---")
        print("1. Exportar en Formato PDF")
        print("2. Exportar en Formato Excel (.xlsx)")
        opcion = input("\nSeleccione el formato deseado: ").strip()

        conexion = self.repo_proyecto.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proyecto, nombre, presupuesto, estado FROM proyectos")
        filas = cursor.fetchall()
        conexion.close()

        datos_reporte = [
            {
                "ID Proyecto": f[0],
                "Nombre": f[1],
                "Presupuesto ($)": f"{f[2]:,.2f}",
                "Estado": f[3]
            }
            for f in filas
        ] if filas else [
            {"ID Proyecto": 1, "Nombre": "Sin proyectos registrados", "Presupuesto ($)": "0.00", "Estado": "N/A"}
        ]

        carpeta_salida = "salida_reportes"
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

        if opcion == "1":
            ruta = os.path.join(carpeta_salida, "Reporte_Proyectos_ECOTECH.pdf")
            informe = InformePDF("Consolidado General de Proyectos", datos_reporte)
            if informe.generar(ruta):
                print(f"\n[ÉXITO] Informe PDF generado en: {ruta}")
        elif opcion == "2":
            ruta = os.path.join(carpeta_salida, "Reporte_Proyectos_ECOTECH.xlsx")
            informe = InformeExcel("Consolidado General de Proyectos", datos_reporte)
            if informe.generar(ruta):
                print(f"\n[ÉXITO] Informe Excel generado en: {ruta}")
        else:
            print("\nOpción inválida.")
        pausar()

if __name__ == "__main__":
    app = MenuApp()
    app.iniciar_sistema()