from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import ZonaAgricola, Personal


class AgriculturaModelsTestCase(TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas. 
        Se ejecuta antes de cada método de prueba.
        """
        # 1. Crear un usuario de prueba
        self.user = User.objects.create_user(
            username="admin_campo",
            email="admin@finca.com",
            password="PasswordSeguro123"
        )

    ## --- PRUEBAS DE USUARIOS ---
    def test_crear_usuario(self):
        """Verifica que un usuario se cree correctamente con sus atributos."""
        self.assertEqual(self.user.username, "admin_campo")
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