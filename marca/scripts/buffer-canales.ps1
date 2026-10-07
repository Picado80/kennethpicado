# Marca personal - lista los canales conectados en Buffer sin mostrar la llave
#
# Lee SOLO BUFFER_API_KEY con el mismo buscador de TORRE: Get-ProveedorKey
# (torre/hooks/dispatch/proveedores.ps1, INDICE-CODIGO #15). No carga el .env
# entero al entorno. Solo lectura: no programa ni publica nada.
#
# API (developers.buffer.com, guides/getting-started y reference#query-channels):
#   POST https://api.buffer.com  (GraphQL)  Authorization: Bearer <llave>
#   OJO: publish.buffer.com/graphql NO es la API; ahi el 400 del 7-oct.
# Gasta 1 llamada + 1 por organizacion (plan Free: 250 por dia, 3.000 por mes).
#
# Uso (desde la raiz de kennethpicado):
#   powershell -ExecutionPolicy Bypass -File marca\scripts\buffer-canales.ps1
#   powershell -ExecutionPolicy Bypass -File marca\scripts\buffer-canales.ps1 -TorreDir D:\otra\torre
#
# Guarda la respuesta en marca\salidas\buffer-canales.json (ignorada por git).
# Sale con el numero de fallas (0 = Instagram, YouTube y LinkedIn conectados).
#
# ASCII puro a proposito: PowerShell 5.1 lee .ps1 sin BOM como cp1252 y un
# acento o un guion largo rompe el archivo entero (ver nota en proveedores.ps1).
param(
  [string]$TorreDir = $(if ($env:TORRE_DIR) { $env:TORRE_DIR } else { Join-Path $env:USERPROFILE "torre" })
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Api = "https://api.buffer.com"
# Los 3 canales del plan Free que decidio Kenneth (CICLO.md, LLAVES.md)
$Esperados = @("instagram", "youtube", "linkedin")

# marca\scripts\buffer-canales.ps1 -> marca\salidas (ignorada por git)
$salidas = Join-Path (Split-Path -Parent (Split-Path -Parent $PSCommandPath)) "salidas"

$proveedores = Join-Path $TorreDir "hooks\dispatch\proveedores.ps1"
if (-not (Test-Path $proveedores)) {
  Write-Host "No encuentro TORRE en $TorreDir. Pasale la ruta con -TorreDir C:\ruta\a\torre" -ForegroundColor Red
  exit 1
}
. $proveedores
New-Item -ItemType Directory -Force -Path $salidas | Out-Null

Write-Host ""
Write-Host "TORRE: $TorreDir" -ForegroundColor DarkGray
Write-Host ""
Write-Host "== Buffer (BUFFER_API_KEY) ==" -ForegroundColor Cyan

$llave = Get-ProveedorKey -Proveedor @{ KeyFile = ".buffer_key"; KeyEnv = "BUFFER_API_KEY" }
if (-not $llave) {
  Write-Host "  llave    : NO ENCONTRADA. Revisa que en torre\.env la linea empiece con BUFFER_API_KEY=" -ForegroundColor Red
  exit 1
}
$cola = $llave.Substring([Math]::Max(0, $llave.Length - 4))
Write-Host "  llave    : encontrada (largo $($llave.Length), termina en ...$cola)" -ForegroundColor DarkGray
# Una llave nunca tiene espacios: si los tiene, quedo texto pegado despues en la linea del .env
if ($llave -match "\s") {
  Write-Host "  aviso    : la llave tiene espacios. En torre\.env la linea BUFFER_API_KEY= debe terminar donde termina la llave" -ForegroundColor Yellow
  exit 1
}

$h = @{ "Authorization" = "Bearer $llave" }

# POST GraphQL de solo lectura. Nunca lanza: devuelve Ok, Codigo, Datos y Detalle.
# GraphQL contesta 200 aunque la consulta falle: el error viene en .errors.
# El cuerpo se lee como UTF-8 a mano (5.1 lo decodifica mal si falta el charset).
# Al detalle se le borra la llave por si el servidor la repitiera.
function Invoke-Buffer([string]$Consulta) {
  $cuerpo = [Text.Encoding]::UTF8.GetBytes((@{ query = $Consulta } | ConvertTo-Json -Compress))
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Method Post -Uri $Api -Headers $h `
      -ContentType "application/json; charset=utf-8" -Body $cuerpo -TimeoutSec 30
    $r = [Text.Encoding]::UTF8.GetString($resp.RawContentStream.ToArray()) | ConvertFrom-Json
    if ($r.errors) {
      $detalle = (@($r.errors) | ForEach-Object { $_.message }) -join " | "
      return @{ Ok = $false; Codigo = 200; Datos = $null; Detalle = $detalle.Replace($llave, "***") }
    }
    return @{ Ok = $true; Codigo = 200; Datos = $r.data; Detalle = "" }
  } catch {
    $codigo = 0
    if ($_.Exception.Response) { $codigo = [int]$_.Exception.Response.StatusCode }
    $detalle = ""
    if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $detalle = $_.ErrorDetails.Message }
    if (-not $detalle) { $detalle = $_.Exception.Message }
    $detalle = ($detalle.Replace($llave, "***") -replace "\s+", " ").Trim()
    if ($detalle.Length -gt 300) { $detalle = $detalle.Substring(0, 300) + "..." }
    return @{ Ok = $false; Codigo = $codigo; Datos = $null; Detalle = $detalle }
  }
}

function Write-Falla([string]$Que, [hashtable]$R) {
  $http = if ($R.Codigo) { "HTTP $($R.Codigo)" } else { "sin respuesta" }
  Write-Host ("  {0,-9}: FALLA ({1}) {2}" -f $Que, $http, $R.Detalle) -ForegroundColor Red
  if ($R.Codigo -eq 401) {
    Write-Host "             401 = la llave no sirve: revisa que este completa, sin espacios ni comillas" -ForegroundColor Yellow
  }
}

# 1. Organizaciones de la cuenta (la llave es de cuenta: ve todas)
$o = Invoke-Buffer "query { account { organizations { id } } }"
if (-not $o.Ok) { Write-Falla "cuenta" $o; exit 1 }
$orgs = @($o.Datos.account.organizations | Where-Object { $_ })
Write-Host "  cuenta   : OK ($($orgs.Count) organizacion(es))" -ForegroundColor Green
if ($orgs.Count -eq 0) {
  Write-Host "             la cuenta no tiene organizaciones: entra una vez a publish.buffer.com" -ForegroundColor Yellow
  exit 1
}

# 2. Canales de cada organizacion
$fallos = 0
$todos = @()
foreach ($org in $orgs) {
  $c = Invoke-Buffer ("query { channels(input: { organizationId: ""{0}"" }) { id name displayName service descriptor isDisconnected isLocked } }" -f $org.id)
  if (-not $c.Ok) { Write-Falla "canales" $c; $fallos++; continue }
  foreach ($canal in @($c.Datos.channels | Where-Object { $_ })) {
    $canal | Add-Member -NotePropertyName organizationId -NotePropertyValue $org.id -Force
    $todos += $canal
  }
}

$archivo = Join-Path $salidas "buffer-canales.json"
ConvertTo-Json -InputObject @{ organizaciones = $orgs; canales = $todos } -Depth 6 |
  Set-Content -Path $archivo -Encoding UTF8

Write-Host "  canales  : $($todos.Count) conectado(s)" -ForegroundColor $(if ($todos.Count) { "Green" } else { "Yellow" })
foreach ($canal in $todos) {
  $nombre = if ($canal.displayName) { $canal.displayName } else { $canal.name }
  $estado = "ok"
  if ($canal.isDisconnected) { $estado = "DESCONECTADO" } elseif ($canal.isLocked) { $estado = "BLOQUEADO" }
  Write-Host ("             {0,-12} {1,-28} {2,-14} {3}" -f $canal.service, $nombre, $estado, $canal.descriptor) -ForegroundColor DarkGray
  if ($estado -ne "ok") { $fallos++ }
}

foreach ($red in $Esperados) {
  if (-not @($todos | Where-Object { "$($_.service)" -match $red }).Count) {
    Write-Host "  falta    : $red no esta conectado en Buffer" -ForegroundColor Yellow
    $fallos++
  }
}
Write-Host "             detalle en $archivo" -ForegroundColor DarkGray

Write-Host ""
if ($fallos -eq 0) {
  Write-Host "Todo verde: Instagram, YouTube y LinkedIn listos para E003. La llave no se mostro." -ForegroundColor Green
} else {
  Write-Host "$fallos punto(s) para revisar. La llave no se mostro en pantalla." -ForegroundColor Red
}
exit $fallos
