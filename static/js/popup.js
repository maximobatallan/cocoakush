
   // Espera a que el DOM esté listo
   document.addEventListener("DOMContentLoaded", function() {
     // Obtén el enlace
     var enlaceObjetivo = document.getElementById("enlaceObjetivo");
 
     // Agrega un controlador de eventos clic al enlace
     enlaceObjetivo.addEventListener("click", function(event) {
       // Previene el comportamiento predeterminado del enlace
       event.preventDefault();
       // Muestra el modal
       $('#miModal').modal('show');
     });
   });
