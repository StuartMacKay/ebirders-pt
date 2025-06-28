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

function open_filter_panels() {
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });

    if (params.country || params.state || params.country || params.location || params.hotspot) {
        const list = document.querySelectorAll('a[href="#form-location"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.observer) {
        const list = document.querySelectorAll('a[href="#form-observer"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.from || params.until) {
        const list = document.querySelectorAll('a[href="#form-date-range"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.species) {
        const list = document.querySelectorAll('a[href="#form-species"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.category) {
        const list = document.querySelectorAll('a[href="#form-category"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.order) {
        const checklist_list = document.querySelectorAll('a[href="#form-checklist-order"]');
        for (const link of checklist_list) {
            link.click();
        }
        const observation_list = document.querySelectorAll('a[href="#form-checklist-order"]');
        for (const link of observation_list) {
            link.click();
        }
        const seen_list = document.querySelectorAll('a[href="#form-checklist-order"]');
        for (const link of seen_list) {
            link.click();
        }
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
  'use strict';
  open_filter_panels();
  remove_blank_form_fields();
});
