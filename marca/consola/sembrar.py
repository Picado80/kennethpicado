"""Genera las semillas de la consola de marca en marca/consola/datos/*.json.

Uso (desde la raíz de kennethpicado):
    python marca/consola/sembrar.py

Sigue a ESTRATEGIA.md (19-oct): la meta es crecer en seguidores. Cada pieza dice si es volumen o insignia, qué
formato tiene y qué paso de la cadena mueve (ver, reaccionar, pasarlo, conocerte, seguir).
No llama a ninguna API. Los saldos se pasan a mano abajo, con la fecha en que se midieron.
Ojo: cargar estas semillas pisa lo que Kenneth marcó en la consola (ver LEEME.md).
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos"
ACTUALIZADO = "2026-10-19T11:30:00-06:00"
ARRANQUE = date(2026, 10, 21)        # el Día 1 (Kenneth, 19-oct)
COSTO_INSIGNIA = 3.0                 # ESTRATEGIA.md §10: de $2 a $4 cada una

# La cadena (ESTRATEGIA.md §1). En cada pieza, «objetivo» es el paso que mueve.
VARAS = {
    "Ver": "retiene más del 50 % a los 3 s",
    "Reaccionar": "más comentarios por cada 1.000 vistas que el promedio de la cuenta",
    "Pasarlo": "al menos 1 compartido o guardado por cada 1.000 vistas",
    "Conocerte": "más visitas al perfil que la pieza anterior del mismo tipo",
    "Seguir": "más seguidores por cada 1.000 vistas que el promedio de la semana",
}
RETO = "Pieza del reto: lleva el sello «Día N de 30». Meta: 1.000 seguidores nuevos, la de la fase 1."

# El mes: 30 días = los 30 días del reto. Cada día, 3 piezas de volumen (V1 el reto, V2 y V3) y, algunos días, una insignia.
# Ritmo fijo por día de la semana (MES-1.md §3): lunes la decisión y una regla · martes la noticia · miércoles IA sin jerga
# y una insignia · jueves la prueba · viernes 3 noticias y una lista · sábado una regla o la fecha del mes y una respuesta ·
# domingo el resumen y lo personal.
# Reto, V1: (titulo, formato, paso)
RETO_V1 = [
    ("El contador en el número real", "loop", "Seguir"), ("El plan de la oficina: quién hace qué", "imagen", "Conocerte"),
    ("El contador y lo que falló", "loop", "Seguir"), ("El comentario que se va a probar", "imagen", "Reaccionar"),
    ("Resumen de los primeros 5 días", "loop", "Seguir"), ("Lo que decidió la oficina el lunes", "imagen", "Conocerte"),
    ("El contador", "loop", "Seguir"), ("El contador: una semana", "loop", "Seguir"),
    ("El contador y lo que se probó", "loop", "Seguir"), ("El comentario que se va a probar", "imagen", "Reaccionar"),
    ("El contador", "loop", "Seguir"), ("Resumen de la semana 2", "loop", "Seguir"),
    ("Lo que decidió la oficina el lunes", "imagen", "Conocerte"), ("El contador", "loop", "Seguir"),
    ("Mitad del reto: cuánto falta", "imagen", "Seguir"), ("El contador y lo que se probó", "loop", "Seguir"),
    ("El comentario que se va a probar", "imagen", "Reaccionar"), ("El contador", "loop", "Seguir"),
    ("Resumen de la semana 3", "loop", "Seguir"), ("Lo que decidió la oficina el lunes", "imagen", "Conocerte"),
    ("El contador", "loop", "Seguir"), ("El contador: faltan 8 días", "loop", "Seguir"),
    ("El contador y lo que se probó", "loop", "Seguir"), ("El comentario que se va a probar", "imagen", "Reaccionar"),
    ("El contador", "loop", "Seguir"), ("Resumen de la semana 4", "loop", "Seguir"),
    ("Lo que decidió la oficina para el cierre", "imagen", "Conocerte"), ("El contador: faltan 3 días", "loop", "Seguir"),
    ("El contador: faltan 24 horas", "loop", "Seguir"), ("El número final", "loop", "Seguir"),
]
NOT = "Una noticia real de IA, verificada en la fuente original y contada para un dueño de negocio: qué pasó y qué le cambia."
RN = "Las 3 noticias de IA de la semana que le importan a un negocio, en 30 s, con fuente y fecha en pantalla."
PRU = "Una prueba real que hace la oficina de IAs, con el resultado tal como salió."
PER = "La cuenta sigue siendo de una persona. Lo sube Kenneth."
RES = "La audiencia ve su comentario en pantalla y vuelve a comentar."
# V2 y V3, día por día: (codigo, serie, formato, titulo, porque, paso, estado)
V2 = [
    ("J1", "IA sin jerga", "motion", "«Prompt» son las instrucciones que le di", "Tema amplio: le enseña a TikTok de qué habla la cuenta. Ya está hecho (pizarra).", "Ver", "producido"),
    ("PR1", "La prueba", "voz", "3 IAs de la oficina: el mismo pedido vago y después completo", PRU + " Muestra el J1 funcionando.", "Pasarlo", "por-hacer"),
    ("RN1", "3 noticias en 30 s", "voz", "Las 3 noticias de IA de la semana", RN, "Ver", "por-hacer"),
    ("F1A", "Fecha del mes", "motion", "Un pit stop dura 2 segundos porque nadie es indispensable", "Fin de semana del GP de Austin (23 al 25 de octubre): la F1 es del mundo de Kenneth.", "Ver", "por-hacer"),
    ("PER1", "Personal", "personal", "Video personal", PER, "Conocerte", "por-hacer"),
    ("R2", "La regla", "motion", "Un sistema que te necesita es una dependencia", "Una regla que se guarda.", "Pasarlo", "por-hacer"),
    ("NS1", "La noticia sin jerga", "voz", "La noticia de la semana, sin jerga", NOT, "Pasarlo", "por-hacer"),
    ("J2", "IA sin jerga", "motion", "Un «agente» es un empleado de IA", "Prepara La Oficina. Coincide con GitHub Universe (28 y 29 de octubre).", "Ver", "por-hacer"),
    ("PR2", "La prueba", "voz", "¿Una IA puede contar el inventario de una soda con una foto?", PRU, "Pasarlo", "por-hacer"),
    ("RN2", "3 noticias en 30 s", "voz", "Las 3 noticias de IA de la semana", RN, "Ver", "por-hacer"),
    ("HAL", "Fecha del mes", "motion", "Lo que de verdad asusta en un negocio: que todo dependa de vos", "31 de octubre: Día de la Mascarada Tradicional Costarricense y Halloween. Mascaradas de papel, con respeto.", "Reaccionar", "por-hacer"),
    ("PER2", "Personal", "personal", "Video personal", PER + " Es el fin de semana del GP de México.", "Conocerte", "por-hacer"),
    ("R1", "La regla", "motion", "El que hace el trabajo no lo revisa", "La regla que sale del 001.", "Pasarlo", "por-hacer"),
    ("NS2", "La noticia sin jerga", "voz", "La noticia de la semana, sin jerga", NOT, "Pasarlo", "por-hacer"),
    ("J3", "IA sin jerga", "motion", "Un «modelo» es una IA", "Una palabra que se oye todos los días.", "Ver", "por-hacer"),
    ("PR3", "La prueba", "voz", "Le pedí a la oficina el manual de apertura de una cafetería", PRU + " Conecta con el 002b.", "Pasarlo", "por-hacer"),
    ("RN3", "3 noticias en 30 s", "voz", "Las 3 noticias de IA de la semana", RN, "Ver", "por-hacer"),
    ("R5", "La regla", "motion", "Nada se hace dos veces", "Ahorro que cualquier negocio entiende. Fin de semana del GP de São Paulo.", "Pasarlo", "por-hacer"),
    ("PER3", "Personal", "personal", "Video personal", PER, "Conocerte", "por-hacer"),
    ("R6", "La regla", "motion", "Lo que no se escribe no pasó", "La regla de la bitácora.", "Pasarlo", "por-hacer"),
    ("NS3", "La noticia sin jerga", "voz", "La noticia de la semana, sin jerga", NOT + " Semana de Web Summit y Adobe MAX.", "Pasarlo", "por-hacer"),
    ("J4", "IA sin jerga", "motion", "Un «workflow» es la cadena de pasos", "Una palabra que el dueño oye y no entiende.", "Ver", "por-hacer"),
    ("PR4", "La prueba", "voz", "La prueba que pidieron en los comentarios", PRU + " La tarea más votada del lunes 9.", "Pasarlo", "por-hacer"),
    ("RN4", "3 noticias en 30 s", "voz", "Las 3 noticias de IA de la semana", RN, "Ver", "por-hacer"),
    ("R7", "La regla", "motion", "La tabla decide quién trabaja, no el capricho", "Cómo se reparte el trabajo sin favoritismos.", "Pasarlo", "por-hacer"),
    ("PER4", "Personal", "personal", "Video personal", PER, "Conocerte", "por-hacer"),
    ("J5", "IA sin jerga", "motion", "Los «tokens» son horas de trabajo", "Explica el costo de la IA sin tecnicismos.", "Ver", "por-hacer"),
    ("NS4", "La noticia sin jerga", "voz", "La noticia de la semana, sin jerga", NOT + " Semana de Microsoft Ignite.", "Pasarlo", "por-hacer"),
    ("J6", "IA sin jerga", "motion", "El «handoff» es la nota de relevo", "Cierra la primera tanda del glosario.", "Ver", "por-hacer"),
    ("FIN", "Reto · Día N de 30", "motion", "Lo que aprendió la oficina en 30 días, en 30 segundos", "El resumen del mes: se guarda y se comparte.", "Seguir", "por-hacer"),
]
V3 = [
    ("P1", "Postura", "imagen", "Si tu negocio no sobrevive a tus vacaciones, no es un negocio", "Opinión fuerte que divide: trae comentarios. Sale del 002.", "Reaccionar", "por-hacer"),
    ("002b", "Amazon en la soda", "voz", "Si tu cafetería recién abierta no sobrevive a tus vacaciones", "Prueba del escenario: cafetería. Voz y motion graphics, $0.", "Pasarlo", "guion"),
    ("L1", "La lista", "carrusel", "La reunión de los lunes en 15 minutos", "Algo que se usa el lunes siguiente: se guarda.", "Pasarlo", "por-hacer"),
    ("002c", "Amazon en la soda", "voz", "Si tu restaurante recién abierto no sobrevive a tus vacaciones", "Prueba del escenario: restaurante. Voz y motion graphics, $0.", "Pasarlo", "guion"),
    ("Q1", "Pregunta", "imagen", "¿Le darías la caja a una IA? Sí o no.", "Obliga a tomar partido en los comentarios.", "Reaccionar", "por-hacer"),
    ("002d", "Amazon en la soda", "voz", "Si acabás de emprender y tu negocio no sobrevive a tus vacaciones", "Prueba del escenario: quien acaba de emprender. Voz y motion graphics, $0.", "Pasarlo", "guion"),
    ("P2", "Postura", "imagen", "Tu mejor empleado es el que menos debería hacer", "Opinión que divide y Kenneth puede defender.", "Reaccionar", "por-hacer"),
    ("N2", "El número", "imagen", "800 personas de capacidad, 25 % de uso", "Un dato real que hace preguntar quién es este.", "Conocerte", "por-hacer"),
    ("N1", "El número", "imagen", "165 personas, 4 países", "Dice quién es Kenneth sin presumir.", "Conocerte", "por-hacer"),
    ("L2", "La lista", "carrusel", "Las 3 cosas que solo vos sabés", "Sale del 002: lo que hay que dejar escrito.", "Pasarlo", "por-hacer"),
    ("RC1", "Respuesta a un comentario", "voz", "Respuesta a un comentario", RES, "Reaccionar", "por-hacer"),
    ("MR1", "La mejor respuesta", "imagen", "La mejor respuesta de la semana", RES, "Reaccionar", "por-hacer"),
    ("Q2", "Pregunta", "imagen", "¿Qué tarea de tu negocio le darías mañana a una IA?", "Las respuestas alimentan las pruebas.", "Reaccionar", "por-hacer"),
    ("P3", "Postura", "imagen", "La IA no te va a quitar el trabajo: te lo va a quitar el compañero que la usa", "Opinión que divide (ESTRATEGIA.md §5).", "Reaccionar", "por-hacer"),
    ("A3", "Amazon en la soda", "voz", "La reunión de los lunes", "Un método de Amazon que un negocio copia el lunes siguiente.", "Pasarlo", "por-hacer"),
    ("N4", "El número", "imagen", "12 semanas, sin contratar a un gerente", "Cierra el caso del anfiteatro.", "Conocerte", "por-hacer"),
    ("L3", "La lista", "carrusel", "Apertura y cierre del local", "Una lista que se usa todos los días.", "Pasarlo", "por-hacer"),
    ("RC2", "Respuesta a un comentario", "voz", "Respuesta a un comentario", RES, "Reaccionar", "por-hacer"),
    ("MR2", "La mejor respuesta", "imagen", "La mejor respuesta de la semana", RES, "Reaccionar", "por-hacer"),
    ("Q3", "Pregunta", "imagen", "¿Cuál es la tarea que más odiás de tu negocio? La oficina prueba la más votada", "Los comentarios eligen la prueba del jueves 12.", "Reaccionar", "por-hacer"),
    ("P4", "Postura", "imagen", "Si tenés que estar para que funcione, no lo construiste: lo cargás", "Opinión que divide. Sale del portafolio.", "Reaccionar", "por-hacer"),
    ("A4", "Amazon en la soda", "voz", "Escribí el titular del día en que ya lo lograste", "Un método de Amazon que cualquiera puede usar.", "Pasarlo", "por-hacer"),
    ("N3", "El número", "imagen", "14 años en una operación que no se apagó", "De dónde sale lo que Kenneth enseña.", "Conocerte", "por-hacer"),
    ("L4", "La lista", "carrusel", "Lo que tu negocio tiene que saber hacer sin vos", "Sale del 002.", "Pasarlo", "por-hacer"),
    ("RC3", "Respuesta a un comentario", "voz", "Respuesta a un comentario", RES, "Reaccionar", "por-hacer"),
    ("MR3", "La mejor respuesta", "imagen", "La mejor respuesta de la semana", RES, "Reaccionar", "por-hacer"),
    ("Q4", "Pregunta", "imagen", "¿Tu negocio aguanta un día de locos sin vos?", "Abre la semana del Black Friday (27 de noviembre) sin vender nada.", "Reaccionar", "por-hacer"),
    ("L5", "La lista", "carrusel", "Para un día de locos: 5 cosas que se dejan escritas", "Se guarda antes del Black Friday.", "Pasarlo", "por-hacer"),
    ("A5", "Amazon en la soda", "voz", "Una evaluación que no dispara nada no sirve", "Todo negocio evalúa y casi ninguno hace algo con el resultado.", "Pasarlo", "por-hacer"),
    ("RC4", "Respuesta a un comentario", "voz", "Respuesta a un comentario", RES, "Reaccionar", "por-hacer"),
]
# Insignias del mes: dia -> (codigo, serie, titulo, porque, paso, estado, reto)
INSIGNIAS = {
    1: ("G0", "¿Cuál soy yo?", "El gemelo se presenta y lanza el reto (Día 1)", "Dice qué es real y qué es IA desde el primer día. Va fijado en el perfil.", "Seguir", "por-hacer", True),
    3: ("002", "Amazon en la soda", "Si tu negocio no sobrevive a tus vacaciones (con el gancho nuevo)", "El caso más cercano a lo que ya le funcionó a la cuenta: Amazon y Costa Rica.", "Pasarlo", "guion-grafico", False),
    5: ("001", "La Oficina", "Mi empleado se calificó su propio examen", "Presenta la serie insignia con el incidente más claro.", "Reaccionar", "guion", False),
    8: ("003", "La Oficina", "Le prohibí trabajar a mi mejor empleado", "El gancho con más puntaje del banco (20 de 20).", "Pasarlo", "guion", False),
    10: ("AMX", "Amazon en la soda", "El escenario que va ganando, ahora con Kenneth", "Sale de la prueba del 002b, 002c y 002d: el que más seguidores trajo por cada 1.000 vistas.", "Pasarlo", "por-hacer", False),
    12: ("004", "Amazon en la soda", "Un anfiteatro para 800 personas al 25 %", "El caso real más fuerte: prueba que el método funciona.", "Pasarlo", "guion", False),
    15: ("DIA15", "Reto · Día N de 30", "Mitad del reto: cuánto llevamos y qué cambió", "El punto medio, con el número real.", "Seguir", "por-hacer", True),
    17: ("005", "La Oficina", "La oficina me avisó tres veces", "Kenneth se equivoca en público: da confianza.", "Reaccionar", "guion", False),
    19: ("TOP1", "El más seguido", "La pieza de volumen que más seguidores trajo, ahora con Kenneth", "Regla del lunes (ESTRATEGIA.md §8.4): se paga el gemelo en lo que ya demostró que hace seguir.", "Seguir", "por-hacer", False),
    22: ("O6", "La Oficina", "Cuando el gerente se queda sin horas, ¿quién manda?", "Todo dueño se pregunta quién manda si él falta.", "Reaccionar", "por-hacer", False),
    26: ("TOP2", "El más seguido", "La segunda pieza que más seguidores trajo, ahora con Kenneth", "Misma regla del lunes.", "Seguir", "por-hacer", False),
    30: ("DIA30", "Reto · Día N de 30", "Día 30: ¿llegamos? Se cuenta igual", "El cierre del reto, llegue o no. El contador nunca se infla.", "Seguir", "por-hacer", True),
}
PIEZAS = []
for _d in range(1, 31):
    _t, _f, _p = RETO_V1[_d - 1]
    PIEZAS.append((_d, "volumen", _f, f"D{_d}", "Reto · Día N de 30", _t, "La pieza diaria del reto: el número real, lo que se intentó y lo que falló.", _p, "por-hacer", True))
    for _cod, _serie, _fmt, _tit, _porque, _paso, _est in (V2[_d - 1], V3[_d - 1]):
        PIEZAS.append((_d, "volumen", _fmt, _cod, _serie, _tit, _porque, _paso, _est, _cod == "FIN"))
    if _d in INSIGNIAS:
        _cod, _serie, _tit, _porque, _paso, _est, _reto = INSIGNIAS[_d]
        PIEZAS.append((_d, "insignia", "insignia", _cod, _serie, _tit, _porque, _paso, _est, _reto))
FORMATOS = {"loop": "loop de 3 a 8 s", "imagen": "imagen", "carrusel": "carrusel", "motion": "motion graphics", "voz": "voz sobre animación",
            "personal": "video personal", "insignia": "insignia con el gemelo"}

# dia del reto (0 = antes del Día 1), titulo, porque, quien
LUNES = ("Seguidores nuevos contra la semana anterior, seguidores por cada 1.000 vistas por serie y tipo, qué paso empuja "
         "a seguir y una sola decisión (ESTRATEGIA.md §8).")
ACCIONES = [
    (0, "Responder las 8 preguntas del arranque", "Están en Pendientes. Sin ellas no arranca el Día 1.", "Kenneth"),
    (0, "Cargar unos $5 en HeyGen", "Lo de las 3 insignias de la semana 1 (unos $7.60); quedan $2.88.", "Kenneth"),
    (0, "Poner nombre, bio y foto del perfil", "ESTRATEGIA.md §7. Se hace una vez, antes del Día 1.", "Kenneth"),
    (0, "Aprobar el lote de la semana 1", "Un guion gráfico con las 21 piezas de volumen.", "Kenneth"),
    (1, "Leer los seguidores del Día 1 en TikTok e Instagram", "De los perfiles públicos. Es el número del contador y la vara del mes.", "Claude"),
    (5, "Aprobar el lote de la semana siguiente", "El domingo, un solo guion gráfico con las 21 piezas.", "Kenneth"),
    (6, "Revisión del lunes", LUNES, "Kenneth y Claude"),
    (6, "Impulsar la pieza que más seguidores trajo", "TikTok Promote, objetivo «más seguidores», $5.", "Kenneth"),
    (9, "Elegir el escenario de Amazon en la soda", "El 002b, el 002c o el 002d: el que más seguidores trajo por cada 1.000 vistas va con el gemelo el viernes.", "Kenneth y Claude"),
    (12, "Aprobar el lote de la semana siguiente", "Un solo guion gráfico con las 21 piezas.", "Kenneth"),
    (13, "Revisión del lunes", LUNES, "Kenneth y Claude"),
    (13, "Impulsar la pieza que más seguidores trajo", "TikTok Promote, $5.", "Kenneth"),
    (15, "Mitad del reto: revisar el plan", "Qué series se quedan y cuáles cambian para la segunda mitad.", "Kenneth y Claude"),
    (19, "Aprobar el lote de la semana siguiente", "Un solo guion gráfico con las 21 piezas.", "Kenneth"),
    (20, "Revisión del lunes", LUNES, "Kenneth y Claude"),
    (20, "Impulsar la pieza que más seguidores trajo", "TikTok Promote, $5.", "Kenneth"),
    (26, "Aprobar el lote de la semana siguiente", "Un solo guion gráfico con las piezas que faltan.", "Kenneth"),
    (27, "Revisión del lunes", LUNES, "Kenneth y Claude"),
    (27, "Impulsar la pieza que más seguidores trajo", "TikTok Promote, $5.", "Kenneth"),
    (30, "Cierre del mes", "Seguidores ganados, qué serie y qué tipo de pieza convirtieron, y el plan del mes 2.", "Kenneth y Claude"),
]

# id, titulo, detalle, quien, para, hecho
TAREAS = [
    ("k-reto", "Sí al reto de 30 días, a 1.000 seguidores", "La meta de la fase 1, contada en público. El G0 pasa por guion gráfico.", "Kenneth", "2026-10-20", True),
    ("k-heygen", "Cargar unos $5 en HeyGen", "Lo de las 3 insignias de la semana 1 (unos $7.60); quedan $2.88. Se carga por semana, solo lo de sus insignias.", "Kenneth", "2026-10-20", False),
    ("k-dia1", "Seguidores de hoy en TikTok e Instagram", "Ya no hace falta que los pases: los leo de los perfiles públicos. 19-oct: TikTok 1.080, Instagram 578.", "Kenneth", "2026-10-20", True),
    ("k-perfil", "Poner nombre, bio y foto del perfil", "«Kenneth Picado · Dirijo una oficina de IAs». La bio está en ESTRATEGIA.md §7. La misma foto en las dos redes.", "Kenneth", "2026-10-20", False),
    ("k-lote", "Sí a aprobar en lote, con guion gráfico primero", "Siempre un guion gráfico barato primero; el contenido real, solo cuando lo aprobás.", "Kenneth", "2026-10-20", True),
    ("k-facebook", "Crear la página «Kenneth Picado» y conectarla en Buffer", "Es la tercera red gratis de Buffer. Avisame cuando esté y reviso qué canales ve.", "Kenneth", "2026-10-21", False),
    ("k-xli", "X y LinkedIn: ¿ya o en la fase 2?", "Ya cuesta unos $25 al mes en Buffer. La estrategia los deja para la fase 2.", "Kenneth", "2026-10-21", False),
    ("k-bernal", "Hablar con Bernal", "Pasarle el carrusel de aires (es terreno de Cawhi) y consultarle la idea A8, que toca ventas.", "Kenneth", "2026-10-23", False),
    ("k-arranca", "Decir «arranca»", "El Día 1 es el miércoles 21 de octubre.", "Kenneth", "2026-10-20", True),
    ("k-j1", "Aprobar el J1 en estilo pizarra", "Está hecho; va en el Día 1. Si no te convence el estilo, se cambia antes de hacer los otros.", "Kenneth", "2026-10-20", False),
    ("k-blob", "Crear el almacén Blob de la consola en Vercel", "Proyecto kennethpicado-consola → Storage → Blob, acceso Private. Sin eso, la consola de Vercel no guarda lo que marcás.", "Kenneth", "2026-10-22", False),
    ("c-consola", "Alinear la consola con la estrategia", "Seguidores nuevos como meta, la cadena, volumen e insignias, y la semana 1.", "Claude", "2026-10-19", True),
    ("c-costeo", "Alinear el costeo", "Costo por seguidor nuevo de cada insignia.", "Claude", "2026-10-19", True),
    ("c-lote", "Guion gráfico de la semana 1", "Las 21 piezas de volumen y las 3 insignias, en bocetos de $0. Está en Guiones.", "Claude", "2026-10-19", True),
    ("c-002", "Rehacer el gancho del 002 hasta pasar la vara", "Los 3 ganchos nuevos están en el guion gráfico de la semana 1. Con tu sí van a la prueba: 70 de total, 60 de gancho y 90 de «sostiene» (el mejor intento sacó 56).", "Claude", "2026-10-21", False),
    ("c-g0", "Prueba de gancho del G0", "Su boceto está en el guion gráfico de la semana 1. Con tu sí, la prueba y después el gemelo.", "Claude", "2026-10-21", False),
    ("c-001", "Prueba de gancho del 001", "Su boceto está en el guion gráfico de la semana 1. Con tu sí, la prueba y después el gemelo.", "Claude", "2026-10-22", False),
    ("c-002bcd", "Hacer el 002b, el 002c y el 002d", "Voz y motion graphics, $0, después de tu sí al guion gráfico. Gana el escenario con más seguidores por cada 1.000 vistas.", "Claude", "2026-10-22", False),
    ("c-reto", "Plantilla del contador «Día N de 30»", "Un loop que se rehace cada día con el número, después de tu sí al guion gráfico.", "Claude", "2026-10-21", False),
    ("c-buffer", "Programar en Buffer (E003)", "Con tu aprobación antes de cada publicación. Hasta que esté, se publica a mano.", "Claude", "2026-10-23", False),
    ("c-medicion", "Cargar los números a las 48 horas y a los 7 días", "Seguidores nuevos por pieza y por semana, y la revisión de los lunes.", "Claude", "2026-10-23", False),
]

GUIONES = {
    "j1-v1": {
        "titulo": "J1 · «Prompt» son las instrucciones que le di", "version": "v1", "estado": "por-aprobar",
        "nota": "Estilo pizarra. Está hecho (24,6 s, $0) y va en el Día 1 como volumen. Si te gusta, la serie IA sin jerga sale así.",
        "comentario": "", "paginas": ["guiones/j1-v1-1.webp", "guiones/j1-v1-2.webp"], "orden": 1,
    },
    "lote-s1": {
        "titulo": "Semana 1 · del 21 al 27 de octubre", "version": "v1 · boceto", "estado": "por-aprobar",
        "nota": "Las 21 piezas de volumen y las 3 insignias de la semana, una página por día, en bocetos de $0. Con tu sí se hace el contenido real; si algo no te gusta, decime qué pieza y qué cambiar.",
        "comentario": "", "paginas": [f"guiones/lote-s1-dia-{d}.webp" for d in range(1, 8)], "orden": 0,
    },
    "002-v4": {
        "titulo": "002 · Si tu negocio no sobrevive a tus vacaciones", "version": "v4", "estado": "por-aprobar",
        "nota": "Insignia del Día 3. El video existe; el gancho se rehace hasta pasar la vara de la estrategia (70 / 60 / 90) antes de pagar el gemelo.",
        "comentario": "", "paginas": ["guiones/002-v4-1.webp", "guiones/002-v4-2.webp", "guiones/002-v4-3.webp"], "orden": 2,
    },
}

CONEXIONES = {
    "tiktok": {"nombre": "TikTok", "tipo": "red", "estado": "conectada", "detalle": "@picado80, por Buffer. 3 piezas de volumen por día y las insignias.", "orden": 1},
    "instagram": {"nombre": "Instagram", "tipo": "red", "estado": "conectada", "detalle": "@picado80, por Buffer. 1 por día (la de volumen que mejor le fue el día anterior en TikTok) y las insignias.", "orden": 2},
    "facebook": {"nombre": "Facebook", "tipo": "red", "estado": "falta", "detalle": "Falta crear la página «Kenneth Picado» y conectarla en Buffer: es la tercera red gratis. Recibe lo mismo que Instagram.", "orden": 3},
    "x": {"nombre": "X", "tipo": "red", "estado": "despues", "detalle": "Fase 2, o ya por unos $25 al mes en Buffer: espera tu respuesta.", "orden": 4},
    "linkedin": {"nombre": "LinkedIn", "tipo": "red", "estado": "despues", "detalle": "Fase 2, o ya por unos $25 al mes en Buffer: espera tu respuesta.", "orden": 5},
    "youtube": {"nombre": "YouTube", "tipo": "red", "estado": "despues", "detalle": "Kenneth crea el canal cuando pueda.", "orden": 6},
    "buffer": {"enlace": "https://publish.buffer.com", "nombre": "Buffer", "tipo": "herramienta", "estado": "conectada", "detalle": "Plan gratis: 3 redes, 10 programadas por red y 3.000 llamadas al mes. Hoy, 2 redes.", "orden": 10},
    "heygen": {"enlace": "https://app.heygen.com", "nombre": "HeyGen", "tipo": "herramienta", "estado": "conectada", "detalle": "El gemelo «Kenneth GP», por la API v3 (la v2 se apaga el 31-oct). $0.0805 por segundo.", "orden": 11},
    "elevenlabs": {"nombre": "ElevenLabs", "tipo": "herramienta", "estado": "conectada", "detalle": "Tu voz clonada, los tiempos de cada palabra y los efectos.", "orden": 12},
    "higgsfield": {"nombre": "Higgsfield", "tipo": "herramienta", "estado": "conectada", "detalle": "La prueba de gancho de las insignias (gratis, hasta 16 s).", "orden": 13},
    "hyperframes": {"nombre": "HyperFrames y Lemo-Opuscar", "tipo": "herramienta", "estado": "conectada", "detalle": "Todo el volumen, con código, en tu PC. $0.", "orden": 14},
    "pixabay": {"enlace": "https://pixabay.com/api/docs/", "nombre": "Pixabay", "tipo": "herramienta", "estado": "falta", "detalle": "Video de banco gratis para el volumen. Falta la llave.", "orden": 15},
}

SALDOS = {
    "heygen": {"nombre": "HeyGen", "valor": "$2.88", "detalle": "No alcanza para las 3 insignias de la semana 1 (unos $7.60). Faltan unos $5.", "alerta": True, "orden": 1},
    "elevenlabs": {"nombre": "ElevenLabs", "valor": "313 de 186.000", "detalle": "Caracteres del mes. Plan fijo de $22.", "alerta": False, "orden": 2},
    "higgsfield": {"nombre": "Higgsfield", "valor": "200 créditos", "detalle": "La prueba de gancho no gasta créditos.", "alerta": False, "orden": 3},
    "claude": {"nombre": "Claude", "valor": "Plan Max", "detalle": "Sin cobros extra.", "alerta": False, "orden": 4},
}

NOTAS = {
    "redes": "Fase 1: TikTok lleva todo; Instagram, 1 pieza por día más las insignias; Facebook, lo mismo que Instagram cuando esté. X y LinkedIn, en la fase 2. Conectar una red lo hace Kenneth, porque pide iniciar sesión.",
}

OBJETIVOS = {
    "norte": {
        "titulo": "Seguidores nuevos por semana", "que": "En TikTok más Instagram. Es la única métrica que importa al final (ESTRATEGIA.md §1).",
        "meta": 0, "meta_texto": "la semana 1 fija la vara; después, cada semana más que la anterior", "actual": 0, "periodo": "la semana 1",
    },
    "items": {
        "ver": {"nombre": "Ver", "busca": "Que lo vea completo gente que no te conoce.", "mide": "Retención a los 3 s y vio completo", "vara": VARAS["Ver"], "excelente": "", "cuenta": ["Ver"], "orden": 1},
        "reaccionar": {"nombre": "Reaccionar", "busca": "Me gusta, comentarios y la discusión.", "mide": "Comentarios por cada 1.000 vistas", "vara": VARAS["Reaccionar"], "excelente": "", "cuenta": ["Reaccionar"], "orden": 2},
        "pasarlo": {"nombre": "Pasarlo", "busca": "Que lo compartan o lo guarden: así llega a gente nueva.", "mide": "Compartidos y guardados por cada 1.000 vistas", "vara": VARAS["Pasarlo"], "excelente": "", "cuenta": ["Pasarlo"], "orden": 3},
        "conocerte": {"nombre": "Conocerte", "busca": "Que quieran saber quién es.", "mide": "Visitas al perfil", "vara": VARAS["Conocerte"], "excelente": "", "cuenta": ["Conocerte"], "orden": 4},
        "seguir": {"nombre": "Seguir", "busca": "La meta: que te sigan.", "mide": "Seguidores nuevos por cada 1.000 vistas", "vara": VARAS["Seguir"], "excelente": "", "cuenta": ["Seguir"], "orden": 5},
    },
    "ritmo": {
        "tiktok": {"nombre": "TikTok", "texto": "3 piezas de volumen por día (loop, imagen o carrusel, motion, voz) y 2 o 3 insignias por semana.", "orden": 1},
        "instagram": {"nombre": "Instagram", "texto": "1 por día, la de volumen que mejor le fue ayer en TikTok, y las insignias.", "orden": 2},
        "personal": {"nombre": "Lo personal", "texto": "1 por semana, como siempre.", "orden": 3},
        "fuera": {"nombre": "Fuera de la fase 1", "texto": "Vender, nombrar SEMI o RedTurn, buscar empresas, LinkedIn, X y anuncios de venta.", "orden": 4},
    },
    "base": {
        "fecha": "9 de octubre",
        "datos": [
            {"etiqueta": "Seguidores hoy (TikTok + Instagram)", "valor": "falta el dato"},
            {"etiqueta": "TikTok: vistas de un video normal", "valor": "326"},
            {"etiqueta": "TikTok: comentarios por cada 1.000 vistas", "valor": "2"},
            {"etiqueta": "TikTok: compartidos y guardados", "valor": "0"},
            {"etiqueta": "Instagram: seguidores", "valor": "576"},
        ],
    },
    "fases": [
        {"nombre": "1 · Probar", "cuando": "hasta 1.000 seguidores nuevos", "texto": "Se busca qué serie y qué tipo de pieza hace seguir."},
        {"nombre": "2 · Duplicar", "cuando": "de 1.000 a 10.000", "texto": "70 % de lo que mejor convierte y 30 % de pruebas."},
        {"nombre": "3 · Introducir", "cuando": "más de 10.000", "texto": "SEMI aparece en 1 de cada 10 piezas, sin precio."},
    ],
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    DATOS.mkdir(exist_ok=True)
    dia = lambda n: (ARRANQUE + timedelta(days=n - 1)).isoformat()      # noqa: E731
    items = {}
    for n, (d, tipo, formato, cod, serie, titulo, porque, paso, estado, reto) in enumerate(PIEZAS):
        insignia = tipo == "insignia"
        items[f"p-d{d:02d}-{cod}"] = {
            "fecha": dia(d), "dia": d, "linea": "B" if insignia else "A", "tipo": tipo, "formato": formato, "formato_texto": FORMATOS[formato],
            "codigo": cod, "serie": serie, "titulo": titulo, "porque": (porque + " " + RETO) if reto else porque, "reto": reto,
            "objetivo": paso, "vara": VARAS[paso], "redes": ["tiktok", "instagram"] if insignia else ["tiktok"],
            "estado": estado, "quien": "Kenneth" if formato == "personal" else "Claude", "costo": COSTO_INSIGNIA if insignia else 0, "orden": n,
        }
    for n, (d, titulo, porque, quien) in enumerate(ACCIONES):
        fecha = dia(d) if d > 0 else (ARRANQUE - timedelta(days=1)).isoformat()
        items[f"m-{fecha}-{n}"] = {"fecha": fecha, "dia": d, "linea": "M", "tipo": "accion", "formato": "", "codigo": "", "serie": "Marca", "titulo": titulo,
                                   "porque": porque, "objetivo": "", "vara": "", "estado": "pendiente", "quien": quien, "costo": 0, "orden": 100 + n}
    tareas = {i: {"titulo": t, "detalle": d, "quien": q, "para": p, "hecho": h, "orden": n} for n, (i, t, d, q, p, h) in enumerate(TAREAS)}
    insignias = sum(1 for p in PIEZAS if p[1] == "insignia")
    presupuesto = {
        "tope": 100, "gastado": 30.12, "proyectado": round(22 + insignias * COSTO_INSIGNIA + 20, 2), "proyectado_texto": "El mes del reto",
        "detalle": f"Octubre hasta hoy: $22 de ElevenLabs y $8.12 de HeyGen. El mes del reto: {insignias} insignias (unos ${insignias * COSTO_INSIGNIA:.0f}), voz $22, impulso $20; el volumen, $0.",
        "por_video": COSTO_INSIGNIA, "meta_por_video": 4.0,
    }
    docs = {
        "calendario": {"items": items, "arranque": {"fecha": ARRANQUE.isoformat(), "provisional": False}},
        "tareas": {"items": tareas},
        "guiones": {"items": GUIONES},
        "estado": {"actualizado": ACTUALIZADO, "conexiones": CONEXIONES, "saldos": SALDOS, "presupuesto": presupuesto, "notas": NOTAS},
        "objetivos": OBJETIVOS,
    }
    for nombre, cuerpo in docs.items():
        (DATOS / f"{nombre}.json").write_text(json.dumps(cuerpo, ensure_ascii=False, indent=1), encoding="utf-8")
        print(nombre, len(json.dumps(cuerpo)), "bytes")
    vol = [p for p in PIEZAS if p[1] == "volumen"]
    assert len(vol) == 90 and insignias == 12, (len(vol), insignias)
    for d in range(1, 31):
        assert sum(1 for p in vol if p[0] == d) == 3, d
    assert len({(p[0], p[3]) for p in PIEZAS}) == len(PIEZAS), "códigos repetidos el mismo día"
    print(f"el mes: {len(vol)} de volumen ({sum(1 for p in vol if p[9])} del reto) y {insignias} insignias, del {ARRANQUE.isoformat()} al {dia(30)}")


if __name__ == "__main__":
    main()
