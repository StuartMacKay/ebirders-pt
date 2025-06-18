function remove_blank_form_fields() {
    'use strict';
    let forms = document.getElementsByClassName("remove-empty-values");
    for (let i=0; i < forms.length; i++) {
       forms[i].addEventListener("submit", (event) => {
           let fields = event.target.elements;
           for (let j=0; j < fields.length; j++) {
              if (!fields[j].value) {
                 fields[j].setAttribute("name", "");
              }
           }
       });
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
  'use strict';
  remove_blank_form_fields();
});
