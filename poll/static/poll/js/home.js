/* globals $, $$, btoa, fetch, Clipboard, twttr, window, document */

/* bling.js Modified to make $ querySelector and $$ qSA */
window.$ = document.querySelector.bind(document);
window.$$ = document.querySelectorAll.bind(document);
Node.prototype.on = window.on = function (name, fn) {
  this.addEventListener(name, fn);
};
NodeList.prototype.__proto__ = Array.prototype;
NodeList.prototype.on = NodeList.prototype.addEventListener = function (name, fn) {
  this.forEach(function (elem, i) {
    elem.on(name, fn);
  });
};

(() => {
  const user = $('#mal-username');
  const pass = $('#mal-password');
  const submit = $('#submitForm');
  const credentials = $('#credentials');
  const clipboard = new Clipboard('.copy');

  const apiCall = (url, body) =>
    fetch(url, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })
    .then(res => res.json())
    .catch(err => Error(err));

  function showList(user) {
    const url = `${window.location.origin}/${user}`;
    $('#link').innerHTML = `<a href="${url}" rel="noopener noreferrer" target="_blank">${url}</a>`;
    $('#reddit-md').value = `Pick something from my PTW list! [pick.moe/${user}](${url})`;
    twttr.widgets.createShareButton('/',
      $('#twitter'),
      { size: 'large', text: `Pick something from my PTW list! ${url}` });
    $('#newList').classList.remove('hidden');
    $('#newList').scrollIntoView();
  }

  const showMalError = (err) => {
    $('#mal-error').innerHTML = err;
    setTimeout(() => {
      $('#mal-error').innerHTML = '';
    }, 4000);
  };

  function submitForm(e) {
    e.preventDefault();
    if (!submit.disabled) {
      const malUser = user.value.trim();
      const malPass = pass.value.trim();
      submit.classList.add('is-loading');
      apiCall('/poll/create', { auth: btoa(`${malUser}:${malPass}`) })
      .then((res) => {
        console.log(res);
        submit.classList.remove('is-loading');
        if (res.user) showList(res.user);
        else showMalError('Username and password did not match or no user found.');
      })
      .catch(err => console.error(Error(err)));
    }
  }

  // Event listeners
  credentials.on('submit', submitForm);
  clipboard.on('success', () => {
    const tooltip = document.createElement('span');
    tooltip.classList.add('tooltiptext');
    tooltip.innerHTML = ' Copied! ';
    $('.copy').appendChild(tooltip);
    setTimeout(() => {
      $('.copy').removeChild($('.tooltiptext'));
    }, 2000);
  });

  // Open the help modal
  $('#help').on('click', () => {
    $('#helpModal').classList.add('is-active');
  });
  // Open the reddit modal
  $('#reddit').on('click', () => {
    $('#redditModal').classList.add('is-active');
  });
  // Close modals
  Array.from($$('.modal-background')).forEach((e) => {
    e.on('click', () => $('.is-active').classList.remove('is-active'));
  });
  Array.from($$('.modal-close')).forEach((e) => {
    e.on('click', () => $('.is-active').classList.remove('is-active'));
  });
})();
