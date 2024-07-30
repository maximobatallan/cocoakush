from django.shortcuts import render, get_object_or_404
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

    def agregar(self, producto, talle, color):

        
        id = str(producto.id)


     
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id": producto.id,
                "nombre": f"{producto.nombre} - {talle}",
                "color": color,                
                "talle": talle,
                "acumulado": producto.precio,
                "cantidad": 1,
                "imagen": str(producto.imagen),
                "precio": producto.precio,
                "precioanterior": int(producto.precio *1.25),
            }
       
        else:
            nombre_producto = f"{self.carrito[id]['nombre']} {talle}"
            self.carrito[id]["nombre"] = nombre_producto
      
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.precio
            
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
        
        self.eliminar(producto)
        self.session.modified = True
