export function mountInterpolation(container) {
    const W = 340, H = 340, PAD = 40, N = 4;
    const GW = W - 2 * PAD, GH = H - 2 * PAD;
    let px = 0.5, py = 0.5, dragging = false;

    container.innerHTML = `
    <div style="display:flex;gap:2rem;align-items:flex-start;flex-wrap:wrap;">
      <canvas id="ibl-grid" width="${W}" height="${H}" style="display:block;cursor:crosshair;"></canvas>
      <div style="display:flex;flex-direction:column;gap:12px;min-width:160px;">
        <p style="font-size:13px;color:#888;margin:0 0 4px;">coefficients</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
          <div class="ibl-card" id="ibl-c-tl"><div class="ibl-label">haut gauche</div><div class="ibl-val" id="ibl-tl">0.25</div></div>
          <div class="ibl-card" id="ibl-c-tr"><div class="ibl-label">haut droit</div><div class="ibl-val" id="ibl-tr">0.25</div></div>
          <div class="ibl-card" id="ibl-c-bl"><div class="ibl-label">bas gauche</div><div class="ibl-val" id="ibl-bl">0.25</div></div>
          <div class="ibl-card" id="ibl-c-br"><div class="ibl-label">bas droit</div><div class="ibl-val" id="ibl-br">0.25</div></div>
        </div>
        <p style="font-size:12px;color:#aaa;margin:8px 0 0;">
          x = <span id="ibl-sx">0.500</span>, y = <span id="ibl-sy">0.500</span>
        </p>
      </div>
    </div>
    <style>
      .ibl-card { background:#f5f5f5; border-radius:8px; padding:10px 12px; transition:background .15s; }
      .ibl-label { font-size:11px; color:#888; margin-bottom:4px; }
      .ibl-val { font-size:20px; font-weight:500; }
    </style>
  `;

    const canvas = container.querySelector('#ibl-grid');
    const ctx = canvas.getContext('2d');

    function toCanvas(nx, ny) { return [PAD + nx * GW, PAD + (1 - ny) * GH]; }
    function fromCanvas(cx, cy) {
        return [
            Math.max(0, Math.min(1, (cx - PAD) / GW)),
            Math.max(0, Math.min(1, 1 - (cy - PAD) / GH))
        ];
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);

        const gridColor = 'rgba(0,0,0,0.25)';
        const axisColor = 'rgba(0,0,0,0.25)';
        const textColor = 'rgba(0,0,0,0.45)';
        const pointColor = '#378ADD';
        const lineColor = 'rgba(55,138,221,0.25)';

        ctx.strokeStyle = gridColor; ctx.lineWidth = 1; ctx.setLineDash([2, 2]);
        for (let i = 0; i <= N; i++) {
            const xc = PAD + (i / N) * GW, yc = PAD + (i / N) * GH;
            ctx.beginPath(); ctx.moveTo(xc, PAD); ctx.lineTo(xc, PAD + GH); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(PAD, yc); ctx.lineTo(PAD + GW, yc); ctx.stroke();
        }
        ctx.setLineDash([]);
        ctx.strokeStyle = axisColor; ctx.lineWidth = 2;
        ctx.strokeRect(PAD, PAD, GW, GH);

        ctx.font = '12px sans-serif'; ctx.fillStyle = textColor;
        ctx.textAlign = 'center';
        for (let i = 0; i <= N; i++) {
            ctx.fillText((i / N).toFixed(2), PAD + (i / N) * GW, PAD + GH + 18);
        }
        ctx.textAlign = 'right';
        for (let i = 0; i <= N; i++) {
            ctx.fillText((i / N).toFixed(2), PAD - 6, PAD + (1 - i / N) * GH + 4);
        }

        const [cx, cy] = toCanvas(px, py);
        ctx.strokeStyle = lineColor; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.moveTo(cx, PAD); ctx.lineTo(cx, PAD + GH); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(PAD, cy); ctx.lineTo(PAD + GW, cy); ctx.stroke();
        ctx.setLineDash([]);

        const bl = (1 - px) * (1 - py), br = px * (1 - py), tl = (1 - px) * py, tr = px * py;

        ctx.beginPath(); ctx.arc(cx, cy, 7, 0, Math.PI * 2);
        ctx.fillStyle = pointColor; ctx.fill();
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();

        container.querySelector('#ibl-tl').textContent = tl.toFixed(3);
        container.querySelector('#ibl-tr').textContent = tr.toFixed(3);
        container.querySelector('#ibl-bl').textContent = bl.toFixed(3);
        container.querySelector('#ibl-br').textContent = br.toFixed(3);
        container.querySelector('#ibl-sx').textContent = px.toFixed(3);
        container.querySelector('#ibl-sy').textContent = py.toFixed(3);

        const max = Math.max(bl, br, tl, tr);
        for (const [id, v] of [['ibl-c-tl', tl], ['ibl-c-tr', tr], ['ibl-c-bl', bl], ['ibl-c-br', br]]) {
            const card = container.querySelector('#' + id);
            card.style.background = v === max ? '#dbeafe' : '#f5f5f5';
            card.querySelector('.ibl-val').style.color = v === max ? '#1d4ed8' : '#000';
        }
    }

    function getPos(e) {
        const r = canvas.getBoundingClientRect();
        const t = e.touches ? e.touches[0] : e;
        return [t.clientX - r.left, t.clientY - r.top];
    }

    canvas.addEventListener('mousedown', e => { dragging = true;[px, py] = fromCanvas(...getPos(e)); draw(); });
    canvas.addEventListener('mousemove', e => { if (!dragging) return;[px, py] = fromCanvas(...getPos(e)); draw(); });
    canvas.addEventListener('mouseup', () => dragging = false);
    canvas.addEventListener('mouseleave', () => dragging = false);
    canvas.addEventListener('touchstart', e => { e.preventDefault(); dragging = true;[px, py] = fromCanvas(...getPos(e)); draw(); }, { passive: false });
    canvas.addEventListener('touchmove', e => { e.preventDefault(); if (!dragging) return;[px, py] = fromCanvas(...getPos(e)); draw(); }, { passive: false });
    canvas.addEventListener('touchend', () => dragging = false);

    draw();
}