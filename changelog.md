# Changelog

Registro de interacciones y cambios en el proyecto ECOTECH.

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
