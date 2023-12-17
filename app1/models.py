from django.db import models
from user.models import User

# Create your models here.
class Ticket(models.Model):
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()

    OTRO = 'Otro'
    CONTABILIDAD = 'Contabilidad'
    RRHH = 'RRHH'
    LEGAL = 'Legal'
    INFORMATICA = 'Informatica'

    DEPARTAMENTO_CHOICES = [
        (OTRO, 'Otro'),
        (CONTABILIDAD, 'Contabilidad'),
        (RRHH, 'RRHH'),
        (LEGAL, 'Legal'),
        (INFORMATICA, 'Informatica'),
    ]
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTO_CHOICES, default='Otro')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_creados')
    email = models.EmailField(blank=True)
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')

    #  índice para acelerar las consultas frecuentes que buscan tickets por su estado o prioridad:
    # estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='tickets', null=True)
    # prioridad = models.ForeignKey(Prioridad, on_delete=models.CASCADE, related_name='tickets', null=True)

    def save(self, *args, **kwargs):
        # Aquí se agrega automáticamente el correo electrónico del usuario registrado
        self.email = self.usuario.email
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.asunto} - creado por: {self.usuario.username}"

class Comentario(models.Model):
    FK_id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')
    fecha_creado = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()

    def __str__(self):
        return f"Comentario: {self.id} - Ticket#: {self.FK_id_ticket.id} - Comentado por: {self.usuario.username}"

class Estado(models.Model):
    ABIERTO = 'Abierto'
    EN_PROGRESO = 'En progreso'
    CERRADO = 'Cerrado'

    ESTADO_CHOICES = [
        (ABIERTO, 'Abierto'),
        (EN_PROGRESO, 'En progreso'),
        (CERRADO, 'Cerrado'),
    ]
    FK_id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='estados')
    usuario_creacion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estados_creados')
    usuario_modificacion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estados_modificados')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierto')
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - Ticket#: {self.FK_id_ticket.id} - Estado: {self.estado} - Clasificado por: {self.usuario_creacion.username}"

class Prioridad(models.Model):
    NORMAL = 'Normal'
    BAJA = 'Baja'
    ALTA = "Alta"

    PRIORIDAD_CHOICES = [
        (NORMAL, 'Normal'),
        (BAJA, 'Baja'),
        (ALTA, 'Alta'),
    ]
    FK_id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='prioridades')
    usuario_creacion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prioridades_creadas')
    usuario_modificacion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prioridades_modificadas')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='Normal')
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - Ticket#: {self.FK_id_ticket.id} - Prioridad: {self.prioridad} - Clasificado por: {self.usuario_creacion.username}"