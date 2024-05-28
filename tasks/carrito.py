import random
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, link, producto, cantidad):
        

        

        id = str(producto.id)

        
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "codigo": producto.descripcion,
                "acumulado": cantidad *producto.precio,
                "cantidad": cantidad,
                "link": link,
                "imagen": str(producto.imagen),
                "precio": producto.precio,
                "precio2": producto.precio2,
                "precio3": producto.precio3,
                "precio4": producto.precio4,
                "precio5": producto.precio5,
                
                
                
                "precioanterior": int(producto.precio *1.25),
            }
       
        else:
           
            id = str(int(id)+random.randint(1,100000))
            self.carrito[id]={
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "acumulado": cantidad *producto.precio,
                "codigo": producto.descripcion,
                "cantidad": cantidad,
                "link": link,
                "imagen": str(producto.imagen),
                "precio": producto.precio,
                "precio2": producto.precio2,
                "precio3": producto.precio3,
                "precio4": producto.precio4,
                "precio5": producto.precio5,
                "precioanterior": int(producto.precio *1.25),
            }

        if cantidad <= 500:
            
            
            self.carrito[id]["precio"] = self.carrito[id]["precio"]
            
        elif 500 < cantidad <= 1000:
          
            self.carrito[id]["precio"] = self.carrito[id]["precio2"]



        elif 1000 < cantidad <= 2000:
           


            self.carrito[id]["precio"] = self.carrito[id]["precio3"]



        elif  2000 < cantidad <= 5000:
            
            self.carrito[id]["precio"] = self.carrito[id]["precio4"]
        else:

            
            self.carrito[id]["precio"] = self.carrito[id]["precio5"]
    

 




        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.precio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
        
    def limpiaritem(self, producto):
        self.eliminar(str(producto))
        self.session.modified = True