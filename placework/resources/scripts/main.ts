const formradio = document.querySelector("#id_account_type") as HTMLInputElement;
const fieldsetPJ = document.querySelector("#fieldset-pj") as HTMLInputElement;
const fieldsetPF = document.querySelector("#fieldset-pf") as HTMLInputElement;
const passwordHelpInline = document.querySelector("#passwordHelpInline") as HTMLElement;
const infoAddress = document.querySelector("#infoAddress") as HTMLElement;

if (formradio.value == "PJ") {
    fieldsetPJ.classList.remove("d-none");
    fieldsetPJ.disabled = false;
    fieldsetPF.classList.add("d-none");
    fieldsetPF.disabled = true;
    passwordHelpInline.style.display = "block";
    infoAddress.style.display = "inline-block";
}

if (formradio.value == "PF") {
    fieldsetPF.classList.remove("d-none");
    fieldsetPF.disabled = false;
    fieldsetPJ.classList.add("d-none");
    fieldsetPJ.disabled = true;
    passwordHelpInline.style.display = "none";
    infoAddress.style.display = "none";
}

if (formradio) {
    formradio.addEventListener("change", function () {
        if (formradio.value == "PJ") {
            fieldsetPJ.classList.remove("d-none");
            fieldsetPJ.disabled = false;
            fieldsetPF.classList.add("d-none");
            fieldsetPF.disabled = true;
            passwordHelpInline.style.display = "block";
            infoAddress.style.display = "inline-block";
        } else {
            fieldsetPF.classList.remove("d-none");
            fieldsetPF.disabled = false;
            fieldsetPJ.classList.add("d-none");
            fieldsetPJ.disabled = true;
            passwordHelpInline.style.display = "none";
            infoAddress.style.display = "none";
        }
    });
}
