"""Genera las semillas de la consola de marca en marca/consola/datos/*.json.

Uso (desde la raíz de kennethpicado):
    python marca/consola/sembrar.py

No llama a ninguna API. Los saldos y las conexiones se pasan a mano arriba, con la fecha en que se midieron.
Ojo: cargar estas semillas pisa lo que Kenneth marcó en la consola (ver LEEME.md).
"""
import json
import sys
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos"
ACTUALIZADO = "2026-10-12T16:00:00-06:00"
COSTO_B = 1.83

VARAS = {
    "Alcance": "pasa de 326 vistas",
    "Guardado": "al menos 1 guardado",
    "Compartido": "al menos 1 compartido",
    "Comentario": "al menos 2 comentarios de gente nueva",
    "Perfil": "más visitas al perfil que el video anterior",
    "Perfil y empresa": "más visitas al perfil, o un mensaje de una empresa",
}

SERIES = {
    "J": "IA sin jerga", "R": "La regla", "C": "Las cinco capas", "L": "La lista", "N": "El número",
    "AM": "Amazon en la soda", "OF": "La Oficina", "SI": "Sistema de la semana", "RC": "Respuesta a un comentario",
    "TOP": "El más visto", "G": "¿Cuál soy yo?",
}
ECO = "Deja en una frase el video de ayer, para guardarlo."
RC = "La audiencia empieza a dictar los temas."
TOP = "El gemelo se usa en un tema que ya probó que pega."

# Dos piezas por día (Kenneth, 12-oct): un gráfico (A) y un video con Kenneth (B). Todo sale en TikTok.
# La última columna marca las 3 por semana que también van a Instagram.
# fecha, linea, codigo, serie, titulo, porque, objetivo, instagram
PIEZAS = [
    # semana 42
    ("2026-10-13", "A", "J1", "J", "«Prompt» son las instrucciones que le di", "Tema amplio, para que TikTok empiece a mostrar la cuenta a gente interesada en IA.", "Alcance", False),
    ("2026-10-13", "B", "002", "AM", "Si tu negocio no sobrevive a tus vacaciones", "El primer video de la marca entra por lo que ya le funcionó a la cuenta: Amazon y Costa Rica.", "Guardado", True),
    ("2026-10-14", "A", "R2", "R", "Un sistema que te necesita es una dependencia", ECO, "Guardado", False),
    ("2026-10-14", "B", "A3", "AM", "La reunión de los lunes", "Un método de Amazon que un negocio puede copiar el lunes siguiente.", "Guardado", False),
    ("2026-10-15", "A", "L1", "L", "La reunión de los lunes en 15 minutos", "La lista del video de ayer, para guardarla.", "Guardado", False),
    ("2026-10-15", "B", "004", "AM", "Un anfiteatro para 800 personas al 25 %", "El caso real más fuerte: prueba que el método funciona.", "Compartido", True),
    ("2026-10-16", "A", "N2", "N", "800 personas de capacidad, 25 % de uso", "El dato del video de ayer, solo.", "Perfil", False),
    ("2026-10-16", "B", "A4", "AM", "Escribí el titular del día en que ya lo lograste", "Un método de Amazon que cualquiera puede usar.", "Guardado", False),
    ("2026-10-17", "A", "J2", "J", "Un «agente» es un empleado de IA", "Prepara el terreno para La Oficina, que empieza hoy.", "Alcance", False),
    ("2026-10-17", "B", "001", "OF", "Mi empleado se calificó su propio examen", "Presenta la serie insignia con el incidente más claro.", "Comentario", False),
    ("2026-10-18", "A", "R1", "R", "El que hace el trabajo no lo revisa", ECO, "Guardado", True),
    ("2026-10-18", "B", "003", "OF", "Le prohibí trabajar a mi mejor empleado", "El gancho con más puntaje del banco (20 de 20).", "Compartido", False),
    # semana 43
    ("2026-10-19", "A", "R4", "R", "El mejor no hace todo: decide y revisa", ECO, "Guardado", False),
    ("2026-10-19", "B", "005", "OF", "La oficina me avisó tres veces", "Kenneth se equivoca en público: da confianza.", "Comentario", False),
    ("2026-10-20", "A", "R3", "R", "Un aviso sin dueño y sin fecha es decoración", ECO, "Guardado", False),
    ("2026-10-20", "B", "G0", "G", "Los videos de esta semana no los grabé yo", "El gemelo se presenta solo: mejor contarlo con humor que dejar que alguien lo descubra. Falta el sí de Kenneth.", "Comentario", True),
    ("2026-10-21", "A", "J3", "J", "Un «modelo» es una IA", "Mantiene el alcance entre semana.", "Alcance", False),
    ("2026-10-21", "B", "S2", "SI", "Las notas de voz de WhatsApp convertidas en pasos", "Primera prueba en pantalla: un problema que todos tienen.", "Perfil y empresa", True),
    ("2026-10-22", "A", "C1", "C", "1 de 5: lo que se escribe", "Abre una miniserie: quien ve una capa busca las otras.", "Guardado", False),
    ("2026-10-22", "B", "A5", "AM", "Una evaluación que no dispara nada no sirve", "Todo negocio evalúa a su gente y casi ninguno hace algo con el resultado.", "Compartido", False),
    ("2026-10-23", "A", "N1", "N", "165 personas, 4 países", "Dice quién es Kenneth sin presumir.", "Perfil", True),
    ("2026-10-23", "B", "RC1", "RC", "El mejor comentario de la semana", RC, "Comentario", False),
    ("2026-10-24", "A", "J4", "J", "Un «workflow» es la cadena de pasos", "Una palabra que el dueño oye y no entiende.", "Alcance", False),
    ("2026-10-24", "B", "O7", "OF", "Contraté a un practicante gratis", "Tono liviano para el sábado.", "Compartido", False),
    ("2026-10-25", "A", "C2", "C", "2 de 5: lo que se cuenta todos los días", "Sigue la miniserie.", "Guardado", False),
    ("2026-10-25", "B", "TOP1", "TOP", "El gráfico más visto de la semana, ahora con Kenneth", TOP, "Alcance", False),
    # semana 44
    ("2026-10-26", "A", "C3", "C", "3 de 5: lo que se revisa cada semana", "Sigue la miniserie.", "Guardado", False),
    ("2026-10-26", "B", "O6", "OF", "Cuando el gerente se queda sin horas, ¿quién manda?", "Todo dueño se pregunta quién manda si él falta.", "Comentario", True),
    ("2026-10-27", "A", "J5", "J", "Los «tokens» son horas de trabajo", "Explica el costo de la IA sin tecnicismos y prepara el video de hoy.", "Alcance", False),
    ("2026-10-27", "B", "O3", "OF", "Despedí a una IA", "Una decisión de plata que cualquier dueño entiende: no pagar dos veces por lo mismo.", "Comentario", False),
    ("2026-10-28", "A", "N3", "N", "14 años en una operación que no se apagó", "De dónde sale lo que Kenneth enseña.", "Perfil", False),
    ("2026-10-28", "B", "S1", "SI", "La factura te dice a quién comprarle más barato", "Un sistema que le ahorra plata al dueño. SEMI aparece como «lo que construyo».", "Perfil y empresa", True),
    ("2026-10-29", "A", "C4", "C", "4 de 5: lo que ve el que dirige", "Sigue la miniserie.", "Guardado", False),
    ("2026-10-29", "B", "G1", "G", "La nota de voz de «tu hijo» pidiendo plata", "Algo que la gente le manda a su familia.", "Compartido", False),
    ("2026-10-30", "A", "L2", "L", "Las 3 cosas que solo vos sabés", "Sale del 002: lo que hay que dejar escrito antes de irse de vacaciones.", "Guardado", True),
    ("2026-10-30", "B", "RC2", "RC", "El mejor comentario de la semana", RC, "Comentario", False),
    ("2026-10-31", "A", "J6", "J", "El «handoff» es la nota de relevo", "Otra palabra de IA traducida a oficina.", "Alcance", False),
    ("2026-10-31", "B", "O4", "OF", "Mis empleados llevan bitácora", "Muestra la oficina de IAs por dentro.", "Compartido", False),
    ("2026-11-01", "A", "C5", "C", "5 de 5: lo que se decide los lunes", "Cierra la miniserie.", "Guardado", False),
    ("2026-11-01", "B", "TOP2", "TOP", "El gráfico más visto de la semana, ahora con Kenneth", TOP, "Alcance", False),
    # semana 45
    ("2026-11-02", "A", "R6", "R", "Lo que no se escribe no pasó", "La regla que sale del video de la bitácora.", "Guardado", False),
    ("2026-11-02", "B", "C6", "C", "Las cinco capas, de corrido", "Junta la miniserie en un solo video con Kenneth.", "Guardado", True),
    ("2026-11-03", "A", "J8", "J", "El «log» es la bitácora", "Otra palabra de IA traducida a oficina.", "Alcance", False),
    ("2026-11-03", "B", "O8", "OF", "Nada se hace dos veces", "Ahorro que cualquier negocio entiende, contado como historia.", "Comentario", False),
    ("2026-11-04", "A", "R5", "R", "Nada se hace dos veces", ECO, "Guardado", False),
    ("2026-11-04", "B", "S3", "SI", "La cámara mágica", "Un sistema hecho para un evento real.", "Perfil y empresa", False),
    ("2026-11-05", "A", "J7", "J", "«Dispatch» es pasarle el trabajo", "Otra palabra de IA traducida a oficina.", "Alcance", False),
    ("2026-11-05", "B", "G3", "G", "Con 30 segundos de audio se clona una voz", "Qué hacer con las notas de voz de la familia: es de los que se comparten.", "Compartido", True),
    ("2026-11-06", "A", "N4", "N", "12 semanas, sin contratar a un gerente", "Cierra el caso del anfiteatro.", "Perfil", False),
    ("2026-11-06", "B", "RC3", "RC", "El mejor comentario de la semana", RC, "Comentario", False),
    ("2026-11-07", "A", "L3", "L", "Apertura y cierre del local", "Una lista que se usa todos los días.", "Guardado", True),
    ("2026-11-07", "B", "S4", "SI", "11 bolsas de empleo a la vez", "Tema amplio. Atrae más a quien busca trabajo que a quien contrata: va una sola vez.", "Alcance", False),
    ("2026-11-08", "A", "R7", "R", "La tabla decide quién trabaja, no el capricho", "Cómo se reparte el trabajo sin favoritismos.", "Guardado", False),
    ("2026-11-08", "B", "TOP3", "TOP", "El gráfico más visto del mes, ahora con Kenneth", TOP, "Alcance", False),
]

REVISION = "Cada pieza contra su objetivo. La serie que falla cambia de gancho; la que cumple se repite."
# fecha, titulo, porque, quien
ACCIONES = [
    ("2026-10-12", "Aprobar los guiones gráficos de la semana 1", "Sin el visto bueno no se produce nada.", "Kenneth"),
    ("2026-10-12", "Recargar HeyGen", "Quedan $2.88: alcanza para un video. Con dos piezas por día el mes necesita unos $50.", "Kenneth"),
    ("2026-10-17", "Video personal, como los de siempre", "La cuenta sigue siendo de una persona (regla del arranque).", "Kenneth"),
    ("2026-10-17", "Grabar 3 o 4 tomas más para el gemelo, sin audífono", "Para que los videos puedan cortar entre encuadres.", "Kenneth"),
    ("2026-10-19", "Revisión de la semana 1", REVISION, "Kenneth y Claude"),
    ("2026-10-26", "Revisión de la semana 2", REVISION, "Kenneth y Claude"),
    ("2026-11-02", "Revisión de la semana 3", REVISION, "Kenneth y Claude"),
    ("2026-11-09", "Revisión del mes", "Qué series se quedan, cuáles cambian de gancho, cuánto costó y cuántas empresas escribieron.", "Kenneth y Claude"),
    ("2026-11-09", "SEMI: las 8 preguntas en ChatGPT", "Medición mensual de si ChatGPT ya menciona a SEMI.", "Kenneth"),
]

# id, titulo, detalle, quien, para, hecho
TAREAS = [
    ("k-calendario", "Aprobar el calendario", "Decidido el 12-oct: dos piezas por día en TikTok y tres por semana en Instagram.", "Kenneth", "2026-10-12", True),
    ("k-002", "Aprobar el 002 con el inicio nuevo", "Abre con «En Amazon nadie era indispensable. Ni el jefe.» (fue el inicio con mejor puntaje).", "Kenneth", "2026-10-13", False),
    ("k-heygen", "Recargar HeyGen", "Quedan $2.88. Con dos piezas por día, el mes necesita unos $50.", "Kenneth", "2026-10-12", False),
    ("k-enlace", "Crear el proyecto de la consola en Vercel", "En tu cuenta personal de Vercel: importar el repo con la carpeta marca/consola, crear el almacén Blob privado y activar la protección. Los pasos están en el LEEME de la consola.", "Kenneth", "2026-10-13", False),
    ("k-pixabay", "Sacar la llave gratis de Pixabay", "En pixabay.com/api/docs. Pegarla en torre\\.env como PIXABAY_API_KEY=", "Kenneth", "2026-10-14", False),
    ("k-redes", "Conectar Facebook en Buffer", "Ocupa el tercer lugar gratis y recibe las mismas 3 piezas de Instagram. X espera. LinkedIn: sin publicar por ahora.", "Kenneth", "2026-10-14", False),
    ("k-g0", "Decidir si sale el video donde el gemelo se presenta", "Martes 20: «Los videos de esta semana no los grabé yo». Si no querés, lo cambio por otro.", "Kenneth", "2026-10-16", False),
    ("k-tomas", "Grabar 3 o 4 tomas más para el gemelo", "2 minutos cada una, sin audífono: cerca, sentado más lejos, de pie y con otro fondo.", "Kenneth", "2026-10-17", False),
    ("k-personal", "Subir un video personal", "Como los de siempre: la cuenta sigue siendo tuya.", "Kenneth", "2026-10-17", False),
    ("k-openai", "SEMI: verificar la organización en OpenAI", "En platform.openai.com. Tarda, conviene empezar ya.", "Kenneth", "2026-10-16", False),
    ("c-002", "Rehacer el 002 con el inicio nuevo", "Guion gráfico primero; después el video.", "Claude", "2026-10-12", False),
    ("c-semana1", "Guion gráfico de los gráficos de la semana 1", "Los seis juntos: J1, R2, L1, N2, J2 y R1.", "Claude", "2026-10-13", False),
    ("c-a3", "Guion y guion gráfico del A3", "La reunión de los lunes.", "Claude", "2026-10-13", False),
    ("c-004", "Guion gráfico del 004", "El anfiteatro.", "Claude", "2026-10-14", False),
    ("c-a4", "Guion y guion gráfico del A4", "El titular del día en que ya lo lograste.", "Claude", "2026-10-15", False),
    ("c-oficina", "Guiones gráficos del 001 y del 003", "Los dos primeros de La Oficina.", "Claude", "2026-10-16", False),
    ("c-plantillas", "Plantillas por serie", "Para que cada gráfico nuevo salga de datos y no se arme de cero.", "Claude", "2026-10-14", False),
    ("c-buffer", "Programar las publicaciones en Buffer", "Con la aprobación de Kenneth antes de cada una (encargo E003).", "Claude", "2026-10-16", False),
    ("c-medicion", "Cargar los resultados a las 48 horas y a los 7 días", "Cada pieza contra su objetivo, en la sección Resultados.", "Claude", "2026-10-15", False),
]

GUIONES = {
    "002-v4": {
        "titulo": "002 · Si tu negocio no sobrevive a tus vacaciones", "version": "v4", "estado": "por-aprobar",
        "nota": "El video ya existe. Falta decidir si se rehace el inicio con «nadie era indispensable».",
        "comentario": "", "paginas": ["guiones/002-v4-1.webp", "guiones/002-v4-2.webp", "guiones/002-v4-3.webp"], "orden": 1,
    },
}

CONEXIONES = {
    "tiktok": {"nombre": "TikTok", "tipo": "red", "estado": "conectada", "detalle": "@picado80, por Buffer. Dos piezas por día.", "orden": 1},
    "instagram": {"nombre": "Instagram", "tipo": "red", "estado": "conectada", "detalle": "@picado80, cuenta profesional, por Buffer. Tres piezas por semana; las historias las sube Kenneth cuando quiera.", "orden": 2},
    "facebook": {"nombre": "Facebook", "tipo": "red", "estado": "falta", "detalle": "Cabe en el tercer lugar gratis de Buffer. Recibe las mismas 3 piezas de Instagram, sin trabajo extra.", "orden": 3},
    "x": {"nombre": "X", "tipo": "red", "estado": "despues", "detalle": "Sin plan todavía. En Buffer cuesta $6 al mes.", "orden": 4},
    "linkedin": {"nombre": "LinkedIn", "tipo": "red", "estado": "despues", "detalle": "Sin publicar por ahora: Kenneth decidió el 12-oct que no es la red para el resultado que busca.", "orden": 5},
    "youtube": {"nombre": "YouTube", "tipo": "red", "estado": "despues", "detalle": "Kenneth crea el canal cuando pueda.", "orden": 6},
    "buffer": {"enlace": "https://publish.buffer.com", "nombre": "Buffer", "tipo": "herramienta", "estado": "conectada", "detalle": "Plan gratis: 2 de 3 redes usadas. Cada red extra cuesta $6 al mes.", "orden": 10},
    "heygen": {"enlace": "https://app.heygen.com", "nombre": "HeyGen", "tipo": "herramienta", "estado": "conectada", "detalle": "El gemelo «Kenneth GP». Por API, $0.0805 por segundo.", "orden": 11},
    "elevenlabs": {"nombre": "ElevenLabs", "tipo": "herramienta", "estado": "conectada", "detalle": "Tu voz clonada, los tiempos de cada palabra y los efectos.", "orden": 12},
    "higgsfield": {"nombre": "Higgsfield", "tipo": "herramienta", "estado": "conectada", "detalle": "La prueba de gancho (gratis) y tomas realistas.", "orden": 13},
    "hyperframes": {"nombre": "HyperFrames", "tipo": "herramienta", "estado": "conectada", "detalle": "Gráficos, subtítulos y montaje, en tu PC. $0.", "orden": 14},
    "pixabay": {"enlace": "https://pixabay.com/api/docs/", "nombre": "Pixabay", "tipo": "herramienta", "estado": "falta", "detalle": "Video de banco gratis. Falta la llave.", "orden": 15},
    "openai": {"enlace": "https://platform.openai.com/settings/organization/general", "nombre": "OpenAI (SEMI)", "tipo": "herramienta", "estado": "despues", "detalle": "Anuncios y directorio de plugins, para SEMI. Falta verificar la organización.", "orden": 16},
}

SALDOS = {
    "heygen": {"nombre": "HeyGen", "valor": "$2.88", "detalle": "Alcanza para 1 video. Cada video usa unos $1.83.", "alerta": True, "orden": 1},
    "elevenlabs": {"nombre": "ElevenLabs", "valor": "169 de 186.000", "detalle": "Caracteres del mes. Plan fijo de $22.", "alerta": False, "orden": 2},
    "higgsfield": {"nombre": "Higgsfield", "valor": "200 créditos", "detalle": "La prueba de gancho no gasta créditos.", "alerta": False, "orden": 3},
    "claude": {"nombre": "Claude", "valor": "23 % de la semana", "detalle": "Plan Max, sin cobros extra.", "alerta": False, "orden": 4},
}

NOTAS = {
    "redes": "TikTok lleva todo: dos piezas por día. Instagram lleva tres por semana. Facebook cabe gratis en el tercer lugar de Buffer y recibe lo mismo que Instagram. X y LinkedIn quedan sin publicar. Conectar una red lo hace Kenneth, porque pide iniciar sesión.",
}

# La vara sale de @picado80 al 9-oct-2026 (ARRANQUE.md y CALENDARIO.md).
OBJETIVOS = {
    "norte": {
        "titulo": "Conversaciones con empresas", "que": "Alguien que dirige o decide en un negocio le escribe a Kenneth por algo que vio.",
        "meta": 1, "meta_texto": "1 al mes ya es avance", "actual": 0, "periodo": "octubre",
    },
    "items": {
        "alcance": {"nombre": "Alcance", "busca": "Que lo vea gente que no lo conoce.", "mide": "Vistas a los 7 días", "vara": "Pasa de 326", "excelente": "650", "cuenta": ["Alcance"], "orden": 1},
        "guardado": {"nombre": "Guardado", "busca": "Que sea tan útil que lo guarden.", "mide": "Guardados", "vara": "Al menos 1 (hoy son 0)", "excelente": "10 por cada 1.000 vistas", "cuenta": ["Guardado"], "orden": 2},
        "compartido": {"nombre": "Compartido", "busca": "Que el empleado se lo mande al jefe.", "mide": "Compartidos", "vara": "Al menos 1 (hoy son 0)", "excelente": "10 por cada 1.000 vistas", "cuenta": ["Compartido"], "orden": 3},
        "comentario": {"nombre": "Comentario", "busca": "Que la gente cuente su caso.", "mide": "Comentarios de gente que no es conocida", "vara": "Al menos 2", "excelente": "10 por cada 1.000 vistas", "cuenta": ["Comentario"], "orden": 4},
        "perfil": {"nombre": "Perfil", "busca": "Que quieran saber quién es.", "mide": "Visitas al perfil y seguidores nuevos", "vara": "Más que el video anterior con el mismo objetivo", "excelente": "", "cuenta": ["Perfil", "Perfil y empresa"], "orden": 5},
        "empresa": {"nombre": "Empresa", "busca": "La que manda: que una empresa le escriba.", "mide": "Mensajes de alguien que dirige o decide", "vara": "1 conversación al mes", "excelente": "", "cuenta": ["Perfil y empresa"], "orden": 6},
    },
    "ritmo": {
        "tiktok": {"nombre": "TikTok", "texto": "2 por día: un gráfico y un video con Kenneth.", "orden": 1},
        "instagram": {"nombre": "Instagram", "texto": "3 por semana, las más útiles para guardar o mandar. Historias cuando Kenneth quiera.", "orden": 2},
        "facebook": {"nombre": "Facebook", "texto": "Lo mismo que Instagram, cuando se conecte.", "orden": 3},
        "linkedin": {"nombre": "LinkedIn y X", "texto": "Sin publicar por ahora.", "orden": 4},
    },
    "base": {
        "fecha": "9 de octubre",
        "datos": [
            {"etiqueta": "TikTok: vistas de un video normal", "valor": "326"},
            {"etiqueta": "TikTok: comentarios por cada 1.000 vistas", "valor": "2"},
            {"etiqueta": "TikTok: compartidos y guardados", "valor": "0"},
            {"etiqueta": "TikTok: videos en la cuenta", "valor": "238"},
            {"etiqueta": "Instagram: seguidores", "valor": "576"},
        ],
    },
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    DATOS.mkdir(exist_ok=True)
    items = {}
    for n, (fecha, linea, cod, serie, titulo, porque, objetivo, ig) in enumerate(PIEZAS):
        items[f"p-{fecha}-{cod}"] = {
            "fecha": fecha, "linea": linea, "tipo": "pieza", "codigo": cod, "serie": SERIES[serie], "titulo": titulo, "porque": porque,
            "objetivo": objetivo, "vara": VARAS[objetivo], "redes": ["tiktok", "instagram"] if ig else ["tiktok"],
            "estado": "por-hacer", "quien": "Claude", "costo": COSTO_B if linea == "B" else 0, "orden": n,
        }
    items["p-2026-10-13-002"]["estado"] = "guion-grafico"
    for n, (fecha, titulo, porque, quien) in enumerate(ACCIONES):
        items[f"m-{fecha}-{n}"] = {"fecha": fecha, "linea": "M", "tipo": "accion", "codigo": "", "serie": "Marca", "titulo": titulo,
                                   "porque": porque, "objetivo": "", "vara": "", "estado": "pendiente", "quien": quien, "costo": 0, "orden": 100 + n}
    tareas = {i: {"titulo": t, "detalle": d, "quien": q, "para": p, "hecho": h, "orden": n} for n, (i, t, d, q, p, h) in enumerate(TAREAS)}

    b_oct = sum(1 for p in PIEZAS if p[1] == "B" and p[0] < "2026-11-01")
    gastado = 30.12
    presupuesto = {
        "tope": 100, "gastado": gastado, "proyectado": round(gastado + b_oct * COSTO_B, 2),
        "detalle": "Octubre: $22 de ElevenLabs y $8.12 de HeyGen ($5.75 en pruebas y $2.37 en el primer video).",
        "por_video": COSTO_B, "meta_por_video": 2.0,
    }
    docs = {
        "calendario": {"items": items},
        "tareas": {"items": tareas},
        "guiones": {"items": GUIONES},
        "estado": {"actualizado": ACTUALIZADO, "conexiones": CONEXIONES, "saldos": SALDOS, "presupuesto": presupuesto, "notas": NOTAS},
        "objetivos": OBJETIVOS,
    }
    for nombre, cuerpo in docs.items():
        (DATOS / f"{nombre}.json").write_text(json.dumps(cuerpo, ensure_ascii=False, indent=1), encoding="utf-8")
        print(nombre, len(json.dumps(cuerpo)), "bytes")

    a = [p for p in PIEZAS if p[1] == "A"]
    b = [p for p in PIEZAS if p[1] == "B"]
    por_dia = {}
    for p in PIEZAS:
        por_dia.setdefault(p[0], []).append(p[1])
    assert all(sorted(v) == ["A", "B"] for v in por_dia.values()), "cada día lleva un gráfico y un video"
    assert len({p[2] for p in PIEZAS}) == len(PIEZAS), "códigos repetidos"
    print(f"{len(PIEZAS)} piezas en {len(por_dia)} días: {len(a)} gráficos, {len(b)} con Kenneth, {sum(1 for p in PIEZAS if p[7])} a Instagram")
    print(f"costo de las 4 semanas: ${len(b) * COSTO_B + 22:.2f} · octubre proyectado: ${presupuesto['proyectado']}")


if __name__ == "__main__":
    main()
