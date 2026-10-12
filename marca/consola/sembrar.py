"""Genera las semillas de la consola de marca en marca/consola/datos/*.json.

Uso (desde la raíz de kennethpicado):
    python marca/consola/sembrar.py

No llama a ninguna API. Los saldos y las conexiones se pasan a mano arriba, con la fecha en que se midieron.
"""
import json
import sys
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "datos"
ACTUALIZADO = "2026-10-12T16:00:00-06:00"

VARAS = {
    "Alcance": "pasa de 326 vistas",
    "Guardado": "al menos 1 guardado",
    "Compartido": "al menos 1 compartido",
    "Comentario": "al menos 2 comentarios de gente nueva",
    "Perfil": "más visitas al perfil que el video anterior",
    "Perfil y empresa": "más visitas al perfil, o un mensaje de una empresa",
}

# fecha, linea, codigo, serie, titulo, porque, objetivo
PIEZAS = [
    ("2026-10-13", "B", "002", "Amazon en la soda", "Si tu negocio no sobrevive a tus vacaciones", "El primer video de la marca entra por lo que ya le funcionó a la cuenta: Amazon y Costa Rica.", "Guardado"),
    ("2026-10-14", "A", "J1", "IA sin jerga", "«Prompt» son las instrucciones que le di", "Tema amplio, para que TikTok empiece a mostrar la cuenta a gente interesada en IA.", "Alcance"),
    ("2026-10-15", "B", "004", "Amazon en la soda", "Un anfiteatro para 800 personas al 25 %", "El caso real más fuerte: prueba que el método funciona.", "Compartido"),
    ("2026-10-16", "A", "R1", "La regla", "El que hace el trabajo no lo revisa", "Una regla que se entiende sola y sirve en cualquier negocio.", "Guardado"),
    ("2026-10-18", "A", "N1", "El número", "165 personas, 4 países", "Dice quién es Kenneth sin presumir.", "Perfil"),
    ("2026-10-19", "A", "J2", "IA sin jerga", "Un «agente» es un empleado de IA", "Prepara el terreno para La Oficina.", "Alcance"),
    ("2026-10-20", "B", "001", "La Oficina", "Mi empleado se calificó su propio examen", "Presenta la serie insignia con el incidente más claro.", "Comentario"),
    ("2026-10-21", "A", "C1", "Las cinco capas", "1 de 5: lo que se escribe", "Abre una miniserie: quien ve una capa busca las otras.", "Guardado"),
    ("2026-10-22", "B", "003", "La Oficina", "Le prohibí trabajar a mi mejor empleado", "El gancho con más puntaje del banco (20 de 20).", "Compartido"),
    ("2026-10-23", "A", "L1", "La lista", "La reunión de los lunes en 15 minutos", "Algo que se puede hacer el lunes siguiente.", "Guardado"),
    ("2026-10-24", "B", "005", "La Oficina", "La oficina me avisó tres veces", "Kenneth se equivoca en público: da confianza.", "Comentario"),
    ("2026-10-25", "A", "N2", "El número", "800 personas de capacidad, 25 % de uso", "Refuerza el caso del anfiteatro.", "Perfil"),
    ("2026-10-25", "A", "J3", "IA sin jerga", "Un «modelo» es una IA", "Mantiene el alcance el fin de semana.", "Alcance"),
    ("2026-10-26", "A", "C2", "Las cinco capas", "2 de 5: lo que se cuenta todos los días", "Sigue la miniserie.", "Guardado"),
    ("2026-10-26", "B", "O6", "La Oficina", "Cuando el gerente se queda sin horas, ¿quién manda?", "Todo dueño se pregunta quién manda si él falta.", "Comentario"),
    ("2026-10-27", "A", "J4", "IA sin jerga", "Un «workflow» es la cadena de pasos", "Una palabra que el dueño oye y no entiende.", "Alcance"),
    ("2026-10-27", "B", "S2", "Sistema de la semana", "Las notas de voz de WhatsApp convertidas en pasos", "Primera prueba en pantalla: un problema que todos tienen.", "Perfil y empresa"),
    ("2026-10-28", "A", "R5", "La regla", "Nada se hace dos veces", "Ahorro que cualquier negocio entiende.", "Guardado"),
    ("2026-10-29", "A", "C3", "Las cinco capas", "3 de 5: lo que se revisa cada semana", "Sigue la miniserie.", "Guardado"),
    ("2026-10-29", "B", "A3", "Amazon en la soda", "La reunión de los lunes", "El gráfico del viernes 23, ahora con Kenneth.", "Guardado"),
    ("2026-10-30", "A", "L2", "La lista", "Las 3 cosas que solo vos sabés", "Sale del 002.", "Guardado"),
    ("2026-10-30", "B", "RC1", "Respuesta a un comentario", "El mejor comentario de la semana", "La audiencia empieza a dictar los temas.", "Comentario"),
    ("2026-10-31", "B", "O7", "La Oficina", "Contraté a un practicante gratis", "Tono liviano para el sábado.", "Compartido"),
    ("2026-11-01", "A", "N4", "El número", "12 semanas, sin contratar a un gerente", "Cierra el caso del anfiteatro.", "Perfil"),
    ("2026-11-02", "A", "C4", "Las cinco capas", "4 de 5: lo que ve el que dirige", "Sigue la miniserie.", "Guardado"),
    ("2026-11-02", "B", "A4", "Amazon en la soda", "Escribí el titular del día en que ya lo lograste", "Un método de Amazon que cualquiera puede usar.", "Guardado"),
    ("2026-11-03", "A", "J5", "IA sin jerga", "Los «tokens» son horas de trabajo", "Explica el costo de la IA sin tecnicismos.", "Alcance"),
    ("2026-11-03", "B", "S1", "Sistema de la semana", "La factura te dice a quién comprarle más barato", "Un sistema que le ahorra plata al dueño.", "Perfil y empresa"),
    ("2026-11-04", "A", "R6", "La regla", "Lo que no se escribe no pasó", "La regla de la bitácora.", "Guardado"),
    ("2026-11-04", "B", "RC2", "Respuesta a un comentario", "El mejor comentario de la semana", "Sigue la conversación con la audiencia.", "Comentario"),
    ("2026-11-05", "A", "C5", "Las cinco capas", "5 de 5: lo que se decide los lunes", "Cierra la miniserie.", "Guardado"),
    ("2026-11-05", "B", "O4", "La Oficina", "Mis empleados llevan bitácora", "Muestra la oficina de IAs por dentro.", "Compartido"),
    ("2026-11-06", "A", "L3", "La lista", "Apertura y cierre del local", "Una lista que se usa todos los días.", "Guardado"),
    ("2026-11-06", "B", "S3", "Sistema de la semana", "La cámara mágica", "Un sistema hecho para un evento real.", "Perfil y empresa"),
    ("2026-11-07", "A", "J6", "IA sin jerga", "El «handoff» es la nota de relevo", "Cierra la primera tanda del glosario.", "Alcance"),
    ("2026-11-07", "B", "O8", "La Oficina", "Nada se hace dos veces", "La regla del miércoles 28, contada como historia.", "Comentario"),
    ("2026-11-08", "A", "R7", "La regla", "La tabla decide quién trabaja, no el capricho", "Cómo se reparte el trabajo sin favoritismos.", "Guardado"),
    ("2026-11-08", "B", "TOP", "El más visto del mes", "El gráfico más visto, ahora con Kenneth", "El gemelo solo se paga en temas que ya pegaron.", "Alcance"),
]

# fecha, titulo, porque, quien
ACCIONES = [
    ("2026-10-12", "Aprobar el calendario y los guiones gráficos de la semana 1", "Sin el visto bueno no se produce nada.", "Kenneth"),
    ("2026-10-12", "Recargar HeyGen", "Quedan $2.88: alcanza para un video. El mes necesita unos $31.", "Kenneth"),
    ("2026-10-17", "Video personal, como los de siempre", "La cuenta sigue siendo de una persona (regla del arranque).", "Kenneth"),
    ("2026-10-17", "Grabar 3 o 4 tomas más para el gemelo, sin audífono", "Para que los videos puedan cortar entre encuadres.", "Kenneth"),
    ("2026-10-19", "Revisión de la semana 1", "Cada pieza contra su objetivo. Se decide si se sube a 8 piezas.", "Kenneth y Claude"),
    ("2026-10-26", "Revisión de la semana 2", "Cada pieza contra su objetivo. Se decide si se sube a 11 piezas.", "Kenneth y Claude"),
    ("2026-11-02", "Revisión de la semana 3", "Cada pieza contra su objetivo. Se decide si se sube a dos diarias.", "Kenneth y Claude"),
    ("2026-11-09", "Revisión del mes", "Qué series se quedan, cuáles cambian de gancho y cuánto costó.", "Kenneth y Claude"),
    ("2026-11-09", "SEMI: las 8 preguntas en ChatGPT", "Medición mensual de si ChatGPT ya menciona a SEMI.", "Kenneth"),
]

# id, titulo, detalle, quien, para
TAREAS = [
    ("k-calendario", "Aprobar el calendario", "O pedir las dos piezas diarias desde la primera semana.", "Kenneth", "2026-10-12"),
    ("k-002", "Aprobar el 002 con el inicio nuevo", "Abre con «En Amazon nadie era indispensable. Ni el jefe.» (fue el inicio con mejor puntaje).", "Kenneth", "2026-10-13"),
    ("k-heygen", "Recargar HeyGen", "Quedan $2.88. Para el mes son unos $31.", "Kenneth", "2026-10-12"),
    ("k-pixabay", "Sacar la llave gratis de Pixabay", "En pixabay.com/api/docs. Pegarla en torre\\.env como PIXABAY_API_KEY=", "Kenneth", "2026-10-14"),
    ("k-redes", "Decidir cómo conectar Facebook, X y LinkedIn", "Buffer gratis deja 3 redes y ya hay 2. Opciones en la sección Conexiones.", "Kenneth", "2026-10-14"),
    ("k-tomas", "Grabar 3 o 4 tomas más para el gemelo", "2 minutos cada una, sin audífono: cerca, sentado más lejos, de pie y con otro fondo.", "Kenneth", "2026-10-17"),
    ("k-personal", "Subir un video personal", "Como los de siempre: la cuenta sigue siendo tuya.", "Kenneth", "2026-10-17"),
    ("k-openai", "SEMI: verificar la organización en OpenAI", "En platform.openai.com. Tarda, conviene empezar ya.", "Kenneth", "2026-10-16"),
    ("c-002", "Rehacer el 002 con el inicio nuevo", "Guion gráfico primero; después el video.", "Claude", "2026-10-12"),
    ("c-semana1", "Guion gráfico de la semana 1", "Los tres gráficos juntos: J1, R1 y N1.", "Claude", "2026-10-13"),
    ("c-004", "Guion gráfico del 004", "El anfiteatro. Con foto fija de Kenneth, sin gastar.", "Claude", "2026-10-13"),
    ("c-plantillas", "Plantillas por serie", "Para que cada gráfico nuevo salga de datos y no se arme de cero.", "Claude", "2026-10-15"),
    ("c-buffer", "Programar las publicaciones en Buffer", "Con la aprobación de Kenneth antes de cada una (encargo E003).", "Claude", "2026-10-16"),
    ("c-medicion", "Anotar los números a las 48 horas y a los 7 días", "Cada pieza contra su objetivo, en el registro.", "Claude", "2026-10-15"),
]

GUIONES = {
    "002-v4": {
        "titulo": "002 · Si tu negocio no sobrevive a tus vacaciones", "version": "v4", "estado": "por-aprobar",
        "nota": "El video ya existe. Falta decidir si se rehace el inicio con «nadie era indispensable».",
        "comentario": "", "paginas": ["guiones/002-v4-1.png", "guiones/002-v4-2.png", "guiones/002-v4-3.png"], "orden": 1,
    },
}

CONEXIONES = {
    "instagram": {"nombre": "Instagram", "tipo": "red", "estado": "conectada", "detalle": "@picado80, cuenta profesional. Por Buffer.", "orden": 1},
    "tiktok": {"nombre": "TikTok", "tipo": "red", "estado": "conectada", "detalle": "@picado80. Por Buffer.", "orden": 2},
    "facebook": {"nombre": "Facebook", "tipo": "red", "estado": "falta", "detalle": "Dos caminos: el ajuste de Instagram que comparte los Reels en Facebook (gratis; hay que probar si toma lo que sale por Buffer) o un lugar en Buffer.", "orden": 3},
    "x": {"nombre": "X", "tipo": "red", "estado": "falta", "detalle": "Necesita un lugar en Buffer: el plan gratis deja 3 y ya hay 2.", "orden": 4},
    "linkedin": {"nombre": "LinkedIn", "tipo": "red", "estado": "falta", "detalle": "Necesita un lugar en Buffer. Es donde están las empresas.", "orden": 5},
    "youtube": {"nombre": "YouTube", "tipo": "red", "estado": "despues", "detalle": "Kenneth crea el canal cuando pueda.", "orden": 6},
    "buffer": {"enlace": "https://publish.buffer.com", "nombre": "Buffer", "tipo": "herramienta", "estado": "conectada", "detalle": "Plan gratis: 2 de 3 redes usadas. Con 5 redes: Essentials, $6 por red al mes.", "orden": 10},
    "heygen": {"enlace": "https://app.heygen.com", "nombre": "HeyGen", "tipo": "herramienta", "estado": "conectada", "detalle": "El gemelo «Kenneth GP». Por API, $0.0805 por segundo.", "orden": 11},
    "elevenlabs": {"nombre": "ElevenLabs", "tipo": "herramienta", "estado": "conectada", "detalle": "Tu voz clonada, los tiempos de cada palabra y los efectos.", "orden": 12},
    "higgsfield": {"nombre": "Higgsfield", "tipo": "herramienta", "estado": "conectada", "detalle": "La prueba de gancho (gratis) y tomas realistas.", "orden": 13},
    "hyperframes": {"nombre": "HyperFrames", "tipo": "herramienta", "estado": "conectada", "detalle": "Gráficos, subtítulos y montaje, en tu PC. $0.", "orden": 14},
    "pixabay": {"enlace": "https://pixabay.com/api/docs/", "nombre": "Pixabay", "tipo": "herramienta", "estado": "falta", "detalle": "Video de banco gratis. Falta la llave.", "orden": 15},
    "openai": {"enlace": "https://platform.openai.com/settings/organization/general", "nombre": "OpenAI (SEMI)", "tipo": "herramienta", "estado": "despues", "detalle": "Anuncios y directorio de plugins, para SEMI. Falta verificar la organización.", "orden": 16},
}

SALDOS = {
    "heygen": {"enlace": "https://app.heygen.com", "nombre": "HeyGen", "valor": "$2.88", "detalle": "Alcanza para 1 video. Cada video usa unos $1.83.", "alerta": True, "orden": 1},
    "elevenlabs": {"nombre": "ElevenLabs", "valor": "169 de 186.000", "detalle": "Caracteres del mes. Plan fijo de $22.", "alerta": False, "orden": 2},
    "higgsfield": {"nombre": "Higgsfield", "valor": "200 créditos", "detalle": "La prueba de gancho no gasta créditos.", "alerta": False, "orden": 3},
    "claude": {"nombre": "Claude", "valor": "23 % de la semana", "detalle": "Plan Max, sin cobros extra.", "alerta": False, "orden": 4},
}

NOTAS = {
    "redes": "Buffer gratis deja 3 redes y ya hay 2 (Instagram y TikTok). Recomendación: LinkedIn ocupa el tercer lugar, porque ahí están las empresas; Facebook se prueba gratis desde Instagram; X espera o cuesta $6 al mes. Conectar cada red lo hace Kenneth, porque pide iniciar sesión.",
}

PRESUPUESTO = {"tope": 100, "gastado": 30.12, "detalle": "Octubre: $22 de ElevenLabs, $8.12 de HeyGen ($5.75 en pruebas y $2.37 en el primer video).", "por_video": 1.83, "meta_por_video": 2.0}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    DATOS.mkdir(exist_ok=True)
    items = {}
    for n, (fecha, linea, cod, serie, titulo, porque, objetivo) in enumerate(PIEZAS):
        items[f"p-{fecha}-{cod}"] = {
            "fecha": fecha, "linea": linea, "tipo": "pieza", "codigo": cod, "serie": serie, "titulo": titulo, "porque": porque,
            "objetivo": objetivo, "vara": VARAS[objetivo], "estado": "por-hacer", "quien": "Claude", "costo": 1.83 if linea == "B" else 0, "orden": n,
        }
    items["p-2026-10-13-002"]["estado"] = "guion-grafico"
    for n, (fecha, titulo, porque, quien) in enumerate(ACCIONES):
        items[f"m-{fecha}-{n}"] = {"fecha": fecha, "linea": "M", "tipo": "accion", "codigo": "", "serie": "Marca", "titulo": titulo,
                                   "porque": porque, "objetivo": "", "vara": "", "estado": "pendiente", "quien": quien, "costo": 0, "orden": 100 + n}
    tareas = {i: {"titulo": t, "detalle": d, "quien": q, "para": p, "hecho": False, "orden": n} for n, (i, t, d, q, p) in enumerate(TAREAS)}
    docs = {
        "calendario": {"items": items},
        "tareas": {"items": tareas},
        "guiones": {"items": GUIONES},
        "estado": {"actualizado": ACTUALIZADO, "conexiones": CONEXIONES, "saldos": SALDOS, "presupuesto": PRESUPUESTO, "notas": NOTAS},
    }
    for nombre, cuerpo in docs.items():
        (DATOS / f"{nombre}.json").write_text(json.dumps(cuerpo, ensure_ascii=False, indent=1), encoding="utf-8")
        print(nombre, len(json.dumps(cuerpo)), "bytes")


if __name__ == "__main__":
    main()
