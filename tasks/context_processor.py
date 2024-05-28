def total_carrito(request):
    total = 0
    cantidad = 0
    contar = 0
    

    if "carrito" in request.session.keys():
        carrito = request.session['carrito']
        contar = len(carrito)
        for key, value in request.session["carrito"].items():
            
            total += int(value["acumulado"])
            cantidad += int(value["cantidad"])
         
                
    return {"total_carrito": total,"cantidad": cantidad, "contar": contar}
