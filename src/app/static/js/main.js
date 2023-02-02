console.log('%c¡Alto! ', 'color: red; font-size: 40px');
console.log('%cEste es un espacio para desarrolladores. No intentes nada fuera de lo normal. ', 'color: red; font-size: 20px');

// Jquery de DataTables para la tabla de docentes
$(document).ready(function () {
  $("#tabla_docentes").DataTable({
    fixedColumns: {
      leftColumns: 1,
    },
    // color de las letras de la tabla 
    
    scrollX: true,
    scrollY: "500px",
    scrollCollapse: true,

    aLengthMenu: [[5, 10, 25, -1], [5, 10, 20, 50], "todo"],
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

    aLengthMenu: [[5, 10, 25, -1], [5, 10, 20, 50], "todo"],
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
    // agregar un tamaño fijo a la tabla
    
    
    scrollX: true,
    scrollCollapse: true,
    // agregarle estilos
    

    aLengthMenu: [[5, 10, 25, -1], [5, 10, 20, 50], "todo"],
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
  $("#tabla_curso").DataTable({
    scrollX: true,
    scrollCollapse: true,
  //  Fijar la ultima columna
    fixedColumns: {
      leftColumns: 0,
    },
    aLengthMenu: [[5, 10, 25, -1], [5, 10, 20, 50], "todo"],
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
  $("#tabla_curso_cerrado").DataTable({
    scrollX: true,
    scrollCollapse: true,
  //  Fijar la ultima columna
    fixedColumns: {
      leftColumns: 0,
    },
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
  $("#tabla_asistencia_calificaciones").DataTable({
    aLengthMenu: [[5, 10, 25, -1], [5, 10, 20, 50], "todo"],
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



// // Recorrer las filas de la tabla
// $(document).ready(function() {
//   // Asignar el evento "change" a todos los campos de calificaciones
//   $("input[name^='calif_']").on("change", function() {
//       // Obtener la fila de la tabla donde se encuentra el campo modificado
//       var row = $(this).closest("tr");
//       // Inicializar las sumas de las calificaciones en 0
//       var sum_corte_1 = 0;
//       var sum_corte_2 = 0;
//       var sum_corte_3 = 0;
//       // Recorrer las columnas de calificaciones del primer corte
//       row.find("input[name='calif_1'], input[name='calif_2'], input[name='calif_3']").each(function() {
//           // Sumar los valores de las calificaciones
//           sum_corte_1 += parseFloat($(this).val());
//       });
//       // Recorrer las columnas de calificaciones del segundo corte
//       row.find("input[name='calif_4'], input[name='calif_5'], input[name='calif_6']").each(function() {
//           // Sumar los valores de las calificaciones
//           sum_corte_2 += parseFloat($(this).val());
//       });
//       // Recorrer las columnas de calificaciones del tercer corte
//       row.find("input[name='calif_7'], input[name='calif_8'], input[name='calif_9']").each(function() {
//           // Sumar los valores de las calificaciones
//           sum_corte_3 += parseFloat($(this).val());
//       });
//       // Calcular el promedio final multiplicando cada corte por su porcentaje y sumando los resultados
//       var average = ((sum_corte_1/3) * 0.3) + ((sum_corte_2/3) * 0.3) + ((sum_corte_3/3) * 0.4);
//       // Actualizar el valor de la columna "Calificación final" con el promedio calculado
//       row.find("input[name='calif_10']").val(average.toFixed(2));
//     });
// });
// $(document).ready(function() {
//   $("input[name='calif_10']").attr("readonly", true);
// });

$(document).ready(function() {
  $("input[name^='calif_'][name!='calif_10']").on("change", function() {  
      var parametro_nota = document.getElementById("parametro_nota").value;
      var row = $(this);
      var suma_total = 0;
      row.closest("tr").find("input[name='calif_1'], input[name='calif_2'], input[name='calif_3'], input[name='calif_4'], input[name='calif_5'], input[name='calif_6'], input[name='calif_7'], input[name='calif_8'], input[name='calif_9']").each(function() {
        suma_total += parseFloat($(this).val());
      }
      );
      var promedio = suma_total/parametro_nota;
      row.closest("tr").find("input[name='calif_10']").val(promedio.toFixed(2));
      
      
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
    scroll: true,
    scrollX: true,
    scrollY: "500px",
    scrollCollapse: true,


    aLengthMenu: [[5, 10, 25, -1], [5, 10, 20, 50], "todo"],
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

const buttons = document.querySelectorAll(".btn-card");
const colors = ['#ff6961','#77dd77','#84b6f4'];

for (let i = 0; i < buttons.length; i++) {
    const originalColor = buttons[i].style.backgroundColor;
    buttons[i].addEventListener("mouseover", function() {
    this.style.backgroundColor = getRandomColor();
  });
    buttons[i].addEventListener("mouseout", function() {
    this.style.backgroundColor = originalColor;
  });
}

function getRandomColor() {
  let randomNum = Math.floor(Math.random() * 3);
  return colors[randomNum];
}










