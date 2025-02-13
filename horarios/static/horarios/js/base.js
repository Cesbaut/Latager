


document.addEventListener('DOMContentLoaded', function() {
    const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    // const btnSwitch = document.querySelector("#switch")
    let logoImg = document.querySelector("#logo")
    let icono_path = document.querySelectorAll(".icono_path");
    let icono_fill = document.querySelectorAll(".icono_fill")
    let to_do = document.querySelector(".to-do")
    const logoImage = document.getElementById('logoImage');
    let calendario = document.querySelector(".calendario")
    let informacionUsuario = document.querySelector("#informacionUsuario")
    let sesion_configuracion = document.querySelector("#sesion_configuracion")
    let aspecto_opciones = document.querySelector("#aspecto_opciones")
    let Layer_1 = document.querySelector("#Layer_1")
    let right_opciones = document.querySelector("#right_opciones")
    let Aspecto = document.querySelector("#Aspecto")
    
    function acciones(){
        document.body.classList.toggle("dark");
        // btnSwitch.classList.toggle("active");
        if (to_do) {
            to_do.classList.toggle("dark");
        }
        if (calendario){
            calendario.classList.toggle("dark");
        }
        if (informacionUsuario){
            informacionUsuario.classList.toggle("dark");
            console.log(informacionUsuario.style.backgroundColor)
            if (informacionUsuario.style.backgroundColor == "rgb(36, 37, 38)" || informacionUsuario.style.backgroundColor == "white"){
                if (informacionUsuario.classList.contains("dark")) {
                    // Si la tiene, realiza alguna modificación, por ejemplo, cambiar el color de fondo
                    informacionUsuario.style.backgroundColor = "rgb(36, 37, 38)";
                }
                else{
                    informacionUsuario.style.backgroundColor = "white";
                }
            }
        }
        
        if (document.body.classList.contains("dark")) {
            icono_path.forEach((icono)=>{
                icono.setAttribute("stroke", "#fff");
            })
            icono_fill.forEach((icono)=>{
                icono.setAttribute("fill", "#fff");
            })
            logoImage.src = image2;
        } else {
            icono_path.forEach((icono)=>{
                icono.setAttribute("stroke", "#000000");
            }) 
            icono_fill.forEach((icono)=>{
                icono.setAttribute("fill", "#000000");
            })
            logoImage.src = image1;
        }
    }

    
    
    if (aspecto == "S"){
        if (isDarkMode) {
            console.log("El sistema está en modo oscuro.");
            acciones()
        } else {
            console.log("El sistema está en modo claro.");
        }
    }else if (aspecto == "O"){
        console.log("El usuario lo configuro en modo oscuro.");
        acciones()
    }else if (aspecto == "C"){
        console.log("El usuario lo configuro en modo claro")
    }


    document.body.style.display = 'block'; 

    const radioButton = document.querySelector(`input[name="modo"][value="${aspecto}"]`);
    if (radioButton) {
        radioButton.checked = true; // Marca el radio button como seleccionado
    }

    
    Layer_1.addEventListener("click", (event) => {
        if (sesion_configuracion.style.display === "flex" || aspecto_opciones.style.display === "flex") {
            sesion_configuracion.style.display = "none";
            aspecto_opciones.style.display = "none";
        } else {
            // Si ambos están ocultos, se muestra 'sesion_configuracion'
            sesion_configuracion.style.display = "flex";
        }
        event.stopPropagation(); // Evita que el evento se propague al document
    });
    
    // Evento para cerrar el menú si haces clic fuera de 'sesion_configuracion'
    document.addEventListener("click", (event) => {
        if (!sesion_configuracion.contains(event.target) && !aspecto_opciones.contains(event.target)) {
            sesion_configuracion.style.display = "none";
            aspecto_opciones.style.display = "none";
        }
    });
       
    // Lógica para cuando el usuario hace clic en 'Aspecto'
    Aspecto.addEventListener("click", () => {
        sesion_configuracion.style.display = "none";
        aspecto_opciones.style.display = "flex";
    });
    
    right_opciones.addEventListener("click",()=>{
        aspecto_opciones.style.display = "none";
        sesion_configuracion.style.display = "flex";
    })

window.addEventListener('resize', moveUserSection);
window.addEventListener('load', moveUserSection); // Para ejecutarlo al cargar la página

function moveUserSection() {
    const usuario = document.getElementById('usuario');
    const sesionConfiguracion = document.getElementById('sesion_configuracion');
    const sesion = document.querySelector('.sesion');

    if (window.innerWidth <= 768) {
        // Mover el usuario dentro de la configuración cuando la pantalla es pequeña
        if (!sesionConfiguracion.contains(usuario)) {
            sesionConfiguracion.insertBefore(usuario, sesionConfiguracion.firstChild);
        }
    } else {
        // Devolver el usuario a su posición original cuando la pantalla es grande
        if (!sesion.contains(usuario)) {
            sesion.insertBefore(usuario, sesion.firstChild);
        }
    }
}



    var miDiv = document.getElementById('nav');
    var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var scrollThreshold = 100;

    var isMobile = window.matchMedia("only screen and (min-width: 1001px) and (max-width: 1100px)").matches || window.matchMedia("only screen and (max-width: 400px)").matches;

    if (isMobile) {
        if (window.pageYOffset > scrollThreshold) {
            miDiv.classList.add('scrolled');
        }

        window.addEventListener('scroll', function() {
            var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            if (Math.abs(scrollTop - lastScrollTop) >= scrollThreshold) {
                if (scrollTop > lastScrollTop) {
                    // Desplazamiento hacia abajo
                    miDiv.classList.add('scrolled');
                } else {
                    // Desplazamiento hacia arriba
                    miDiv.classList.remove('scrolled');
                }
                lastScrollTop = scrollTop;
            }
        });
    }
});


$('input[name="modo"]').on('change', function() {

    const modoSeleccionado = document.querySelector('input[name="modo"]:checked').value;

    $.ajax({
        url: '/cambiar_aspecto/', 
        method: 'POST',
        data: {
            'modo': modoSeleccionado,
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        dataType:'json'
    })
    .done(function(data) {
        console.log(data)
        location.reload();
    })
    .fail(function(data) {
        console.log( "error" );
    })
    .always(function(data) {
        console.log( "complete" );
    }); 
    
    
});