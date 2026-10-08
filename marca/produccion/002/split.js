      // Kenneth abajo: acercamiento lento
      tl.fromTo("#av1", { scale: 1.0 }, { scale: 1.04, duration: 5.3, ease: "none" }, 0);
      tl.fromTo("#av2", { scale: 1.0 }, { scale: 1.05, duration: 9.6, ease: "none" }, 10.3);
      tl.fromTo("#av3", { scale: 1.0 }, { scale: 1.06, duration: 13.26, ease: "none" }, 36.9);
      // s1: la operacion que nunca se apago
      tl.fromTo("#s1-cinta", { x: 0 }, { x: 480, duration: 5.3, ease: "none" }, 0);
      tl.fromTo("#s1-anios", { scale: 2.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.6)", svgOrigin: "200 240" }, 0.4);
      tl.fromTo("#s1-anios2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.75);
      tl.fromTo("#s1-247", { fill: "#7B8190" }, { fill: "#F5B700", duration: 0.12 }, 3.0);
      tl.fromTo("#s1-247", { fill: "#F5B700" }, { fill: "#7B8190", duration: 0.06, immediateRender: false }, 3.18);
      tl.fromTo("#s1-247", { fill: "#7B8190" }, { fill: "#F5B700", duration: 0.1, immediateRender: false }, 3.3);
      // s2: la soda cierra
      tl.fromTo("#s2-rotulo", { scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: "back.out(2)", svgOrigin: "390 470" }, 11.1);
      tl.fromTo("#s2-termo", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 11.9);
      tl.fromTo("#s2-mercurio", { scaleY: 0.15 }, { scaleY: 1, duration: 0.8, ease: "power2.out", svgOrigin: "902 680" }, 12.1);
      // s3
      tl.fromTo("#s3a", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 14.15);
      tl.fromTo("#s3b", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 14.3);
      // s4: el estandar vive en tu cabeza
      [["#s4-i1", "500 430", 18.0], ["#s4-i2", "665 450", 18.6], ["#s4-i3", "560 610", 19.2]].forEach(([id, o, t0]) =>
        tl.fromTo(id, { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(2)", svgOrigin: o }, t0));
      // s5: 15 minutos los lunes
      tl.fromTo("#s5-cal", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }, 36.95);
      tl.fromTo("#s5-anillo", { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 2.8, ease: "none" }, 37.7);
      tl.fromTo("#s5-gente", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 40.1);
      // s6: te necesita todos los dias
      tl.fromTo("#s6-cadena", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out", svgOrigin: "370 600" }, 41.9);
      tl.fromTo("#s6-candado", { y: -260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "bounce.out" }, 42.6);
      // s7
      tl.fromTo("#s7a", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 44.8);
      tl.fromTo("#s7b", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 44.95);
      // s8: guardalo, mandaselo
      tl.fromTo("#s8-guardar", { y: -120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "bounce.out" }, 47.1);
      tl.fromTo("#s8-t1", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 47.25);
      tl.fromTo("#s8-avion", { x: -420, y: 260, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.55, ease: "power3.out" }, 49.0);
      tl.fromTo("#s8-t2", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 49.2);
