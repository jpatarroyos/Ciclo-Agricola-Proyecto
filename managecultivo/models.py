from django.db import models
from django.contrib.auth.models import User


# Zonas agrícolas
class ZonaAgricola(models.Model):
    id_zonaagricola = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_ZonaAgricola")

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"


# Cultivo
class Cultivo(models.Model):
    id_cultivo = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    tiempo_agricola = models.IntegerField(help_text="Tiempo en días")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_Cultivo")

    def __str__(self):
        return self.descripcion


# Actividad agrícola
class Actividad(models.Model):
    PRIORIDADES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
    ]

    id_actividad = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default="media")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_Actividad")

    def __str__(self):
        return f"{self.descripcion} (Prioridad: {self.get_prioridad_display()})"

# Insumos
class Insumo(models.Model):
    TIPOS = [
        ("fertilizante", "Fertilizante"),
        ("insecticida", "Insecticida"),
        ("fungicida", "Fungicida"),
        ("herbicida", "Herbicida"),                        
        ("semilla", "Semilla"),
        ("plantula", "Plantula"),        
        ("herramienta", "Herramienta"),
        ("recurso", "Recurso"),        
    ]

    id_insumo = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    cantidad_existente = models.FloatField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default="fertilizante")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_insumos")

    def __str__(self):
        return f"{self.descripcion} ({self.get_tipo_display()})"


class UnidadTiempo(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

# Compra de insumos
class CompraInsumo(models.Model):
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="fk_CompraInsumo1")
    fecha_compra = models.DateField()
    marca = models.CharField(max_length=50)
    cantidad = models.FloatField()
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_CompraInsumo2")

    def __str__(self):
        return f"{self.id_insumo.descripcion} - {self.fecha_compra} - {self.cantidad}"


# Personal
class Personal(models.Model):
    id_cedula = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    ROLES = [
        ("Agricultor", "Agricultor"),
        ("Fumigador", "Fumigador"),
        ("Recolector", "Recolector"),
        ("Varios", "Varios"),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default="Varios")

    def __str__(self):
        return f"{self.id_cedula} - {self.nombre} ({self.rol})"

# Ciclo agrícola
class Ciclo(models.Model):
    id_ciclo = models.BigAutoField(primary_key=True)
    id_cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name="fk_ciclo1")
    id_zonaagricola = models.ForeignKey(ZonaAgricola, on_delete=models.CASCADE, related_name="fk_ciclo2")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cantidad_produccion = models.FloatField(help_text="Cantidad cosechada en Kg")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_ciclo3")

    def __str__(self):
        return f"Ciclo de {self.id_cultivo.descripcion} ({self.fecha_inicio} - {self.fecha_fin})"

# Actividades dentro del ciclo
class CicloActividad(models.Model):
    id_ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name="fk_CicloActividad1")
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="fk_CicloActividad2")
    fecha_programada = models.DateField()
    color = models.CharField(max_length=20, default="#000000")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_CicloActividad3")

    def __str__(self):
        return f"{self.id_actividad.descripcion} en {self.id_ciclo.id_cultivo.descripcion} el {self.fecha_programada}"


# Insumos utilizados en actividades dentro del ciclo
class CicloActividadInsumo(models.Model):
    actividad_ciclo = models.ForeignKey(CicloActividad, on_delete=models.CASCADE, related_name="fk_CCicloActividadInsumo1")
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="fk_CCicloActividadInsumo2")
    cantidad_utilizada = models.FloatField(help_text="Cantidad real utilizada en Kg")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_CCicloActividadInsumo3")

    def __str__(self):
        return f"{self.id_insumo.descripcion} usado en Actividad {self.actividad_ciclo.id_actividad.descripcion} cultivo {self.actividad_ciclo.id_ciclo.id_cultivo.descripcion} fecha {self.actividad_ciclo.fecha_programada} "


# Relación Personal - Actividad
class CicloActividadPersonal(models.Model):
    actividad_ciclo = models.ForeignKey(CicloActividad, on_delete=models.CASCADE, related_name="fk_CicloActividadPersonal1")
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="fk_CicloActividadPersonal2")

    def __str__(self):
        return f"{self.personal.nombre} en ciclo {self.actividad_ciclo.id_ciclo.id_cultivo.descripcion}"

# Observaciones del Monitoreo
class CicloMonitoreo(models.Model):
    id_ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name="fk_CicloMonitoreo1")
    observacion = models.TextField()
    fecha = models.DateField()
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_CicloMonitoreo2")

    def __str__(self):
        return f"{self.id_ciclo.id_cultivo.descripcion} el {self.fecha} observacion {self.observacion}"

# Relación Cultivo - Actividad
class CultivoActividad(models.Model):
    TIPOS = [
        ("obligatoria", "Obligatoria"),
        ("opcional", "Opcional"),
    ]    
    id_cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name="fk_cultivoactividad")
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="fk_cultivoactividad2")
    dia_inicio = models.IntegerField(default=1)    
    frecuencia = models.ForeignKey(UnidadTiempo, on_delete=models.PROTECT, related_name="fk_cultivoactividad3")
    min_personas = models.IntegerField()
    max_personas = models.IntegerField()    
    tipo = models.CharField(max_length=20, choices=TIPOS, default="obligatoria")    
    color = models.CharField(max_length=20, default="#000000")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_cultivoactividad4")
    personal_encargado = models.ManyToManyField(
        Personal,
        blank=True,
        related_name="cultivo_actividades",
        help_text="Personal asignado a esta actividad para este cultivo específico",
    )

    class Meta:
        ordering = ["dia_inicio"]

    def __str__(self):
        return f"Cultivo: {self.id_cultivo.descripcion} | dia inicio: {self.dia_inicio} - actividad:{self.id_actividad.descripcion}"

# Relación Cultivo-Actividad - Insumos
class CultivoActividadInsumo(models.Model):
    actividad_cultivo = models.ForeignKey(CultivoActividad, on_delete=models.CASCADE, related_name="fk_CultivoActividadInsumo1")
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="fk_CultivoActividadInsumo2")
    cantidad_sugerida = models.FloatField(help_text="Cantidad requerida para la actividad")
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fk_CultivoActividadInsumo2")

    def __str__(self):
        return f"{self.actividad_cultivo.id_cultivo.descripcion} | {self.actividad_cultivo.id_actividad.descripcion} | {self.id_insumo.descripcion}"

# Relación Cultivo-Actividad - Personal
class CultivoActividadPersonal(models.Model):
    actividad_cultivo = models.ForeignKey(CultivoActividad, on_delete=models.CASCADE, related_name="fk_CultivoActividadPersonal_Base")
    id_personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="fk_CultivoActividadPersonal_Base2")

    def __str__(self):
        return f"{self.actividad_cultivo} -> Encargado: {self.id_personal.nombre}"