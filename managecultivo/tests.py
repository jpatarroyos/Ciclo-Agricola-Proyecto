from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import ZonaAgricola, Cultivo, Ciclo, CicloMonitoreo, Actividad, Insumo, CicloActividad, CicloActividadInsumo, Personal


class AgriculturaModelsTestCase(TestCase):

    def setUp(self):
        """Configuración de la infraestructura base para las pruebas."""
        self.user = User.objects.create_user(
            username="supervisor_campo",
            password="PasswordSeguro2026",
            email="admin@finca.com"
        )
        
        self.zona = ZonaAgricola.objects.create(
            nombre="Lote Este",
            ubicacion="Sección C",
            direccion="Km 2",
            registrado_por=self.user
        )
        
        self.cultivo = Cultivo.objects.create(
            descripcion="Papa Pastusa",
            tiempo_agricola=120,
            registrado_por=self.user
        )
        
        # Creamos un ciclo base que usaremos en ambas pruebas
        self.ciclo = Ciclo.objects.create(
            id_cultivo=self.cultivo,
            id_zonaagricola=self.zona,
            fecha_inicio=date(2026, 6, 1),
            fecha_fin=date(2026, 10, 1),
            cantidad_produccion=0.0,
            registrado_por=self.user
        )

    ## --- PRUEBAS DE USUARIOS ---
    def test_crear_usuario(self):
        """Verifica que un usuario se cree correctamente con sus atributos."""
        self.assertEqual(self.user.username, "supervisor_campo")
        self.assertEqual(self.user.email, "admin@finca.com")
        self.assertTrue(self.user.is_active)

    ## --- PRUEBAS DE ZONA AGRÍCOLA ---
    def test_crear_zona_agricola_con_usuario(self):
        """Valida la creación de una zona agrícola vinculada a un usuario."""
        zona = ZonaAgricola.objects.create(
            nombre="Lote Norte",
            ubicacion="Sección A",
            direccion="Km 5 Vía Principal",
            registrado_por=self.user
        )
        
        self.assertEqual(zona.nombre, "Lote Norte")
        self.assertEqual(zona.registrado_por, self.user)
        # Verificar el método __str__
        self.assertEqual(str(zona), "Lote Norte - Sección A")

    def test_crear_zona_agricola_sin_usuario(self):
        """Valida que la zona agrícola acepte registrado_por como NULL."""
        zona = ZonaAgricola.objects.create(
            nombre="Lote Sur",
            ubicacion="Sección B",
            direccion="Km 12 Vía Alterna",
            registrado_por=None
        )
        self.assertNil = self.assertIsNone(zona.registrado_por)

    ## --- PRUEBAS DE PERSONAL ---
    def test_crear_personal_con_rol_por_defecto(self):
        """Verifica la creación de personal y que el rol por defecto sea 'Varios'."""
        trabajador = Personal.objects.create(
            id_cedula="123456789",
            nombre="Juan Pérez",
            telefono="555-1234",
            email="juan.perez@email.com"
        )
        
        self.assertEqual(trabajador.id_cedula, "123456789")
        self.assertEqual(trabajador.rol, "Varios")  # Valida el default del modelo
        self.assertEqual(str(trabajador), "123456789 - Juan Pérez (Varios)")

    def test_crear_personal_con_rol_especifico(self):
        """Verifica que se asigne correctamente un rol específico (ej. Fumigador)."""
        fumigador = Personal.objects.create(
            id_cedula="987654321",
            nombre="Carlos Gómez",
            rol="Fumigador"
        )
        self.assertEqual(fumigador.rol, "Fumigador")
        # Verificar campos opcionales en blanco
        self.assertIsNone(fumigador.telefono)
        self.assertIsNone(fumigador.email)

    from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date
from .models import (
    ZonaAgricola, Cultivo, Actividad, Insumo, 
    Ciclo, CicloActividad, CicloActividadInsumo
)

class GestionCiclosYActividadesTestCase(TestCase):

    def setUp(self):
        """Configuración de datos base necesarios para los flujos complejos."""
        # 1. Usuario administrador
        self.user = User.objects.create_user(
            username="agronomo_jefe",
            password="SeguridadFinca2026"
        )
        
        # 2. Zona Agrícola base
        self.zona = ZonaAgricola.objects.create(
            nombre="Invernadero 1",
            ubicacion="Bloque Norte",
            direccion="Lote 4",
            registrado_por=self.user
        )
        
        # 3. Cultivo base (ej: Tomate que dura 90 días)
        self.cultivo = Cultivo.objects.create(
            descripcion="Tomate Chonto",
            tiempo_agricola=90,
            registrado_por=self.user
        )
        
        # 4. Actividad base
        self.actividad = Actividad.objects.create(
            descripcion="Fumigación Preventiva",
            prioridad="alta",
            registrado_por=self.user
        )
        
        # 5. Insumo en inventario
        self.insumo = Insumo.objects.create(
            descripcion="Fungicida Organico X",
            cantidad_existente=50.0, # 50 Kg/L disponibles
            tipo="fungicida",
            registrado_por=self.user
        )

    ## --- PRUEBAS DE CICLO AGRÍCOLA ---
    def test_crear_ciclo_agricola(self):
        """Verifica la correcta creación de un ciclo de cultivo en una zona."""
        ciclo = Ciclo.objects.create(
            id_cultivo=self.cultivo,
            id_zonaagricola=self.zona,
            fecha_inicio=date(2026, 5, 1),
            fecha_fin=date(2026, 8, 1),
            cantidad_produccion=1200.5, # Cosecha estimada/real en Kg
            registrado_por=self.user
        )
        
        self.assertEqual(ciclo.id_cultivo.descripcion, "Tomate Chonto")
        self.assertEqual(ciclo.id_zonaagricola.nombre, "Invernadero 1")
        self.assertEqual(ciclo.cantidad_produccion, 1200.5)
        self.assertIn("Ciclo de Tomate Chonto", str(ciclo))

    ## --- PRUEBAS DE ACTIVIDADES DENTRO DEL CICLO ---
    def test_programar_actividad_en_ciclo(self):
        """Valida que se pueda agendar una actividad específica dentro de un ciclo."""
        # Primero creamos el ciclo necesario
        ciclo = Ciclo.objects.create(
            id_cultivo=self.cultivo,
            id_zonaagricola=self.zona,
            fecha_inicio=date(2026, 5, 1),
            fecha_fin=date(2026, 8, 1),
            cantidad_produccion=0.0,
            registrado_por=self.user
        )
        
        # Programamos la actividad para este ciclo
        actividad_ciclo = CicloActividad.objects.create(
            id_ciclo=ciclo,
            id_actividad=self.actividad,
            fecha_programada=date(2026, 5, 15),
            color="#FF5733",
            registrado_por=self.user
        )
        
        self.assertEqual(actividad_ciclo.id_actividad.descripcion, "Fumigación Preventiva")
        self.assertEqual(actividad_ciclo.color, "#FF5733")
        self.assertIn("Fumigación Preventiva en Tomate Chonto", str(actividad_ciclo))

    ## --- PRUEBAS DE ASIGNACIÓN DE INSUMOS ---
    def test_asignar_insumo_a_actividad_de_ciclo(self):
        """Prueba el registro del gasto real de un insumo en una actividad programada."""
        # 1. Crear ciclo
        ciclo = Ciclo.objects.create(
            id_cultivo=self.cultivo,
            id_zonaagricola=self.zona,
            fecha_inicio=date(2026, 5, 1),
            fecha_fin=date(2026, 8, 1),
            cantidad_produccion=0.0,
            registrado_por=self.user
        )
        
        # 2. Crear actividad en el ciclo
        actividad_ciclo = CicloActividad.objects.create(
            id_ciclo=ciclo,
            id_actividad=self.actividad,
            fecha_programada=date(2026, 5, 15),
            registrado_por=self.user
        )
        
        # 3. Asignar el insumo utilizado
        insumo_utilizado = CicloActividadInsumo.objects.create(
            actividad_ciclo=actividad_ciclo,
            id_insumo=self.insumo,
            cantidad_utilizada=4.5, # Se gastaron 4.5 Kg
            registrado_por=self.user
        )
        
        self.assertEqual(insumo_utilizado.id_insumo.descripcion, "Fungicida Organico X")
        self.assertEqual(insumo_utilizado.cantidad_utilizada, 4.5)
        # Validar que la relación hacia atrás (relación inversa) funcione mediante el __str__
        self.assertIn("Fungicida Organico X usado en Actividad Fumigación Preventiva", str(insumo_utilizado))

class MonitoreoYBorradoTestCase(TestCase):

    def setUp(self):
        """Configuración de la infraestructura base para las pruebas."""
        self.user = User.objects.create_user(
            username="supervisor_campo",
            password="PasswordSeguro2026"
        )
        
        self.zona = ZonaAgricola.objects.create(
            nombre="Lote Este",
            ubicacion="Sección C",
            direccion="Km 2",
            registrado_por=self.user
        )
        
        self.cultivo = Cultivo.objects.create(
            descripcion="Papa Pastusa",
            tiempo_agricola=120,
            registrado_por=self.user
        )
        
        # Creamos un ciclo base que usaremos en ambas pruebas
        self.ciclo = Ciclo.objects.create(
            id_cultivo=self.cultivo,
            id_zonaagricola=self.zona,
            fecha_inicio=date(2026, 6, 1),
            fecha_fin=date(2026, 10, 1),
            cantidad_produccion=0.0,
            registrado_por=self.user
        )

    ## --- PRUEBAS DE OBSERVACIONES DE MONITOREO ---
    def test_crear_observacion_monitoreo(self):
        """Valida que se registren bitácoras u observaciones sobre un ciclo activo."""
        bitacora = CicloMonitoreo.objects.create(
            id_ciclo=self.ciclo,
            observacion="Se detectaron indicios leves de plaga (tizón tardío) en las hojas inferiores. Se recomienda revisión.",
            fecha=date(2026, 6, 15),
            registrado_por=self.user
        )
        
        # Validar persistencia de los datos
        self.assertEqual(bitacora.id_ciclo, self.ciclo)
        self.assertIn("tizón tardío", bitacora.observacion)
        self.assertEqual(bitacora.fecha, date(2026, 6, 15))
        
        # Validar método __str__
        self.assertIn("Papa Pastusa el 2026-06-15", str(bitacora))

    ## --- PRUEBAS DE BORRADO EN CASCADA (INTEGRIDAD REFERENCIAL) ---
    def test_eliminacion_cultivo_borra_ciclos_en_cascada(self):
        """Verifica que al eliminar un Cultivo, se borren automáticamente sus Ciclos asociados (CASCADE)."""
        # Aseguramos primero que el ciclo existe en la base de datos
        self.assertTrue(Ciclo.objects.filter(id_ciclo=self.ciclo.id_ciclo).exists())
        
        # Acto: Eliminamos el cultivo padre
        self.cultivo.delete()
        
        # Afirmación: El ciclo asociado debió desaparecer debido al on_delete=models.CASCADE
        ciclo_existe = Ciclo.objects.filter(id_ciclo=self.ciclo.id_ciclo).exists()
        self.assertFalse(ciclo_existe, "El ciclo no se eliminó en cascada al borrar su cultivo.")