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

    if (params.country || params.state || params.county || params.location || params.hotspot) {
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
    if (params.start || params.finish) {
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
    if (params.protocol || params.complete) {
        const list = document.querySelectorAll('a[href="#form-protocol"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.approved || params.audio || params.photo || params.video) {
        const list = document.querySelectorAll('a[href="#form-observation"]');
        for (const link of list) {
            link.click();
        }
    }
    if (params.order) {
        const checklist_list = document.querySelectorAll('a[href="#form-checklist-order"]');
        for (const link of checklist_list) {
            link.click();
        }
        const observation_list = document.querySelectorAll('a[href="#form-observation-order"]');
        for (const link of observation_list) {
            link.click();
        }
        const seen_list = document.querySelectorAll('a[href="#form-seen-order"]');
        for (const link of seen_list) {
            link.click();
        }
    }
}

function activate_clear_button() {
    const button = document.getElementById("clear-form");
    if (button) {
        const forms = document.getElementsByTagName("form");
        button.addEventListener("click", (event) => {
            var elements = document.getElementsByTagName("input");
            for (var i=0; i < elements.length; i++) {
                elements[i].name = "";
                elements[i].value = "";
            }
            var elements = document.getElementsByTagName("select");
            for (var i=0; i < elements.length; i++) {
                elements[i].name = "";
                elements[i].value = "";
            }
            forms[0].submit();
        });
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
  'use strict';
  open_filter_panels();
  remove_blank_form_fields();
  activate_clear_button();
});
