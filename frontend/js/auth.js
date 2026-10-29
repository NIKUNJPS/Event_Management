async function submitAuth(type) {
  const name = document.getElementById('name')?.value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const data =
    type === 'register'
      ? { name, email, password }
      : { email, password };

  try {
    const out = await api('/auth/' + type, {
      method: 'POST',
      body: JSON.stringify(data)
    });

    localStorage.setItem('token', out.access_token);

    location.href = 'events.html';
  } catch (e) {
    document.getElementById('msg').textContent = e.message;
  }
}