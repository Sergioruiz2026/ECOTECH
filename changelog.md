# Changelog

Registro de interacciones y cambios en el proyecto ECOTECH.

---

## 2026-09-15

### Prompt

Corregir `main.py` y compatibilizar la interfaz de consola con los modelos y repositorios actuales.

### Respuesta/Acciones

- Se reemplazaron imports obsoletos de `entidades` por `modelos`.
- Se corrigió el repositorio de registros de tiempo.
- Se actualizó la inicialización para compartir `Database` entre repositorios.
- Se adaptaron autenticación, registro de usuarios, empleados, departamentos, proyectos y registros de tiempo a las APIs actuales.

### Archivos Modificados

- `main.py`
- `changelog.md`

### Validaciones

- `MenuApp` instanciado correctamente.
- Menú de acceso iniciado y cerrado mediante la opción `0`.
- Actualización de nombre de proyecto validada.
- Sintaxis y diagnósticos de `main.py` correctos.

---

## 2026-09-15

### Prompt

Corregir el error al actualizar el nombre de un proyecto desde el menú de consola.

### Respuesta/Acciones

- Se añadió el setter `Proyecto.nombre`.
- El setter valida que el nombre no esté vacío y elimina espacios laterales.

### Archivos Modificados

- `modelos/proyecto.py`
- `changelog.md`

### Validaciones

- Actualización directa del nombre ejecutada correctamente.
- Sintaxis validada con `py_compile`.

---

## 2026-09-15

### Prompt

Corregir la interfaz de consola y el menú de gestión de ECOTECH.

### Respuesta/Acciones

- Se reemplazaron imports obsoletos de `entidades` por los modelos actuales.
- Se corrigió el nombre del repositorio de registros de tiempo.
- Se adaptaron las operaciones del menú a los constructores y métodos actuales de SQLite.
- Se corrigió la asignación de IDs en los repositorios al guardar entidades.
- Se agregó validación repetitiva para confirmaciones de eliminación.

### Archivos Modificados

- `main.py`
- `repositorios/empleado_repository.py`
- `repositorios/proyecto_repository.py`
- `repositorios/departamento_repository.py`
- `changelog.md`

### Validaciones

- Arranque de `main.py` y salida mediante la opción `0`.
- Flujo directo de creación en el submenú de proyectos.
- Confirmación inválida seguida de `n` correctamente gestionada.
- Comprobación de sintaxis con `py_compile`.

---

## 2026-09-15

### Prompt

Crear `main_informes.py` para consultar SQLite mediante repositorios y generar reportes PDF y Excel en `salida_reportes/`.

### Respuesta/Acciones

- Se alinearon los repositorios de empleados, proyectos y departamentos con `Database` y las clases de `modelos`.
- Se añadieron las lecturas masivas necesarias para el flujo de reportes.
- Se creó `main_informes.py` para generar `reporte_tiempo.pdf` y `reporte_tiempo.xlsx`.

### Archivos Modificados

- `main_informes.py`
- `repositorios/repositorio_base.py`
- `repositorios/empleado_repository.py`
- `repositorios/proyecto_repository.py`
- `repositorios/departamento_repository.py`
- `changelog.md`

### Validaciones

- Ejecución de `python main_informes.py` completada correctamente.
- Suite de pruebas del proyecto ejecutada correctamente.

---

## 2026-09-15

### Prompt

Corregir la confirmación de eliminación de departamentos cuando se ingresa una letra distinta de `s` o `n`.

### Respuesta/Acciones

- Se verificó el flujo exacto de eliminación de un departamento.
- Una letra inválida ahora mantiene la solicitud activa hasta recibir `s` o `n`.
- Se agregó una prueba integrada con el caso `x` seguido de `n`.

### Archivos Modificados

- `pruebas/test_main.py`
- `changelog.md`

### Validaciones

- Prueba enfocada y suite completa ejecutadas correctamente.

---

## 2026-09-15

### Prompt

Verificar nuevamente que una letra distinta de `s` o `n` no cierre el sistema durante una confirmación.

### Respuesta/Acciones

- Se reforzó el helper de confirmaciones para normalizar la entrada y repetir la pregunta.
- Se eliminó el flujo redundante alrededor de la confirmación de gerente.
- Se agregó una prueba integrada de creación de departamento con respuesta inválida.

### Archivos Modificados

- `main.py`
- `pruebas/test_main.py`
- `changelog.md`

### Validaciones

- Pruebas enfocadas y suite completa ejecutadas correctamente.

---

## 2026-09-15

### Prompt

Corregir las confirmaciones `s/n` para que una letra inválida no cierre ni cancele el flujo.

### Respuesta/Acciones

- Se centralizó la validación de confirmaciones en `solicitar_confirmacion`.
- Las respuestas distintas de `s` o `n` muestran un mensaje y vuelven a preguntar.
- Se aplicó la validación al asignar gerentes y confirmar eliminaciones.
- Se agregó una prueba para una respuesta inválida seguida de una respuesta válida.

### Archivos Modificados

- `main.py`
- `pruebas/test_main.py`
- `changelog.md`

### Validaciones

- Prueba enfocada y suite completa ejecutadas correctamente.

---

## 2026-09-15

### Prompt

Agregar opciones de modificar y eliminar para las diferentes clases del script.

### Respuesta/Acciones

- Se agregaron las opciones `Modificar datos` y `Eliminar datos` al menú principal.
- Se habilitaron operaciones para empleados/gerentes, departamentos, proyectos y registros de tiempo.
- Las eliminaciones solicitan confirmación y limpian relaciones y registros dependientes.
- Las modificaciones conservan los valores actuales cuando se deja un campo vacío.
- Se agregaron pruebas para modificar proyectos y eliminar departamentos.

### Archivos Modificados

- `main.py`
- `pruebas/test_main.py`
- `changelog.md`

### Validaciones

- Suite completa de pruebas ejecutada correctamente.

---

## 2026-09-15

### Prompt

Corregir el cierre del sistema al ingresar un correo inválido y mostrar los departamentos existentes.

### Respuesta/Acciones

- El registro de empleados vuelve a solicitar el correo cuando el formato es inválido.
- Se muestra un mensaje de corrección sin interrumpir el programa.
- La persistencia usa una ruta absoluta basada en el proyecto para cargar los departamentos aunque el programa se ejecute desde otro directorio.
- Se agregó una prueba para el reintento de correo.

### Archivos Modificados

- `main.py`
- `modelos/persistencia.py`
- `pruebas/test_main.py`
- `changelog.md`

### Validaciones

- Prueba enfocada del menú y suite completa ejecutadas correctamente.

---

## 2026-09-15

### Prompt

Verificar la seguridad del menú de creación de departamentos y reutilizar los departamentos ya creados.

### Respuesta/Acciones

- El menú muestra los departamentos existentes como opciones.
- Se evita crear departamentos con nombres vacíos, demasiado largos o duplicados sin distinguir mayúsculas/minúsculas.
- Se valida que el número de gerente seleccionado sea válido.
- Se agregaron pruebas del flujo interactivo.

### Archivos Modificados

- `main.py`
- `pruebas/test_main.py`
- `changelog.md`

### Validaciones

- Pruebas unitarias de modelos, persistencia y menú ejecutadas correctamente.

---

## 2026-09-14

### Prompt

Corrección de validación, cifrado y persistencia de correos electrónicos.

### Respuesta/Acciones

- Se corrigió el formato de validación de correos al crear usuarios.
- Se normalizaron los correos antes de validarlos.
- Se implementó el cifrado de la parte local del correo al guardar datos.
- Se evitó el doble cifrado al recargar información persistida.
- Se migraron los correos existentes a su versión cifrada.

### Archivos Modificados

- `modelos/usuario.py`
- `modelos/persistencia.py`
- `pruebas/test_persistencia.py`
- `datos_ecotech.json`

### Validaciones

- Pruebas de modelos y persistencia ejecutadas correctamente.
- Verificación directa de creación, validación y cifrado de usuarios.

---

## 2026-09-14

### Prompt

Validar la respuesta `s/n` al asignar un gerente al crear un departamento.

### Respuesta/Acciones

- Se agregó un bucle de validación para aceptar únicamente `s` o `n`.
- Las respuestas inválidas muestran un mensaje y vuelven a solicitarse.

### Archivos Modificados

- `main.py`

### Validaciones

- Flujo simulado con respuesta inválida y posterior respuesta válida.
- Comprobación de sintaxis de `main.py`.

---

## 2026-09-14

### Prompt

Exigir que las tarifas por hora y los bonos de liderazgo sean siempre mayores que cero.

### Respuesta/Acciones

- Los constructores y setters ahora rechazan valores `0` y negativos.
- El menú repite la solicitud cuando se introduce un valor inválido.
- Se actualizaron las restricciones de la base de datos a `CHECK > 0`.
- Se corrigieron los valores existentes en `datos_ecotech.json`.

### Archivos Modificados

- `modelos/empleado.py`
- `modelos/gerente.py`
- `modelos/persistencia.py`
- `database/database.py`
- `main.py`
- `datos_ecotech.json`
- `pruebas/test_modelos.py`

### Validaciones

- Suite de pruebas ejecutada correctamente.
- Carga del JSON real con tarifas y bonos positivos.
- Prueba de reintento al introducir `0`.

---

## 2026-09-14

### Prompt

Corregir `changelog.md` porque no estaba registrando los prompts utilizados.

### Respuesta/Acciones

- Se agregaron al registro las interacciones recientes y sus acciones asociadas.
- Se documentaron los archivos modificados y las validaciones ejecutadas.

### Archivos Modificados

- `changelog.md`

### Validaciones

- Revisión del contenido del registro y de la instrucción de registro obligatorio en `Gemini.md`.

---

## 2026-09-11

### Prompt

Verificación de `Gemini.md` y creación del archivo `changelog.md`

### Respuesta/Acciones

- Lectura y verificación del archivo `Gemini.md`
- Confirmación de estructura correcta y directrices claras
- Creación del archivo `changelog.md` como registro obligatorio

### Archivos Modificados

- `changelog.md` (creado)

### Validaciones

- ✅ Archivo `Gemini.md` con contenido completo y bien estructurado
- ✅ Instrucciones claras para el flujo de trabajo
- ✅ Especificación de `changelog.md` confirmada

---
