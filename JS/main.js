const form = document.getElementById("email-form");
const emailText = document.getElementById("emailText");
const emailFile = document.getElementById("emailFile");
const loading = document.getElementById("loading");
const resultSection = document.getElementById("result");
const categorySpan = document.getElementById("category");
const replyParagraph = document.getElementById("reply");
const resetBtn = document.getElementById("resetBtn");

form.addEventListener("submit", async (e) => {
    event.preventDefault();

    //Validar se não tam vazio
    if(!emailText.value && !emailFile.files.length){
        alert("Por favor, insira o texto do email ou selecione o arquivo.")
        return;
    }

    loading.classList.remove("hidden");
    resultSection.classList.add("hidden");  

    const formData = new FormData();
    formData.append("emailText",emailText.value);

    if (emailFile.files.length > 0) {
        formData.append("emailFile",emailFile.files[0]);
    }
    try {
        const resposta = await fetch("/analyze", {
            method: "POST",
            body: formData,
    });
        if(!resposta.ok){
            throw new Error("Erro ao processar o email.");
        }
        const data = await resposta.json();

        showResult(data.category, data.reply);
    } catch (error) {
        alert("Ocorreu um erro ao processar o email. Tente novamente.");
        console.error("Erro:", error);
    } finally{
        loading.classList.add("hidden");
    }
}); 

// Função para mostrar o resultado
function mostrarResultado(caterory, reply){
    categorySpan.textContent = category;

    categorySpan.classList.remove("emailprodutivo","emailimprodutivo");

    if (caterory.toLowerCase() === "emailprodutivo"){
        categorySpan.classList.add("emailprodutivo");
    } else {
        categorySpan.classList.add("emailimprodutivo");
    }

    replyParagraph.textContent = reply;

    resultSection.classList.remove("hidden");
}

//Botão de Resetar
resetBtn.addEventListener("click", () =>{
    form.reset();
    resultSection.classList.add("hidden");
});
    