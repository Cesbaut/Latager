//VARIABLES GENERALES Y EXPLICACION
//materias: contienen un json que muestra las materias del usuario junto con sus grupos (se usa en la parte derecha)
//gruposUsuario: json con los grupos actuales que tiene el usuario
const csrfmiddlewaretoken = document.querySelector('[name="csrfmiddlewaretoken"]').value; //token

let gruposUsuario1;

// ***** AL INICIAR LA PAGINA *****
document.addEventListener('DOMContentLoaded', function() {
  console.log(materias)

  actualizarMaterias(); 
  gruposUsuario1 = new grupoCalendario(gruposUsuario)
  console.log(gruposUsuario1.datos)
  if(Object.keys(gruposUsuario1.datos).length>0){
    gruposUsuario1.datos.forEach(grupoUsu => {
      const materia = materias[grupoUsu.materia];
        materia.grupos.forEach(key => {
            if (key.id === grupoUsu.grupo_id) {
              agregarEvento(key, materia.materia);
            }
        });
    });
  }
  var materiasContainer  = document.querySelector('.materias');
  Sortable.create(materiasContainer, {
      animation: 150, 
      chosenClass: "chosen", 
      ghostClass: "ghost",
      dragClass: "drag",   
      draggable: ".materia-item",
      onEnd: () => {
          console.log('Se movió un elemento');
      }
  });
})



// ***** GRUPOSUSUARIO ***** */
class grupoCalendario{
  constructor(gruposUsuario){
    this._gruposUsuario=gruposUsuario;
  }

  get datos(){
    return this._gruposUsuario;
  }

  //Funcion para agregar un grupo a gruposUsuario
  agregarGrupo(materia, grupo) {
    console.log(materia, grupo);
    const existeGrupo = this._gruposUsuario.some(grupoExistente => 
      grupoExistente.materia === materia && grupoExistente.grupo_id === grupo
    );
    if (!existeGrupo) {
      this._gruposUsuario.push({ materia, grupo_id: grupo });
      console.log('Grupo agregado');
    } else {
      console.log('Este grupo ya existe');
    }
  }

  //Funcion para eliminar un grupo de gruposUsuario
  eliminarGrupo(materia, grupo) {
    console.log(materia, grupo);
    
    this._gruposUsuario = this._gruposUsuario.filter(p => !(p.materia == materia && p.grupo_id == grupo));

    calendar.getEvents().forEach(event => {
      console.log(event.extendedProps);
      if ((event.extendedProps.grupo_id == grupo)&&(event.extendedProps.clave==materia)) {
        event.remove();
      }
    });
    console.log(this._gruposUsuario)
  }

  async guardarGrupos() {
    try {
      const response = await fetch('/guardarGrupos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfmiddlewaretoken
        },
        body: JSON.stringify({ gruposUsuario: this._gruposUsuario }) 
      });
  
      const data = await response.json();
      if (data.message){
        mensajeExitoGuardado(data.message);
      }
      else{
        mensajeErrorGuardado(data.error)
      }
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }
}




//Funcion auxiliar para agregar un evento y convertirlo en json
function agregarEventoDesdeHTML(element) {
  const grupoJSON = element.getAttribute('data-grupo');
  const materiaJSON = element.getAttribute('data-materia');

  const grupo = JSON.parse(grupoJSON);
  const materia = JSON.parse(materiaJSON);
  gruposUsuario1.agregarGrupo(materia.clave, grupo.id)
  console.log(gruposUsuario1.datos)
  agregarEvento(grupo, materia);
}

// Función para convertir los días y horas en eventos
function agregarEvento(grupo, materia) {
  const diasSemana = {
    Lun: '2024-09-02',
    Mar: '2024-09-03',
    Mie: '2024-09-04',
    Jue: '2024-09-05',
    Vie: '2024-09-06',
    Sab: '2024-09-07',
    Dom: '2024-09-08'
  };

  const dias = grupo.dias.split(', ');
  const [horaInicio, horaFin] = grupo.horas.split(' a ');


  dias.forEach(dia => {
    const fecha = diasSemana[dia];
    let materiaNom = materia.nombre.slice(0, 20);
    let profesor = grupo.nombre.slice(0, 15);
    if (fecha) {
      calendar.addEvent({
        id: grupo.id,
        title: `${materiaNom} - ${grupo.grupo} - ${grupo.nombre} - ${grupo.salon}`, // Mostrar nombre y grupo
        start: `${fecha}T${horaInicio}:00`,
        end: `${fecha}T${horaFin}:00`,
        backgroundColor: materia.color,
        borderColor: '#000',
        extendedProps: {
          nombre: `${grupo.nombre}`,
          grupo: `${grupo.grupo}`,
          grupo_id: `${grupo.id}`,
          tipo: `${grupo.tipo}`,
          horas: `${grupo.horas}`,
          dias: `${grupo.dias}`,
          salon:`${grupo.salon}`,
          cupo: `${grupo.cupo}`,
          calificacion: `${grupo.calificacion}`,
          materia: `${materia.nombre}`,
          color: `${materia.color}`,
          clave: `${materia.clave}`,
        }
      });
    }
  });
}




/* ***** CALENDARIO ***** */

// Incializacion de calendario
var calendarEl = document.getElementById('calendar');
var startOfWeek = '2024-09-02'; 
var endOfWeek = '2024-09-08';   
var calendar = new FullCalendar.Calendar(calendarEl, {
  initialView: 'timeGridWeek',
  timeZone: 'America/Mexico_City',
  locale: 'mx',
  fixedWeekCount:false,
  editable:false,
  dayHeaderFormat: { weekday: 'short' },
  visibleRange: {
      start: startOfWeek,
      end: endOfWeek
    },
    slotMinTime: '07:00:00', 
    slotMaxTime: '22:00:00',
    allDaySlot: false,
  viewDidMount: function(info) {
    let startDate = new Date(startOfWeek);
    info.view.calendar.gotoDate(startDate);
  },
  
  eventDidMount: function(info) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip-event';
    tooltip.innerHTML = `
      <strong>Nombre:</strong> ${info.event.extendedProps.nombre}<br>
      <strong>Grupo:</strong> ${info.event.extendedProps.grupo}<br>
      <strong>Tipo:</strong> ${info.event.extendedProps.tipo}<br>
      <strong>Horas:</strong> ${info.event.extendedProps.horas}<br>
      <strong>Días:</strong> ${info.event.extendedProps.dias}<br>
      <strong>Salon:</strong> ${info.event.extendedProps.salon}<br>
      <strong>Cupo:</strong> ${info.event.extendedProps.cupo}<br>
      <strong>Calificación:</strong> ${info.event.extendedProps.calificacion}<br>
      <strong>Materia:</strong> ${info.event.extendedProps.materia}<br>
    `;
    tooltip.style.position = 'absolute';
    tooltip.style.background = `${info.event.extendedProps.color}`;
    tooltip.style.border = '1px solid #ccc';
    tooltip.style.padding = '8px';
    tooltip.style.borderRadius = '5px';
    tooltip.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
    tooltip.style.display = 'none';
    tooltip.style.zIndex = '1000';

    document.body.appendChild(tooltip);

    info.el.addEventListener('mouseenter', () => {
      tooltip.style.display = 'block';
      tooltip.style.top = `${info.el.getBoundingClientRect().top + window.scrollY + 20}px`;
      tooltip.style.left = `${info.el.getBoundingClientRect().left}px`;
    });

    info.el.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });

    info.el.addEventListener('dblclick', function() {
      gruposUsuario1.eliminarGrupo(info.event.extendedProps.clave, info.event.extendedProps.grupo_id)
      tooltip.remove();
      if (informacionGrupos.style.display == 'flex'){
        mostrarGrupos(info.event.extendedProps.clave)
      }
    });
  }
  
})
calendar.render();

// Obtener todos los eventos actuales del calendario
function obtenerEventosCalendario() {
  let eventos = calendar.getEvents(); 
  let eventosJSON = eventos.map(event => {
    return {
      id: event.id,                    
      title: event.title,               
      start: event.start.toISOString(),
      end: event.end ? event.end.toISOString() : null, 
      color: event.backgroundColor,    
      extendedProps: {                  
        grupo: event.extendedProps.grupo,
        tipo: event.extendedProps.tipo,
        horas: event.extendedProps.horas,
        dias: event.extendedProps.dias,
        cupo: event.extendedProps.cupo,
        calificacion: event.extendedProps.calificacion,
        materia: event.extendedProps.materia,
      }
    };
  });

  return JSON.stringify(eventosJSON, null, 2);
}








/* ***** MATERIAS ***** */

//Funcion para eliminar una materia de un usuario
async function eliminarMateria(clave) {
  try {
    const response = await fetch('/deleteMateriaUsuario/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfmiddlewaretoken
      },
      body: new URLSearchParams({
        clave: clave,
      })
    });
    const data = await response.json();
    delete materias[clave];
    actualizarMaterias();
    mensajeExito('Materia eliminada con éxito')
    return;
  } catch (error) {
    mensajeError(error)
    return;
  }
}


modalEliminar = (nombre, clave)=> openModal(`
  <div>
    <h2>¿Estas seguro de eliminar ${nombre}?</h2>
    <p>Esta acción tambien eliminara los grupos añadidos de esta materia</p>
  </div>
  <div>
    <button class="boton-gris" onclick="closeModal()">
      Cancelar
    </button>
    <button class="boton-rojo" onclick="eliminarMateria('${clave}')">
      Eliminar
    </button>
  </div>
  `);
//Funcion para actualizar las materias
function actualizarMaterias(){
  materiasID.innerHTML = '';
  for (let key in materias) {
    const materia = materias[key].materia;
    
    materiasID.innerHTML += `<div class="materia materia-item" style="background-color: ${materia.color};">
                              <p>${materia.nombre}</p>
                              <div class="btns">
                                <button class="btn-danger" onclick="modalEliminar('${materia.nombre}', '${materia.clave}')">
                                  <img class="imagen imagen1" src="/static/horarios/img/delete.svg" alt="">
                                </button>
                                <button class="btn-groups" onclick="mostrarGrupos('${materia.clave}')">
                                  <img src="/static/horarios/img/right_info.png" alt="" srcset="">
                                </button>
                              </div>
                            </div>`;
  }
}

//Funcion para mostrar los grupos de una materia
function mostrarGrupos(ClaveMateria){
  busqueda.style.display = 'none';
  informacionGrupos.style.display = 'flex';

  informacionGrupos.style.backgroundColor = `${materias[ClaveMateria].materia.color}`
  informacionGrupos.innerHTML = `

  <div class="div-captions">
    <button  id="btn-regresar" class="btns-materia" onclick="regresar()">
      <img src="/static/horarios/img/back.svg" alt="" srcset="">
    </button>
    <h2>${materias[ClaveMateria].materia.nombre}</h2>
    <button id="btn-actualizar" class="btns-materia" onclick="actualizar(${ClaveMateria})">
      <img id="btn-actualizar-imagen" src="/static/horarios/img/reload.svg" alt="available-updates">    
    </button>
  </div>
  <table>
        <thead>
            <tr >
                <th>G</th>
                <th>Nombre</th>
                <th>T</th>
                <th>H</th>
                <th>D</th>
                <th>S</th>
                <th>C</th>
                <th>Calif</th>
                <th id="Subir">Subir</th>
            </tr>
        </thead>
        <tbody id="infoGrupo">

        </tbody>
    </table>
    `
    for (let grupo of materias[ClaveMateria].grupos) {
      console.log(grupo.grupo)
      if (gruposUsuario1.datos.some(item => item.grupo_id === grupo.id)){
        SubirStatus = `<td class="btn-status" 
                        onclick="gruposUsuario1.eliminarGrupo(${materias[ClaveMateria].materia.clave}, ${grupo.id}); mostrarGrupos(${ClaveMateria})">
                          <img src="/static/horarios/img/palomita.svg" alt="" srcset="">
                      </td>`
      }
      else{
        SubirStatus = `<td class="btn-add" 
                        data-grupo='${JSON.stringify(grupo).replace(/'/g, '&#39;')}' 
                        data-materia='${JSON.stringify(materias[ClaveMateria].materia).replace(/'/g, '&#39;')}' 
                        onclick="agregarEventoDesdeHTML(this), mostrarGrupos(${ClaveMateria})">
                          <img src="/static/horarios/img/right_info.png" alt="" srcset="">
                      </td>`
      }
      let infoGrupo = document.querySelector('#infoGrupo');
      infoGrupo.innerHTML += `<tr class="${grupo.cupo > 0 ? 'con-cupo' : 'sin-cupo'}">
                                <td>${grupo.grupo}</td>
                                <td>${grupo.nombre}</td>
                                <td>${grupo.tipo}</td>
                                <td>${grupo.horas}</td>
                                <td>${grupo.dias}</td>
                                <td>${grupo.salon}</td>
                                <td>${grupo.cupo}</td>
                                <td>${grupo.calificacion}</td>
                                ${SubirStatus}
                              </tr>`
    }
    informacionGrupos.innerHTML += `
  
  `;
}






/* ***** FUNCIONALIDADES ***** */

//Clickear en el input radio al clickear en el input text o number
numberField.addEventListener('click', ()=>{
  numberRadio.checked = true;
})
textField.addEventListener('click', ()=>{
  textRadio.checked = true;
})

//Cuando se pide una materia por el formulario
form_materia.addEventListener('submit',async (event) => {
  event.preventDefault();

  const tipoBusqueda = document.querySelector("input[name='tipoBusqueda']:checked").value;
  const numero = document.querySelector("input[name='numero']").value;
  const cadena = document.querySelector("input[name='cadena']").value;
  const csrfmiddlewaretoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
  
  if (numero == '' && cadena == '') {
    mensajeError('Favor de llenar todos los campos')
    return;
  }
  if (materias[numero]) {
    mensajeError('La materia ya fue registrada')
    return
  }
  const data = await MateriayGrupo(tipoBusqueda, numero, cadena, csrfmiddlewaretoken);
  if (data.message == 'Materia registrada') {
    materias[data.materia.clave] = {"materia": data.materia, "grupos": data.grupos};
    mensajeExito(data.message)
    materiasID.innerHTML = '';
    actualizarMaterias();
  }
  else {
    mensajeError(data.message)
  } 
});

// Función para actualizr una materia
async function actualizar(materia_clave) {
  let btn_actualizar_imagen = document.getElementById("btn-actualizar-imagen")
  const imagenOriginal = btn_actualizar_imagen.src;
  const nuevaImagen = "/static/horarios/img/reloadGIF2.gif"; 
  btn_actualizar_imagen.src = nuevaImagen;
  try {
    const response = await fetch(`/actualizarMateria/${materia_clave}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfmiddlewaretoken  
      },
    });
    const data = await response.json();
    if (response.ok) {
      console.log("Materia actualizada correctamente.");
      console.log(data);
      const id = Object.keys(data.materiaNueva)[0]; // "1645"
      const idNumber = Number(id); // 1645 (convertido a número)
      console.log(idNumber);
      materias[idNumber] = data.materiaNueva[id];
      console.log(materias)
      mostrarGrupos(materia_clave)

    } else {
      console.error("Error al actualizar la materia.");
    }
    btn_actualizar_imagen.src = imagenOriginal;
  } catch (error) {
    console.error("Error en la solicitud:", error);
  }
}

// Función para regresar al estado anterior
function regresar() {
  informacionGrupos.style.display = 'none';
  busqueda.style.display = 'flex';
}

//Funcion para mostrar un mensaje de exito
function mensajeExito(mensaje){
  Noticias.style.display = 'Flex';
  Noticias.style.backgroundColor = '#ffffb6'
  Noticias.innerHTML = `${mensaje}`;
  
  setTimeout(() => {
    Noticias.style.display = 'None';
  }, 3000);
}

//Funcion para mostrar un mensaje de error
function mensajeError(mensaje){
  Noticias.style.display = 'Flex';
  Noticias.style.backgroundColor = '#ffb6b6';
  Noticias.innerHTML = `${mensaje}`;
  
  setTimeout(() => {
    Noticias.style.display = 'None';
    Noticias.style.backgroundColor = '#ffffb6'
  }, 3000);
}

let mensajeSave = document.getElementById("mensajeSave")
function mensajeExitoGuardado(mensaje){
  mensajeSave.style.display = 'Flex';
  mensajeSave.style.backgroundColor = '#ffffb6'
  mensajeSave.innerHTML = `${mensaje}`;
  
  setTimeout(() => {
    mensajeSave.style.display = 'None';
  }, 3000);
}


//Funcion para mostrar un mensaje de error
function mensajeErrorGuardado(mensaje){
  mensajeSave.style.display = 'Flex';
  mensajeSave.style.backgroundColor = '#ffb6b6';
  mensajeSave.innerHTML = `${mensaje}`;
  
  setTimeout(() => {
    mensajeSave.style.display = 'None';
    mensajeSave.style.backgroundColor = '#ffffb6'
  }, 3000);
}

// Función para obtener los datos de una materia y sus grupos
async function MateriayGrupo(tipoBusqueda, numero, cadena, csrfmiddlewaretoken) {
  try {
    const response = await fetch('/formulario_maestros/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfmiddlewaretoken
      },
      body: new URLSearchParams({
        tipoBusqueda: tipoBusqueda,
        numero: numero,
        cadena: cadena
      })
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}



// ***** MODAL *****
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");
const openModalBtn = document.querySelector(".btn-open");
const informacionModal = document.getElementById("informacionModal"); 

// Cerrar modal
const closeModal = function () {
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
};
overlay.addEventListener("click", closeModal);

// Cerrar en Esc
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

// Abrir modal
const openModal = function ( text ) {
  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  informacionModal.innerHTML = text;
};



