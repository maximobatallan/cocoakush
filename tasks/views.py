from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, DatosForm, ProductForm
from .models import Task, Producto, DatosPersonales, Categoria, formulario,compra, cupon
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
from .carrito import Carrito
import mercadopago
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import requests



def home(request):
    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()


    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
   
   

    return render(request, "home.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )




def signup(request):
    if request.method == 'GET':
        
        return render(request, 'signup.html',{'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('gallery')
            except IntegrityError:
                return render(request, 'signup.html',{'form': UserCreationForm, "error":'Usuario ya existe'})
            
            
        return render(request, 'signup.html',{'form': UserCreationForm, "error":'La contraseña de verificación no coincide.'})


@login_required 
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render (request, 'tasks.html', {'tasks': tasks})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        if 'submit_get' in request.POST:
            return render(request, 'signin.html', {"form": AuthenticationForm})
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render (request, 'signin.html',{'form': AuthenticationForm, "error":'Usuario o pass incorrecto'})
            else:
                

                login(request, user)
                return redirect('gallery')


@login_required
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() 
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm, 'error':'Por favor ingresos los datos validos'})
     
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)  
        form = TaskForm(instance =task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)       
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form':form, 'error':'Error de actualizacion'})

@login_required
def datos(request):
    if request.method == 'GET':
        return render(request, 'datos.html', {'form': DatosForm, 'form1': ProductForm})
    else:
        try:
            form = DatosForm(request.POST)
            new_datos = form.save(commit=False)
            new_datos.user = request.user
            new_datos.save() 
            return redirect('datos')
        except ValueError:
            return render(request, 'datos.html', {'form': DatosForm, 'error':'Por favor ingresos los datos validos'})
    
@login_required
def producto(request):
    
    if request.method == 'GET':
        return render(request, 'datos.html', {'form': DatosForm, 'form1': ProductForm})
    else:
       
        try:
            form1 = ProductForm(request.POST, request.FILES)
            new_producto = form1.save(commit=False)
            new_producto.user = request.user
            new_producto.save()
          
            return redirect('datos')
        except ValueError:
            return render(request, 'datos.html', {'form1': ProductForm, 'error':'Por favor ingresos los datos validos'})
 

@login_required        
def complete_task (request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete (request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
    
@login_required
def taskcomplete (request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 

    return render(request, 'tasks.html', {'tasks': tasks})


def tienda(request):
    productos = Producto.objects.all()
    return render(request, "tienda.html", {'productos': productos})


def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("cart")
 




def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    
    carrito.eliminar(producto)
   
    return redirect("cart")
    
    
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Tienda")


def limpiar_carrito_item(request,producto_id):
    carrito = Carrito(request)
    #producto = Producto.objects.get(id=producto_id)
    carrito.limpiaritem(producto_id)
    return redirect("cart")


def galeriaprueba(request):
   
    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "home.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )




def detalleproducto(request,producto_id):
    producto = Producto.objects.get(id=producto_id)
    cat = Categoria.objects.all()
    return render(request, "productdetails.html", {'productos': producto, 'cat' : cat})
    
    
def cart(request):
    cat = Categoria.objects.all()
    precioanterior = 0
    cantidad = 0
    desc = 0
    subtotal = 0
    total_aum = 0
    preference_data = { "items": [] }
    cupon_no_encontrado = False
    cupon_encontrado = False
    descuento= 1
    nombre_cupon = 1
    
    
    
    
    if request.method == 'POST':
        nombre_cupon = request.POST.get('cupon_nombre')
        nombre_cupon = nombre_cupon.lower()
        try:
            cupon_obj = cupon.objects.get(nombre=nombre_cupon)
        
            cupon_obj.contador += 1
            cupon_obj.save()  # Guardar el cupon_obj con el contador actualizado

            descuento = cupon_obj.descuento
            cupon_no_encontrado = False
            cupon_encontrado = True
        except cupon.DoesNotExist:
            cupon_no_encontrado = True
            cupon_encontrado = False
    

    else:
        pass
    if "carrito" in request.session and request.session["carrito"]:
        for key, value in request.session["carrito"].items():
           
            precioanterior = int(value["precioanterior"])
          
           
            total_aum += int(precioanterior)
            subtotal += int(value["precio"])
            
        
        if cupon_encontrado == True:

            item = {
                        "title": value["nombre"],
                        "quantity": 1,
                        "unit_price": subtotal-(subtotal*descuento/100),
                    }
         
 
            preference_data["items"].append(item)
        
        
            total_compra = subtotal-(subtotal*descuento/100)
         
        else:
            item = {
                        "title": value["nombre"],
                        "quantity": 1,
                        "unit_price": subtotal,
                    }
         
 
            preference_data["items"].append(item)
        
            total_compra = int(subtotal)
        
        
        total_compra = round(total_compra, 2)
        sdk = mercadopago.SDK("APP_USR-5213772683732349-061323-dc5bd7f2a56c2080735653bb6d1901e7-97277305")
        preference_data["back_urls"] = {
        "success": "https://impulsocial.net/pedido/",
        "failure": "https://impulsocial.net/pendiente/",
        "pending": "https://impulsocial.net/pendiente/"
    }
        preference_data["auto_return"] = "approved"
        
        
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
      

        return render(request, "cart.html", {'preference_id': preference['id'],'cat': cat, 'precioanterior': precioanterior,'total_compra': total_compra, 'desc': desc, 'subtotal': subtotal,'desc': desc, 'total_aum': total_aum, 'cupon_encontrado': cupon_encontrado, 'cupon_no_encontrado': cupon_no_encontrado, 'descuento': descuento, 'nombrecupon': nombre_cupon} )

    else: 
        
        return redirect("gallery")
    
    
    
'''   
def cotizar(request):
    if request.method == 'POST':
        print(request)
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        direccion = request.POST.get('direccion', '')
        numero = request.POST.get('numero', '')
        ciudad = request.POST.get('ciudad', '')
        estado = request.POST.get('estado', '')
        codigo_postal = request.POST.get('codigo_postal', '')
        pais = request.POST.get('pais', '')
        telefono = request.POST.get('telefono', '')

        # Crear un diccionario con los datos recopilados
        cotizacion_data = {
            'Nombre': nombre,
            'Apellido': apellido,
            'Dirección': direccion,
            'Número': numero,
            'Ciudad': ciudad,
            'Estado': estado,
            'Código Postal': codigo_postal,
            'País': pais,
            'Teléfono': telefono,
        }

        # Imprimir los datos en la consola del servidor
        print("Información de la cotización:")
        print(cotizacion_data)

        return JsonResponse({'message': 'Cotización exitosa'})  # Puedes retornar una respuesta JSON si lo deseas

    return render(request, 'cart.html')  # Reemplaza 'tu_template.html' con la plantilla adecuada
'''

def sendmail(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
    asunto= 'Confirmación de Compra'
    cuerpo = 'Gracias por tu compra. Hemos enviado un correo de confirmación a tu dirección: ' + 'correo_destinatario'
    mensaje = f'{cuerpo}Si no recibes el correo, por favor comunícate con nosotros por WhatsApp al número +123456789.'
    cel = '11-2394-1223'
    
    subject = asunto
    message = mensaje
    from_email = 'notificaciondepaginaweb@gmail.com'
    recipient_list = ['notificaciondepaginaweb@gmail.com','maximobatallan@gmail.com']

    correo= 'correo@correo.com'
    
    send_mail(subject, message, from_email, recipient_list)
    
    return render(request, "sendmail.html", {'asunto': asunto,'mensaje': mensaje, 'correo': correo, 'cel': cel})

def datosbanco(request):
    cat = Categoria.objects.all()
    datos_relevantes = DatosPersonales.objects.filter(id=6).values('cbu', 'titular')
    cbu = datos_relevantes[0]['cbu']
    titular = datos_relevantes[0]['titular']
    
    return render(request, "datosbanco.html", {'cbu': cbu, 'titular': titular,'cat': cat,})



def catproducto(request, catproducto):
    productos = Producto.objects.filter(cat = catproducto)
    cat = Categoria.objects.all()
    return render(request, "categoriaproducto.html", {'productos': productos, 'cat': cat})

def send_user_data_email(user_data):
    subject = 'Impulsocial Consulta'
    message = f'{user_data}'
    

    from_email = 'notificaciondepaginaweb@gmail.com'
    recipient_list = ['notificaciondepaginaweb@gmail.com','maximobatallan@gmail.com']
    send_mail(subject, message, from_email, recipient_list)


@csrf_exempt
def save_formulario(request):
    

    nombre = request.POST.get('nombre')

    telefono = request.POST.get('telefono')
    email = request.POST.get('email')
    texto = request.POST.get('texto')
    categoria = request.POST.get('categoria')
    
    
    formulario1 = formulario(nombre=nombre, categoria=categoria, telefono=telefono, mail=email, texto=texto)
    formulario1.save()
    user_data = f"nombre: {nombre} telefono: {telefono} texto: {texto}"
    send_user_data_email(user_data)
    
    
    
    return render(request, 'formularioconfirmacion.html')


def banner1 (request):

    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "x.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

def banner2 (request):

    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "threads.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

def banner3 (request):

    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "instagram.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

def banner4 (request):

    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "tiktok.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

def banner5 (request):

    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "facebook.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

def banner6 (request):

    productos = Producto.objects.filter(important=True)
    cat = Categoria.objects.all()

    # Creamos un diccionario para agrupar los productos por categoría
    categorias_productos = {}
    
    for producto in productos:
        id = producto.id
        categoria = producto.cat
     

        if categoria in categorias_productos:
            categorias_productos[categoria].append(id)
        else:
            categorias_productos[categoria] = [id]
    
  
   
    return render(request, "youtube.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )




def nuevacompra(user_data):
    subject = 'Nueva Venta, ImpulSocial'
    message = f'{user_data}'
    

    from_email = 'notificaciondepaginaweb@gmail.com'
    recipient_list = ['notificaciondepaginaweb@gmail.com','maximobatallan@gmail.com']
    send_mail(subject, message, from_email, recipient_list)

def pedido (request):

    try:
        productos_para_comprar = []
        query_params = request.GET    # Comprobamos si el parámetro payment_id está presente en los query params
        payment_id = query_params.get('preference_id')
        params_list = []

    
        for key, value in query_params.items():
            params_list.append({key: value})


        

        if "carrito" in request.session and request.session["carrito"]:
                for key, value in request.session["carrito"].items():
                
                    producto_id = str(value["producto_id"])
                    cantidad = int(value["cantidad"])
                    link = str(value["link"])
                    codigo = value["codigo"]
                    precio  = int(value["precio"])
                    nombre = str(value["nombre"])

    
                    url = f"https://growfollows.com/api/v2?key=09712c94e11bdb6a8240734518511373&action=add&service={codigo}&link={link}&quantity={cantidad}"


                    producto = {
                    'cantidad': cantidad,
                    'link': link,
                    'nombre': nombre
                    }
                    productos_para_comprar.append(producto)


                    response = requests.request("POST", url)
                    
                    compra1 = compra(producto_id=producto_id, codigo=codigo, cantidad=cantidad, precio=precio, link=link, orden=payment_id)
                    compra1.save()


        user_data = f"{request.session['carrito'].items()}, Datos Mercadolibre {params_list}"
        
        nuevacompra(user_data)

        carrito = Carrito(request)
        carrito.limpiar()
   
        return render(request, "pedido.html", {'producto_id': producto_id, 'cantidad': cantidad, 'productos_para_comprar': productos_para_comprar } )
    except:
        productos = Producto.objects.filter(important=True)
        cat = Categoria.objects.all()


        # Creamos un diccionario para agrupar los productos por categoría
        categorias_productos = {}
        
        for producto in productos:
            id = producto.id
            categoria = producto.cat
        

            if categoria in categorias_productos:
                categorias_productos[categoria].append(id)
            else:
                categorias_productos[categoria] = [id]
    
   

        return render(request, "home.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

def pendiente (request):

    try:
        productos_para_comprar = []
        query_params = request.GET    # Comprobamos si el parámetro payment_id está presente en los query params
        payment_id = query_params.get('preference_id')
        params_list = []

    
        for key, value in query_params.items():
            params_list.append({key: value})


        print ("pendiente")

        if "carrito" in request.session and request.session["carrito"]:
                for key, value in request.session["carrito"].items():
                
                    producto_id = str(value["producto_id"])
                    cantidad = int(value["cantidad"])
                    link = str(value["link"])
                    codigo = value["codigo"]
                    precio  = int(value["precio"])
                    nombre = str(value["nombre"])

    
                

                    producto = {
                    'cantidad': cantidad,
                    'link': link,
                    'nombre': nombre
                    }
                    productos_para_comprar.append(producto)


                    
                    compra1 = compra(producto_id=producto_id, codigo=codigo, cantidad=cantidad, precio=precio, link=link, orden=payment_id)
                    compra1.save()


        user_data = f"{request.session['carrito'].items()}, Datos Mercadolibre {params_list}"
        
        nuevacompra(user_data)

   
        return render(request, "pendiente.html", {'producto_id': producto_id, 'cantidad': cantidad, 'productos_para_comprar': productos_para_comprar } )
    except:
        productos = Producto.objects.filter(important=True)
        cat = Categoria.objects.all()


        # Creamos un diccionario para agrupar los productos por categoría
        categorias_productos = {}
        
        for producto in productos:
            id = producto.id
            categoria = producto.cat
        

            if categoria in categorias_productos:
                categorias_productos[categoria].append(id)
            else:
                categorias_productos[categoria] = [id]
    
   

        return render(request, "home.html", {'categorias_productos': categorias_productos, 'productos': productos, 'cat': cat} )

