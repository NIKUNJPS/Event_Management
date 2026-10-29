async function loadDetails() {
  if (!token()) {
    location.href = 'login.html';
    return;
  }

  const id = new URLSearchParams(location.search).get('id');

  const event = await api('/events/' + id);

  document.getElementById('title').textContent = event.title;

  document.getElementById('info').textContent =
    `${event.event_date} · ${event.event_time.slice(0, 5)} · ${event.venue} · ₹${event.price} per seat`;

  document.getElementById('description').textContent =
    event.description;

  const seats = await api(`/events/${id}/seats`);

  let selected = [];

  const box = document.getElementById('seats');

  box.innerHTML = seats
    .map(
      s =>
        `<button class="seat ${s.is_booked ? 'booked' : ''}" 
        data-id="${s.id}" 
        ${s.is_booked ? 'disabled' : ''}>
        ${s.seat_number}
        </button>`
    )
    .join('');

  box
    .querySelectorAll('.seat:not(.booked)')
    .forEach(b => {
      b.onclick = () => {
        const sid = Number(b.dataset.id);

        if (selected.includes(sid)) {
          selected = selected.filter(x => x !== sid);
          b.classList.remove('selected');
        } else {
          selected.push(sid);
          b.classList.add('selected');
        }

        document.getElementById('total').textContent =
          '₹' + (selected.length * Number(event.price));
      };
    });

  document.getElementById('book').onclick = async () => {
    if (!selected.length) {
      return alert('Select at least one seat');
    }

    try {
      const b = await api('/bookings', {
        method: 'POST',
        body: JSON.stringify({
          event_id: Number(id),
          seat_ids: selected
        })
      });

      document.getElementById('msg').innerHTML =
        `<div class="notice success">
          Booking confirmed. ID: #${b.id}
        </div>`;

      setTimeout(
        () => location.href = 'bookings.html',
        700
      );
    } catch (e) {
      document.getElementById('msg').innerHTML =
        `<div class="notice error">
          ${e.message}
        </div>`;

      loadDetails();
    }
  };
}


async function loadBookings() {
  if (!token()) {
    location.href = 'login.html';
    return;
  }

  const bs = await api('/bookings/my');

  document.getElementById('bookings').innerHTML =
    bs.length
      ? bs
          .map(
            b =>
              `<tr>
                <td>#${b.id}</td>
                <td>${b.event_title}</td>
                <td>${b.seat_numbers.join(', ')}</td>
                <td>₹${b.total_amount}</td>
                <td>${b.status}</td>
                <td>
                  ${
                    b.status === 'confirmed'
                      ? `<button 
                          class="btn danger" 
                          onclick="cancelBooking(${b.id})">
                          Cancel
                        </button>`
                      : ''
                  }
                </td>
              </tr>`
          )
          .join('')
      : '<tr><td colspan="6">No bookings yet.</td></tr>';
}


async function cancelBooking(id) {
  if (!confirm('Cancel this booking?')) {
    return;
  }

  try {
    await api('/bookings/' + id, {
      method: 'DELETE'
    });

    loadBookings();
  } catch (e) {
    alert(e.message);
  }
}