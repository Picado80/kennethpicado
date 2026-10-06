# Marca personal - prueba la voz clonada de Kenneth con una frase del guion 001
#
# Busca la llave ELEVENLABS_MARCA_API_KEY con Get-ProveedorKey de TORRE (igual que
# verificar-llaves.ps1), elige la voz clonada (o la de config/estudio.json, o la que
# pases con -VozId), genera un mp3 corto en marca\salidas\ y lo abre.
# Gasta unos 150 caracteres del plan.
#
# Uso (desde la raiz de kennethpicado):
#   powershell -ExecutionPolicy Bypass -File marca\scripts\probar-voz.ps1
#   powershell -ExecutionPolicy Bypass -File marca\scripts\probar-voz.ps1 -VozId abc123
#   powershell -ExecutionPolicy Bypass -File marca\scripts\probar-voz.ps1 -Modelo eleven_multilingual_v2
#
# ASCII puro a proposito (ver verificar-llaves.ps1): los acentos del texto van como \uXXXX.
param(
  [string]$VozId = "",
  [string]$Modelo = "eleven_v4",
  [string]$TorreDir = $(if ($env:TORRE_DIR) { $env:TORRE_DIR } else { Join-Path $env:USERPROFILE "torre" })
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$marca = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$salidas = Join-Path $marca "salidas"
$estudio = Join-Path $marca "config\estudio.json"

$proveedores = Join-Path $TorreDir "hooks\dispatch\proveedores.ps1"
if (-not (Test-Path $proveedores)) {
  Write-Host "No encuentro TORRE en $TorreDir. Pasale la ruta con -TorreDir C:\ruta\a\torre" -ForegroundColor Red
  exit 1
}
. $proveedores
New-Item -ItemType Directory -Force -Path $salidas | Out-Null

$llave = Get-ProveedorKey -Proveedor @{ KeyFile = ".elevenlabs_marca_key"; KeyEnv = "ELEVENLABS_MARCA_API_KEY" }
if (-not $llave) {
  Write-Host "No encuentro ELEVENLABS_MARCA_API_KEY en torre\.env" -ForegroundColor Red
  exit 1
}
$h = @{ "xi-api-key" = $llave }

# 1. Que voz: -VozId, si no la de estudio.json, si no la clonada de la cuenta
if (-not $VozId -and (Test-Path $estudio)) {
  $cfg = Get-Content $estudio -Raw | ConvertFrom-Json
  if ($cfg.elevenlabs.voz_kenneth) { $VozId = $cfg.elevenlabs.voz_kenneth }
}
if (-not $VozId) {
  $voces = @((Invoke-RestMethod -Method Get -Uri "https://api.elevenlabs.io/v1/voices" -Headers $h -TimeoutSec 30).voices)
  $clones = @($voces | Where-Object { $_.category -eq "cloned" })
  if ($clones.Count -eq 0) {
    Write-Host "Todavia no hay ninguna voz clonada en la cuenta. Si se esta creando, espera unos minutos y volve a correr." -ForegroundColor Yellow
    exit 1
  }
  foreach ($c in $clones) { Write-Host ("  clon: {0,-30} {1}" -f $c.name, $c.voice_id) -ForegroundColor DarkGray }
  $VozId = $clones[0].voice_id
  if ($clones.Count -gt 1) { Write-Host "  hay varios clones: uso el primero. Para otro, -VozId <id>" -ForegroundColor Yellow }
}
Write-Host "  voz      : $VozId" -ForegroundColor DarkGray

# 2. Generar el audio (frase del gancho del guion 001)
$cuerpo = '{"text":"Uno de mis empleados se calific\u00f3 su propio examen. Y no hizo nada malo. Tengo una oficina donde los empleados son inteligencias artificiales.","model_id":"' + $Modelo + '"}'
$archivo = Join-Path $salidas ("prueba-voz-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".mp3")
try {
  Invoke-RestMethod -Method Post -Uri "https://api.elevenlabs.io/v1/text-to-speech/$($VozId)?output_format=mp3_44100_128" `
    -Headers $h -ContentType "application/json" -Body ([Text.Encoding]::UTF8.GetBytes($cuerpo)) `
    -OutFile $archivo -TimeoutSec 120
} catch {
  $detalle = ""
  if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $detalle = $_.ErrorDetails.Message } else { $detalle = $_.Exception.Message }
  Write-Host "  FALLA: $($detalle.Replace($llave, '***'))" -ForegroundColor Red
  exit 1
}

$tam = (Get-Item $archivo).Length
if ($tam -lt 2000) {
  Write-Host "  FALLA: el audio salio vacio ($tam bytes)" -ForegroundColor Red
  exit 1
}
Write-Host "  audio    : OK ($([Math]::Round($tam / 1024)) KB) -> $archivo" -ForegroundColor Green
Write-Host "  Escuchalo: si suena a vos, pasame el ID de la voz para guardarlo en config\estudio.json." -ForegroundColor Green
Start-Process $archivo
