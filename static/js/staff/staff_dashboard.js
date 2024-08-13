const dashboardUrl = "{% url 'dashboard' %}";
const unverifiedFormsUrl = "{% url 'unverifiedforms' %}";
const patientRecordsUrl = "{% url 'view_records' %}";
const manageUsersUrl = "{% url 'manage_users' %}";
const learnMoreUrl = "{% url 'learn_more' %}";

document.addEventListener('DOMContentLoaded', function() {
	document.querySelectorAll('.nav-list a').forEach(link => {
		link.addEventListener('click', function(event) {
			event.preventDefault(); 
			const pageUrl = this.dataset.pageUrl; 
			loadPage(pageUrl); 
		});
	});
});


function loadPage(pageUrl) {
	fetch(pageUrl)
		.then(response => response.text())
		.then(html => {
			document.getElementById('pageContent').innerHTML = html;
		})
		.catch(error => console.error('Error loading page:', error));
}

window.addEventListener('load', function() {
	loadDefaultPage();
});


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
