from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + " " + self.user.username
    
class Categoria(models.Model):
    cat = models.CharField(max_length=64)
    imagen = models.ImageField(upload_to='products/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.cat}"

class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    important = models.BooleanField(default=False)
    cat = models.CharField(max_length=64)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField()
    precio_aumentado = models.IntegerField()
    imagen = models.ImageField(upload_to='products/', null=True, blank=True)
    imagen1 = models.ImageField(upload_to='products/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='products/', null=True, blank=True)
    imagen4 = models.ImageField(upload_to='products/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre}: {self.precio}"
    
    
class DatosPersonales(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    nacionalidad = models.CharField(max_length=64)
    ciudad = models.CharField(max_length=64)
    telefono = models.IntegerField()
    nombreempresa = models.CharField(max_length=100)
    cbu = models.IntegerField()
    titular = models.CharField(max_length=64)
    descripcionempresa = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre}: {self.nombreempresa}"
    
class formulario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=55)
    telefono = models.CharField(max_length=55)
    mail = models.EmailField(max_length=55)
    texto = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255)


class compra(models.Model):
    id = models.AutoField(primary_key=True)
    producto_id = models.CharField(max_length=55)
    codigo = models.CharField(max_length=55)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    link = models.CharField(max_length=255)
    orden = models.CharField(max_length=255)


class cupon(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=55)
    descuento = models.IntegerField()
    contador = models.IntegerField(default=1)

 
class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    color = models.CharField(max_length=64)
    talle = models.CharField(max_length=64)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.color} - {self.talle}: {self.cantidad}"
    

class ShippingAddress(models.Model):
   
  

    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    direccion = models.CharField(max_length=255)
    numero = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}, {self.direccion} {self.numero}, {self.ciudad}, {self.estado}, {self.pais}, {self.user.username}, {self.email}"