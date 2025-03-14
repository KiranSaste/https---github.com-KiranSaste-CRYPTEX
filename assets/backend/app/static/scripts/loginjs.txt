
// This is the login page script
/*
const container = document.querySelector('.login-container');
const CreateAccountBtn = document.querySelector('.create-account-btn");');
const loginBtn = document.querySelector('.login-btn');

CreateAccountBtn.addEventListener('click', () => {
    container.classList.add('active');
});

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});
*/
document.addEventListener('DOMContentLoaded', () => {
    const loginContainer = document.querySelector('.login-container');
    const createAccountLinks = document.querySelectorAll('.create-account-link, .create-account-btn');
    const loginLinks = document.querySelectorAll('.login-link, .login-btn');

    createAccountLinks.forEach(link => {
        link.addEventListener('click', () => {
            loginContainer.classList.add('active');
        });
    });

    loginLinks.forEach(link => {
        link.addEventListener('click', () => {
            loginContainer.classList.remove('active');
        });
    });
});