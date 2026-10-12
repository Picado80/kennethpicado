// Lo que Kenneth marca en la consola (pendientes hechos, respuestas a los guiones gráficos, acciones nuevas).
// Vive en un Blob privado del proyecto de Vercel. La página lo suma a datos/*.json, que escribe Claude.
// El acceso lo cierra la protección de Vercel del proyecto: sin sesión de Vercel no se llega acá.
// Como la función no tiene llave propia, antes de responder comprueba que esa protección esté puesta.
import { get, put } from "@vercel/blob";

const RUTA = "consola/marcas.json";
const DOCS = new Set(["calendario", "tareas", "guiones"]);
const CLAVE = /^[A-Za-z0-9_.:-]{1,80}$/;
const VETADAS = new Set(["__proto__", "constructor", "prototype"]);

// El almacén se crea privado. Si alguien lo creó público, la primera llamada falla por el acceso y se reintenta así.
let acceso = "private";
async function conAcceso(tarea) {
  try {
    return await tarea(acceso);
  } catch (e) {
    if (acceso !== "private" || !/access/i.test(String(e && e.message))) throw e;
    acceso = "public";
    return tarea(acceso);
  }
}

// ¿Un visitante sin sesión puede abrir el sitio por esta misma dirección? Si puede, la función se niega a todo.
const revisado = new Map();
async function protegido(host) {
  if (!/^[a-z0-9.-]{1,200}$/i.test(host || "")) return false;
  const v = revisado.get(host);
  if (v && v.hasta > Date.now()) return v.ok;
  let ok = false;
  try {
    const r = await fetch("https://" + host + "/datos/estado.json", { redirect: "manual", cache: "no-store", signal: AbortSignal.timeout(4000) });
    ok = r.status === 401 || r.status === 403 || (r.status >= 300 && r.status < 400);
  } catch {
    ok = false;
  }
  revisado.set(host, { ok, hasta: Date.now() + 5 * 60 * 1000 });
  return ok;
}

// Un parche es un objeto de hasta 4 niveles con textos cortos, números y sí/no. Lo demás se rechaza.
function limpio(v, nivel) {
  if (v === null || typeof v === "boolean") return v;
  if (typeof v === "number") return Number.isFinite(v) ? v : undefined;
  if (typeof v === "string") return v.length <= 2000 ? v : undefined;
  if (typeof v !== "object" || Array.isArray(v) || nivel > 4) return undefined;
  const o = {};
  for (const [k, x] of Object.entries(v)) {
    if (!CLAVE.test(k) || VETADAS.has(k)) return undefined;
    const y = limpio(x, nivel + 1);
    if (y === undefined) return undefined;
    o[k] = y;
  }
  return o;
}

function fusion(a, b) {
  const o = a && typeof a === "object" && !Array.isArray(a) ? { ...a } : {};
  for (const [k, v] of Object.entries(b)) o[k] = v && typeof v === "object" ? fusion(o[k], v) : v;
  return o;
}

// Si el Blob no existe todavía, no hay marcas. Cualquier otro fallo se lanza: nunca se escribe sobre una lectura fallida.
async function leer() {
  const r = await conAcceso((a) => get(RUTA, { access: a, useCache: false }));
  if (!r) return {};
  if (r.statusCode !== 200 || !r.stream) throw new Error("lectura " + r.statusCode);
  const m = JSON.parse(await new Response(r.stream).text());
  return m && typeof m === "object" && !Array.isArray(m) ? m : {};
}

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  try {
    if (!(await protegido(req.headers.host))) return res.status(403).json({ error: "sin-proteccion" });
    if (req.method === "GET") return res.status(200).json(await leer());
    if (req.method !== "POST") {
      res.setHeader("Allow", "GET, POST");
      return res.status(405).json({ error: "metodo" });
    }
    const origen = req.headers.origin;
    if (origen && new URL(origen).host !== req.headers.host) return res.status(403).json({ error: "origen" });
    if (!String(req.headers["content-type"] || "").startsWith("application/json")) return res.status(415).json({ error: "tipo" });
    const cuerpo = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    const doc = cuerpo && cuerpo.doc;
    const parche = limpio(cuerpo && cuerpo.parche, 0);
    if (!DOCS.has(doc) || !parche || typeof parche !== "object" || JSON.stringify(parche).length > 16000) {
      return res.status(400).json({ error: "parche" });
    }
    const marcas = await leer();
    marcas[doc] = fusion(marcas[doc], parche);
    marcas.actualizado = new Date().toISOString();
    const texto = JSON.stringify(marcas);
    if (texto.length > 400000) return res.status(413).json({ error: "lleno" });
    await conAcceso((a) => put(RUTA, texto, { access: a, addRandomSuffix: false, allowOverwrite: true, contentType: "application/json" }));
    return res.status(200).json(marcas);
  } catch (e) {
    console.error("marcas:", e && e.message);
    return res.status(500).json({ error: "interno" });
  }
}
