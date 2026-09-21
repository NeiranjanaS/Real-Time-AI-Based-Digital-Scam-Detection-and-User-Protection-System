const form = document.getElementById("scanForm");

if(form){

form.addEventListener("submit",()=>{

document.getElementById("loading").classList.remove("hidden");

});

}