const form = document.getElementById("email-form");
const emailText = document.getElementById("emailText");
const emailFile = document.getElementById("emailFile");
const loading = document.getElementById("loading");
const resultSection = document.getElementById("result");
const categorySpan = document.getElementById("category");
const replyParagraph = document.getElementById("reply");
const resetBtn = document.getElementById("resetBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if(!emailText.value && !emailFile.files.length){
        alert("Por favor, insira o texto do email ou selecione o arquivo.");
        return;
    }

    loading.classList.remove("hidden");
    resultSection.classList.add("hidden");  

    const formData = new FormData();
    formData.append("emailText", emailText.value);
    if(emailFile.files.length > 0){
        formData.append("emailFile", emailFile.files[0]);
    }

    try {
        const resposta = await fetch("/analyze", {
            method: "POST",
            body: formData,
        });

        const data = await resposta.json();

        if(!resposta.ok){
            throw new Error(data.error || "Erro ao processar o email.");
        }

        mostrarResultado(data.category, data.reply);

    } catch (error) {
        alert("Ocorreu um erro: " + error.message);
        console.error("Erro detalhado:", error);
    } finally {
        loading.classList.add("hidden");
    }
});

function mostrarResultado(category, reply){
    resultSection.classList.remove("show");
    categorySpan.classList.remove("emailprodutivo", "emailimprodutivo");

    if(!category){
        categorySpan.textContent = "Erro na classificação";
        categorySpan.classList.add("emailimprodutivo");
        replyParagraph.textContent = "Não foi possível analisar o email.";
    } else {
        categorySpan.textContent = category;
        if(category.toLowerCase() === "email produtivo"){
            categorySpan.classList.add("emailprodutivo");
        } else {
            categorySpan.classList.add("emailimprodutivo");
        }
        replyParagraph.textContent = reply || "";
    }

    resultSection.classList.remove("hidden");
    void resultSection.offsetWidth;
    resultSection.classList.add("show");
}

resetBtn.addEventListener("click", () => {
    resultSection.classList.add("hidden");
    setTimeout(() => {
        emailText.value = "";
        emailFile.value = "";
        categorySpan.textContent = "";
        categorySpan.classList.remove("emailprodutivo", "emailimprodutivo");
        replyParagraph.textContent = "";
        form.classList.remove("hidden");
        resultSection.classList.add("hidden");
    }, 400);
});
