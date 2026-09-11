#Verifica la escritura y lectura de archivos sin alterar tus datos reales 
#de producción usando un archivo de prueba temporal.

import os
import unittest
import modelos.persistencia as persistencia
from modelos import Empleado, Gerente, Departamento, Proyecto, RegistroTiempo


class TestPersistenciaEcoTech(unittest.TestCase):

    def setUp(self):
        """Usa un archivo JSON temporal para evitar sobreescribir datos reales."""
        self.archivo_temp = "test_datos_ecotech.json"
        self.original_archivo = persistencia.ARCHIVO_DATOS
        persistencia.ARCHIVO_DATOS = self.archivo_temp

        # Objetos de prueba
        self.emp = Empleado(1, "Laura Torres", "laura@ecotech.com", "Analista", 30.0)
        self.ger = Gerente(2, "Pedro Soto", "pedro@ecotech.com", tarifa_hora=50.0, bono_liderazgo=1000.0)
        self.depto = Departamento(1, "I+D", self.ger)
        self.depto.agregar_empleado(self.emp)
        self.proy = Proyecto(1, "EcoSoftware", 5000.0)
        self.reg = RegistroTiempo(1, self.emp, self.proy, 5.0, descripcion="Diseño de módulo")

    def tearDown(self):
        """Restaura la configuración original y elimina el archivo temporal."""
        persistencia.ARCHIVO_DATOS = self.original_archivo
        if os.path.exists(self.archivo_temp):
            os.remove(self.archivo_temp)

    def test_guardar_y_cargar_datos(self):
        """Prueba guardar y reconstruir la estructura completa desde un archivo JSON."""
        # 1. Guardar
        persistencia.guardar_datos([self.emp, self.ger], [self.depto], [self.proy], [self.reg])
        self.assertTrue(os.path.exists(self.archivo_temp))

        # 2. Cargar
        empleados_c, deptos_c, proys_c, regs_c = persistencia.cargar_datos()

        # 3. Aserciones
        self.assertEqual(len(empleados_c), 2)
        self.assertEqual(len(deptos_c), 1)
        self.assertEqual(len(proys_c), 1)
        self.assertEqual(len(regs_c), 1)

        # Verificar integridad del objeto reconstruido
        emp_rec = empleados_c[0]
        self.assertEqual(emp_rec.nombre, "Laura Torres")
        self.assertEqual(emp_rec.tarifa_hora, 30.0)


if __name__ == "__main__":
    unittest.main()
