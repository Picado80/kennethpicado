# Marca personal - verifica las llaves de HeyGen y ElevenLabs sin mostrarlas
#
# Lee SOLO dos llaves (HEYGEN_API_KEY y ELEVENLABS_MARCA_API_KEY) con el mismo
# buscador de TORRE: Get-ProveedorKey (torre/hooks/dispatch/proveedores.ps1,
# INDICE-CODIGO #15). No carga el .env entero al entorno.
# Solo hace lecturas: no genera video ni audio y no gasta creditos.
# De cada llave muestra el largo y los ultimos 4 caracteres, nada mas.
#
# Uso (desde la raiz de kennethpicado):
#   powershell -ExecutionPolicy Bypass -File marca\scripts\verificar-llaves.ps1
#   powershell -ExecutionPolicy Bypass -File marca\scripts\verificar-llaves.ps1 -TorreDir D:\otra\torre
#
# Sale con el numero de fallas (0 = todo verde).
#
# ASCII puro a proposito: PowerShell 5.1 lee .ps1 sin BOM como cp1252 y un
# acento o un guion largo rompe el archivo entero (ver nota en proveedores.ps1).
param(
  [string]$TorreDir = $(if ($env:TORRE_DIR) { $env:TORRE_DIR } else { Join-Path $env:USERPROFILE "torre" })
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# marca\scripts\verificar-llaves.ps1 -> marca\salidas (ignorada por git)
$salidas = Join-Path (Split-Path -Parent (Split-Path -Parent $PSCommandPath)) "salidas"

$proveedores = Join-Path $TorreDir "hooks\dispatch\proveedores.ps1"
if (-not (Test-Path $proveedores)) {
  Write-Host "No encuentro TORRE en $TorreDir. Pasale la ruta con -TorreDir C:\ruta\a\torre" -ForegroundColor Red
  exit 1
}
. $proveedores
New-Item -ItemType Directory -Force -Path $salidas | Out-Null

# Una llave nunca tiene espacios: si los tiene, quedo texto pegado despues en la linea del .env
function Test-Pegado([string]$Llave, [string]$Nombre) {
  if ($Llave -match "\s") {
    Write-Host "  aviso    : la llave tiene espacios. En torre\.env la linea $Nombre= debe terminar donde termina la llave" -ForegroundColor Yellow
    return $true
  }
  return $false
}

function Get-Cola([string]$Llave) {
  return $Llave.Substring([Math]::Max(0, $Llave.Length - 4))
}

# GET de solo lectura. Nunca lanza: devuelve Ok, Codigo, Datos y Detalle.
# El detalle se recorta y se le borra la llave por si un servidor la repitiera.
function Invoke-Lectura([string]$Uri, [hashtable]$Headers, [string]$Llave) {
  try {
    $r = Invoke-RestMethod -Method Get -Uri $Uri -Headers $Headers -TimeoutSec 30
    return @{ Ok = $true; Codigo = 200; Datos = $r; Detalle = "" }
  } catch {
    $codigo = 0
    if ($_.Exception.Response) { $codigo = [int]$_.Exception.Response.StatusCode }
    $detalle = ""
    if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $detalle = $_.ErrorDetails.Message }
    if (-not $detalle) { $detalle = $_.Exception.Message }
    if ($Llave) { $detalle = $detalle.Replace($Llave, "***") }
    # Si el servidor manda JSON con error/aviso (HeyGen avisa ahi que endpoint usar), se muestra completo
    try {
      $j = $detalle | ConvertFrom-Json
      $partes = @()
      if ($j.error.message) { $partes += "error: $($j.error.message)" }
      if ($j.warning.message) { $partes += "aviso: $($j.warning.message)" }
      if ($partes.Count -gt 0) {
        return @{ Ok = $false; Codigo = $codigo; Datos = $null; Detalle = ($partes -join " | ") }
      }
    } catch { }
    $detalle = ($detalle -replace "\s+", " ").Trim()
    if ($detalle.Length -gt 220) { $detalle = $detalle.Substring(0, 220) + "..." }
    return @{ Ok = $false; Codigo = $codigo; Datos = $null; Detalle = $detalle }
  }
}

function Write-Falla([string]$Que, [hashtable]$R) {
  $http = if ($R.Codigo) { "HTTP $($R.Codigo)" } else { "sin respuesta" }
  Write-Host ("  {0,-9}: FALLA ({1}) {2}" -f $Que, $http, $R.Detalle) -ForegroundColor Red
  if ($R.Detalle -match "Legacy") {
    Write-Host "             HeyGen dice que esta ruta es vieja: el aviso de arriba dice cual usar" -ForegroundColor Yellow
  } elseif ($R.Codigo -eq 401) {
    Write-Host "             401 = la llave no sirve: revisa que este completa, sin espacios ni comillas" -ForegroundColor Yellow
  }
}

$fallos = 0
Write-Host ""
Write-Host "TORRE: $TorreDir" -ForegroundColor DarkGray

# ---------------------------------------------------------------- HeyGen
Write-Host ""
Write-Host "== HeyGen (HEYGEN_API_KEY) ==" -ForegroundColor Cyan
$hg = Get-ProveedorKey -Proveedor @{ KeyFile = ".heygen_key"; KeyEnv = "HEYGEN_API_KEY" }
if (-not $hg) {
  Write-Host "  llave    : NO ENCONTRADA. Revisa que en torre\.env la linea empiece con HEYGEN_API_KEY=" -ForegroundColor Red
  $fallos++
} else {
  Write-Host "  llave    : encontrada (largo $($hg.Length), termina en ...$(Get-Cola $hg))" -ForegroundColor DarkGray
  if (Test-Pegado $hg "HEYGEN_API_KEY") { $fallos++ }
  # API v3 (la v2 se apaga el 2026-10-31). Va la llave en los dos headers que
  # usa HeyGen; el que sobre se ignora.
  $h = @{ "X-Api-Key" = $hg; "Authorization" = "Bearer $hg"; "Accept" = "application/json" }

  $q = Invoke-Lectura "https://api.heygen.com/v3/users/me" $h $hg
  if ($q.Ok) {
    $archivo = Join-Path $salidas "heygen-cuenta.json"
    $q.Datos | ConvertTo-Json -Depth 8 | Set-Content -Path $archivo -Encoding UTF8
    Write-Host "  cuenta   : OK (detalle en $archivo)" -ForegroundColor Green
  } else { Write-Falla "cuenta" $q; $fallos++ }

  $a = Invoke-Lectura "https://api.heygen.com/v3/avatars" $h $hg
  if ($a.Ok) {
    # La forma de la respuesta puede variar: se cuentan las listas que aparezcan
    $d = $a.Datos
    if ($d.data) { $d = $d.data }
    $lista = $null
    foreach ($campo in @("avatars", "items", "results")) { if ($d.$campo) { $lista = @($d.$campo); break } }
    if (-not $lista -and $d -is [array]) { $lista = @($d) }
    $cuantos = if ($lista) { "$($lista.Count) avatares" } else { "respuesta recibida" }
    $archivo = Join-Path $salidas "heygen-avatares.json"
    $a.Datos | ConvertTo-Json -Depth 8 | Set-Content -Path $archivo -Encoding UTF8
    Write-Host "  avatares : OK ($cuantos)" -ForegroundColor Green
    Write-Host "             lista completa en $archivo" -ForegroundColor DarkGray
  } else { Write-Falla "avatares" $a; $fallos++ }
}

# ---------------------------------------------------------------- ElevenLabs
Write-Host ""
Write-Host "== ElevenLabs (ELEVENLABS_MARCA_API_KEY) ==" -ForegroundColor Cyan
$el = Get-ProveedorKey -Proveedor @{ KeyFile = ".elevenlabs_marca_key"; KeyEnv = "ELEVENLABS_MARCA_API_KEY" }
if (-not $el) {
  Write-Host "  llave    : NO ENCONTRADA. Revisa que en torre\.env la linea empiece con ELEVENLABS_MARCA_API_KEY=" -ForegroundColor Red
  $fallos++
} else {
  Write-Host "  llave    : encontrada (largo $($el.Length), termina en ...$(Get-Cola $el))" -ForegroundColor DarkGray
  if (Test-Pegado $el "ELEVENLABS_MARCA_API_KEY") { $fallos++ }

  # La de la marca tiene que ser otra llave que la del producto Semi (ver marca/LLAVES.md).
  $semi = Get-ProveedorKey -Proveedor @{ KeyFile = ".elevenlabs_key"; KeyEnv = "ELEVENLABS_API_KEY" }
  if ($semi -and $semi -eq $el) {
    Write-Host "  aviso    : es la MISMA llave que ELEVENLABS_API_KEY (Semi). Crea una aparte para la marca." -ForegroundColor Yellow
    $fallos++
  } elseif ($semi) {
    Write-Host "  separada : OK (distinta de la llave de Semi)" -ForegroundColor Green
  }

  $h = @{ "xi-api-key" = $el; "Accept" = "application/json" }

  $s = Invoke-Lectura "https://api.elevenlabs.io/v1/user/subscription" $h $el
  if ($s.Ok) {
    $d = $s.Datos
    Write-Host "  plan     : OK ($($d.tier), $($d.character_count) de $($d.character_limit) caracteres usados)" -ForegroundColor Green
  } elseif ($s.Codigo -eq 401 -and $s.Detalle -match "missing_permissions") {
    # Una llave restringida puede no tener permiso de leer el usuario: no es falla.
    Write-Host "  plan     : la llave no tiene permiso para leer la cuenta (normal si la creaste restringida)" -ForegroundColor Yellow
  } else { Write-Falla "plan" $s; $fallos++ }

  $v = Invoke-Lectura "https://api.elevenlabs.io/v1/voices" $h $el
  if ($v.Ok) {
    $voces = @($v.Datos.voices | Where-Object { $_ })
    $propias = @($voces | Where-Object { $_.category -and $_.category -ne "premade" })
    $archivo = Join-Path $salidas "elevenlabs-voces.json"
    $v.Datos | ConvertTo-Json -Depth 8 | Set-Content -Path $archivo -Encoding UTF8
    Write-Host "  voces    : OK ($($voces.Count) en total, $($propias.Count) propias)" -ForegroundColor Green
    foreach ($p in $propias) {
      Write-Host ("             {0,-28} {1,-12} {2}" -f $p.name, $p.category, $p.voice_id) -ForegroundColor DarkGray
    }
    Write-Host "             lista completa en $archivo" -ForegroundColor DarkGray
  } elseif ($v.Codigo -eq 401 -and $v.Detalle -match "missing_permissions") {
    Write-Host "  voces    : FALLA, la llave no tiene permiso de voces. Dale 'Voices: read' en su configuracion" -ForegroundColor Red
    $fallos++
  } else { Write-Falla "voces" $v; $fallos++ }
}

Write-Host ""
if ($fallos -eq 0) {
  Write-Host "Todo verde. Siguiente paso: crear el clon de voz y el gemelo (marca/LLAVES.md)." -ForegroundColor Green
} else {
  Write-Host "$fallos punto(s) para revisar. Ninguna llave se mostro en pantalla." -ForegroundColor Red
}
exit $fallos
