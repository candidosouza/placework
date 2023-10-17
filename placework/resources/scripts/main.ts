const formradio = document.querySelector("#id_account_type") as HTMLInputElement;
const fieldsetPJ = document.querySelector("#fieldset-pj") as HTMLInputElement;
const fieldsetPF = document.querySelector("#fieldset-pf") as HTMLInputElement;
const passwordHelpInline = document.querySelector("#passwordHelpInline") as HTMLElement;
const infoAddress = document.querySelector("#infoAddress") as HTMLElement;

function updateFields() {
    if (formradio.value === "PJ") {
        fieldsetPJ.classList.remove("d-none");
        fieldsetPJ.disabled = false;
        fieldsetPF.classList.add("d-none");
        fieldsetPF.disabled = true;
        passwordHelpInline.style.display = "block";
        infoAddress.style.display = "inline-block";
    } else if (formradio.value === "PF") {
        fieldsetPF.classList.remove("d-none");
        fieldsetPF.disabled = false;
        fieldsetPJ.classList.add("d-none");
        fieldsetPJ.disabled = true;
        passwordHelpInline.style.display = "none";
        infoAddress.style.display = "none";
    }
}

if (formradio) {
    updateFields(); // Atualiza os campos com base no valor inicial.
    formradio.addEventListener("change", updateFields);
}

// // ViaCep
const zipCode = document.querySelector("#id_zip_code") as HTMLInputElement;
const number = document.querySelector("#id_number") as HTMLInputElement;


const cepInfo = {
    street: document.querySelector("#id_street") as HTMLInputElement,
    neighborhood: document.querySelector("#id_neighborhood") as HTMLInputElement,
    city: document.querySelector("#id_city") as HTMLInputElement,
    state: document.querySelector("#id_state") as HTMLInputElement,
};

const updateCepInfo = (data: any) => {
    cepInfo.street.value = data.logradouro;
    cepInfo.neighborhood.value = data.bairro;
    cepInfo.city.value = data.localidade;
    cepInfo.state.value = data.uf;
};

const fetchCepInfo = async (cep: string) => {
    try {
        const url = await `https://viacep.com.br/ws/${cep}/json/`;
        fetch(url)
            .then((response) => response.json())
            .then((data) => {
                if (data.erro) {
                    alert("CEP não encontrado.");
                } else {
                    console.log(data);
                    updateCepInfo(data);
                    number.focus();
                }
            });
    } catch (error) {
        console.error('Erro na solicitação:', error);
    }
};

// console.log('okokokoko');

zipCode.addEventListener('input', () => {
    const enteredCep = zipCode.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (enteredCep.length === 8) {
        fetchCepInfo(enteredCep);
    }
});