      // Papel recortado: la hoja en la cocina
      tl.fromTo("#pa-svg", { scale: 1.0 }, { scale: 1.04, duration: 5.3, ease: "none", transformOrigin: "50% 60%" }, 26.4);
      tl.fromTo("#pa-hoja", { y: 260, rotation: -12, opacity: 0 }, { y: 0, rotation: -3, opacity: 1, duration: 0.6, ease: "back.out(1.6)", svgOrigin: "540 1040" }, 26.5);
      tl.fromTo("#pa-cinta1", { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(2)", svgOrigin: "360 724" }, 27.0);
      tl.fromTo("#pa-cinta2", { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(2)", svgOrigin: "720 724" }, 27.15);
      ["#pa-l1", "#pa-l2", "#pa-l3", "#pa-l4"].forEach((id, i) => tl.fromTo(id, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.45, ease: "power1.inOut" }, 27.4 + i * 0.5));
      [["#pa-vapor1", 26.6], ["#pa-vapor2", 27.1]].forEach(([id, t0]) => {
        for (let k = 0; k < 3; k++) {
          tl.fromTo(id, { y: 0, opacity: 0.7 }, { y: -60, opacity: 0, duration: 1.5, ease: "none", immediateRender: false }, t0 + k * 1.5);
        }
      });
      // Papel recortado: el conteo de platos
      tl.fromTo("#pb-svg", { scale: 1.04 }, { scale: 1.0, duration: 5.2, ease: "none", transformOrigin: "50% 60%" }, 31.7);
      const MARCAS = [[270, 1080], [310, 1080], [350, 1080], [390, 1080], [415, 950], [480, 1080], [520, 1080], [560, 1080], [600, 1080], [625, 950], [270, 1330], [310, 1330]];
      tl.fromTo("#pb-lapiz", { x: 1100, y: 700 }, { x: 270, y: 930, duration: 0.4, ease: "power2.out" }, 31.75);
      MARCAS.forEach(([x, y], i) => {
        const t0 = 32.2 + i * 0.28;
        tl.fromTo("#pb-m" + (i + 1), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.22, ease: "none" }, t0);
        tl.to("#pb-lapiz", { x: x, y: y, duration: 0.22, ease: "none" }, t0);
      });
      tl.to("#pb-lapiz", { x: 1100, y: 700, duration: 0.5, ease: "power2.in" }, 36.0);
      [1, 2, 3, 4, 5, 6].forEach((n) => tl.fromTo("#pb-p" + n, { y: -120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "bounce.out" }, 32.3 + (n - 1) * 0.56));
