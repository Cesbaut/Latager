document.addEventListener('DOMContentLoaded', function() {
    const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

    let icono_fill = document.querySelectorAll(".icono_fill")

    function acciones(){
        document.body.classList.toggle("dark");


        if (document.body.classList.contains("dark")) {
            // icono_path.forEach((icono)=>{
            //     icono.setAttribute("stroke", "#fff");
            // })
            icono_fill.forEach((icono)=>{
                icono.setAttribute("fill", "#fff");
            })
        } else {
            // icono_path.forEach((icono)=>{
            //     icono.setAttribute("stroke", "#000000");
            // }) 
            icono_fill.forEach((icono)=>{
                icono.setAttribute("fill", "#000000");
            })
        }
    }

    if (isDarkMode) {
        console.log("El sistema está en modo oscuro.");
        acciones()
    } else {
        console.log("El sistema está en modo claro.");
    }
    
})