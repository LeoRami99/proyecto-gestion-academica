
// Jquery de DataTables para la tabla de docentes
$(document).ready( function () {
  $('#tabla_docentes').DataTable({
      "fixedColumns": {
          "leftColumns": 1
      },
      "scrollX": true,
      "scrollY": "500px",
      "scrollCollapse": true,

      "aLengthMenu":[[5,10,25,-1],[5,10,24], "todo"],
      "iDisplayLength":5,
      "language":{
          "lengthMenu": "Mostrar _MENU_ registros por página",
          "search": "Buscar",
          "zeroRecords":"Ningún Registro Encontrado",
          "info":"Página _PAGE_ de _PAGES_",
          "infoEmpty": "Ningún registro disponible",
          "infoFiltered":"(Filtrado de _MAX_ registro(s) totales)",
          "paginate":{
              "first":"Primero",
              "last":"Ultimo",
              "next":"Siguiente",
              "previous": "Anterior"
          }
      },
  });
} );

// Jquery de DataTables para la tabla de de asistencia de estudiantes
// Jquery de DataTables para la tabla de docentes
$(document).ready( function () {
    $('#tabla_asistencia_estudiante').DataTable({
        "fixedColumns": {
            "leftColumns": 3
        },
        "scrollX": true,
        "scrollY": "500px",
        "scrollCollapse": true,
  
        "aLengthMenu":[[5,10,25,-1],[5,10,24], "todo"],
        "iDisplayLength":5,
        "language":{
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "search": "Buscar",
            "zeroRecords":"Ningún Registro Encontrado",
            "info":"Página _PAGE_ de _PAGES_",
            "infoEmpty": "Ningún registro disponible",
            "infoFiltered":"(Filtrado de _MAX_ registro(s) totales)",
            "paginate":{
                "first":"Primero",
                "last":"Ultimo",
                "next":"Siguiente",
                "previous": "Anterior"
            }
        },
    });
  } );
  
  $(document).ready( function () {
    $('#tabla_calificaciones_estudiante').DataTable({
        "fixedColumns": {
            "leftColumns": 3
        },
        "scrollX": true,
        "scrollY": "500px",
        "scrollCollapse": true,
  
        "aLengthMenu":[[5,10,25,-1],[5,10,24], "todo"],
        "iDisplayLength":5,
        "language":{
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "search": "Buscar",
            "zeroRecords":"Ningún Registro Encontrado",
            "info":"Página _PAGE_ de _PAGES_",
            "infoEmpty": "Ningún registro disponible",
            "infoFiltered":"(Filtrado de _MAX_ registro(s) totales)",
            "paginate":{
                "first":"Primero",
                "last":"Ultimo",
                "next":"Siguiente",
                "previous": "Anterior"
            }
        },
    });
  } );
  