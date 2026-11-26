// reduz proporcionalmente o texto de cada bloco até caber na área disponível
document.fonts.ready.then(() => {
  document.querySelectorAll('.fitbox').forEach(box => {
    let s = 1;
    box.style.setProperty('--s', s);
    const over = () => box.scrollHeight > box.clientHeight + 1 ||
      [...box.querySelectorAll('.tt,.tt2,.bd,.sub')].some(e => e.scrollWidth > e.clientWidth + 1);
    while (over() && s > 0.55) { s -= 0.02; box.style.setProperty('--s', s.toFixed(2)); }
    box.dataset.scale = s.toFixed(2);
  });
  document.body.dataset.ready = '1';
});
