// Jquery de DataTables para la tabla de docentes
$(document).ready(function () {
  $("#tabla_docentes").DataTable({
    fixedColumns: {
      leftColumns: 1,
    },
    scrollX: true,
    scrollY: "500px",
    scrollCollapse: true,

    aLengthMenu: [[5, 10, 25, -1], [5, 10, 24], "todo"],
    iDisplayLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros por página",
      search: "Buscar",
      zeroRecords: "Ningún Registro Encontrado",
      info: "Página _PAGE_ de _PAGES_",
      infoEmpty: "Ningún registro disponible",
      infoFiltered: "(Filtrado de _MAX_ registro(s) totales)",
      paginate: {
        first: "Primero",
        last: "Ultimo",
        next: "Siguiente",
        previous: "Anterior",
      },
    },
  });
});

// Jquery de DataTables para la tabla de de asistencia de estudiantes
// Jquery de DataTables para la tabla de docentes
$(document).ready(function () {
  $("#tabla_asistencia_estudiante").DataTable({
    fixedColumns: {
      leftColumns: 3,
    },
    scrollX: true,
    scrollY: "500px",
    scrollCollapse: true,

    aLengthMenu: [[5, 10, 25, -1], [5, 10, 24], "todo"],
    iDisplayLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros por página",
      search: "Buscar",
      zeroRecords: "Ningún Registro Encontrado",
      info: "Página _PAGE_ de _PAGES_",
      infoEmpty: "Ningún registro disponible",
      infoFiltered: "(Filtrado de _MAX_ registro(s) totales)",
      paginate: {
        first: "Primero",
        last: "Ultimo",
        next: "Siguiente",
        previous: "Anterior",
      },
    },
  });
});

$(document).ready(function () {
  $("#tabla_calificaciones_estudiante").DataTable({
    fixedColumns: {
      leftColumns: 3,
    },
    scrollX: true,
    scrollY: "500px",
    scrollCollapse: true,

    aLengthMenu: [[5, 10, 25, -1], [5, 10, 24], "todo"],
    iDisplayLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros por página",
      search: "Buscar",
      zeroRecords: "Ningún Registro Encontrado",
      info: "Página _PAGE_ de _PAGES_",
      infoEmpty: "Ningún registro disponible",
      infoFiltered: "(Filtrado de _MAX_ registro(s) totales)",
      paginate: {
        first: "Primero",
        last: "Ultimo",
        next: "Siguiente",
        previous: "Anterior",
      },
    },
  });
});

// Restringir el uso de la consola del navegador
// document.addEventListener("contextmenu", (event) => event.preventDefault());
// document.addEventListener("keydown", (event) => {
//   if (event.ctrlKey && event.shiftKey && event.keyCode == "I".charCodeAt(0)) {
//     event.preventDefault();
//   }
//   if (event.ctrlKey && event.shiftKey && event.keyCode == "J".charCodeAt(0)) {
//     event.preventDefault();
//   }
//   if (event.ctrlKey && event.keyCode == "U".charCodeAt(0)) {
//     event.preventDefault();
//   }
// });

$(document).ready(function () {
  $("#tabla_estudiante").DataTable({
    aLengthMenu: [[5, 10, 25, -1], [5, 10, 24], "todo"],
    iDisplayLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros por página",
      search: "Buscar",
      zeroRecords: "Ningún Registro Encontrado",
      info: "Página _PAGE_ de _PAGES_",
      infoEmpty: "Ningún registro disponible",
      infoFiltered: "(Filtrado de _MAX_ registro(s) totales)",
      paginate: {
        first: "Primero",
        last: "Ultimo",
        next: "Siguiente",
        previous: "Anterior",
      },
    },
  });
});
// cuando carga la tabla se ve cortada, por eso se usa el scrollX





