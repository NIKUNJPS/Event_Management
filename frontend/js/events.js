async function loadEvents() {
  const list = document.getElementById('events');
  const search = document.getElementById('search');
  const category = document.getElementById('category');

  const all = await api('/events');

  const cats = [
    ...new Set(all.map(e => e.category))
  ];

  category.innerHTML =
    '<option value="">All categories</option>' +
    cats
      .map(c => `<option>${c}</option>`)
      .join('');

  function render() {
    const q = search.value.toLowerCase();
    const c = category.value;

    list.innerHTML =
      all
        .filter(
          e =>
            (
              !q ||
              e.title.toLowerCase().includes(q) ||
              e.venue.toLowerCase().includes(q)
            ) &&
            (!c || e.category === c)
        )
        .map(
          e =>
            `<article class="card">
              <div class="card-img">
                ${e.category}
              </div>

              <div class="card-body">
                <div class="muted">
                  ${e.event_date} · ${e.event_time.slice(0, 5)}
                </div>

                <h3>${e.title}</h3>

                <p class="muted">
                  ${e.venue}
                </p>

                <div class="row">
                  <span class="price">
                    ₹${e.price}
                  </span>

                  <a 
                    class="btn" 
                    href="event-details.html?id=${e.id}">
                    View
                  </a>
                </div>
              </div>
            </article>`
        )
        .join('') ||
      '<p>No events found.</p>';
  }

  search.oninput = render;

  category.onchange = render;

  render();
}