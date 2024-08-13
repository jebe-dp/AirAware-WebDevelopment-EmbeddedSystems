const profileUrl = "{% url 'patient_profile' %}";
const patientUrl = "{% url 'patient_record' %}";


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.nav-list a').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); 
            const pageUrl = this.getAttribute('data-page-url'); 
            loadPage(pageUrl); 
        });
    });
});

function loadPage(pageUrl) {
	fetch(pageUrl)
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.text();
		})
		.then(html => {
			document.getElementById('pageContent').innerHTML = html;
		})
		.catch(error => console.error('Error loading page:', error));
}

window.addEventListener('load', function() {
	loadDefaultPage();
});

function loadDefaultPage() {
	const defaultPageUrl = 'patient_profile.html';
	loadPage(defaultPageUrl);
}

const sidebar = document.querySelector(".sidebar");
const closeBtn = document.querySelector("#btn");

closeBtn.addEventListener("click", function() {
	sidebar.classList.toggle("open");
	menuBtnChange();
});

function menuBtnChange() {
	if (sidebar.classList.contains("open")) {
		closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
	} else {
		closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
	}
}
