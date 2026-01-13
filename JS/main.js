const form = document.getElementById("email-form");
cosnt emailText = document.getElementById("emailText");
const emailFile = document.getElementById("emailFile");

form.addEventListener("submit", async (e) => {
    event.preventDefault();

    //Validar
    if(!emailText.value && !emailFile.isDefaultNamespace.length){
        alert("Por favor, insira o texto do email ou selecione o arquivo.")
        return;
    }
}); 