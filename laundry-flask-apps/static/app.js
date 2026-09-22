function fmtRp(n) {
  return 'Rp' + n.toLocaleString('id-ID');
}

async function hitungRute(target) {
  const res = await fetch(`/hitung/${target}`);
  const data = await res.json();

  const routeLine = document.getElementById('routeLine');
  routeLine.innerHTML = '';
  data.rute.forEach((n, i) => {
    const pill = document.createElement('span');
    pill.className = 'node-pill';
    pill.textContent = n;
    routeLine.appendChild(pill);
    if (i < data.rute.length - 1) {
      const arr = document.createElement('span');
      arr.className = 'arrow';
      arr.textContent = '\u2192';
      routeLine.appendChild(arr);
    }
  });

  document.getElementById('distStat').textContent = data.jarak_km.toFixed(1);
  document.getElementById('costStat').textContent = fmtRp(data.total_biaya);
  document.getElementById('zoneStat').textContent = data.label_zona;
  document.getElementById('bDist').textContent = fmtRp(data.biaya_jarak);
  document.getElementById('bZone').textContent = fmtRp(data.biaya_zona);
  document.getElementById('bTotal').textContent = fmtRp(data.total_biaya);
  document.getElementById('result').classList.add('show');
}

async function muatRingkasan() {
  const res = await fetch('/ringkasan');
  const data = await res.json();
  const tbody = document.querySelector('#allTable tbody');
  tbody.innerHTML = '';
  data.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${item.tujuan}</td><td>${item.rute.join('\u2013')}</td><td>${item.jarak_km.toFixed(1)} km</td><td>${fmtRp(item.total_biaya)}</td>`;
    tbody.appendChild(tr);
  });
}

document.getElementById('calc').addEventListener('click', () => {
  hitungRute(document.getElementById('dest').value);
});

// Muat data awal saat halaman dibuka
muatRingkasan();
hitungRute('G');
