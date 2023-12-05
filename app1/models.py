from django.db import models

# Create your models here.

class Usuarios(models.Model):
    estudiante_matricula = models.CharField(max_length=10, unique=True)
    profesor_matricula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True) # se van a guardar en una carpeta llamada 'media' configurada en los 'settings'

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuario'
        ordering = ['id']

class Ticket(models.Model):
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()

    DEPARTAMENTO_CHOICES = (
        ('otro', 'Otro'),
        ('contabilidad', 'Contabilidad'),
        ('rrhh', 'RRHH'),
        ('legal', 'Legal'),
        ('informatica', 'Informatica'),
    )
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTO_CHOICES, default='Otro')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # sacar en una tabla log
    # fecha_actualizacion = models.DateTimeField(auto_now=True)

    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='tickets_creados')
    email = models.EmailField(blank=True)
    asignado_a = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')

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
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    comentario = models.TextField()

    def __str__(self):
        return f"Comentario: {self.id} - Ticket#: {self.FK_id_ticket.id} - Comentado por: {self.usuario.username}"

class Estado(models.Model):
    ESTADO_CHOICES = (
        ('Abierto', 'abierto'),
        ('En progreso', 'en_progreso'),
        ('Cerrado', 'cerrado'),
    )
    FK_id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='estados')
    usuario_creacion = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='estados_creados')
    usuario_modificacion = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='estados_modificados')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierto')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    # comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id} - Ticket#: {self.FK_id_ticket.id} - Estado: {self.estado} - Clasificado por: {self.usuario_creacion.username}"

class Prioridad(models.Model):
    PRIORIDAD_CHOICES = (
        ('Normal', 'normal'),
        ('Baja', 'baja'),
        ('Alta', 'alta'),
    )
    FK_id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='prioridades')
    usuario_creacion = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='prioridades_creadas')
    usuario_modificacion = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='prioridades_modificadas')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='Normal')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    # comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id} - Ticket#: {self.FK_id_ticket.id} - Prioridad: {self.prioridad} - Clasificado por: {self.usuario_creacion.username}"