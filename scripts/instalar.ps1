$ErrorActionPreference = "Stop"
Write-Host "=== Instalacion Caso 3: Jenkins + Docker ===" -ForegroundColor Cyan

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker no esta instalado o no esta disponible en PowerShell."
}

docker info | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Desktop no esta iniciado. Abre Docker Desktop e intenta de nuevo."
}

$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz
Write-Host "Construyendo e iniciando Jenkins y servidor de pruebas..." -ForegroundColor Yellow
docker compose up --build -d
if ($LASTEXITCODE -ne 0) {
    throw "Fallo la construccion. Revisa: docker compose logs jenkins"
}

docker compose ps
Write-Host "Jenkins: http://localhost:8081" -ForegroundColor Green
Write-Host "Servidor de pruebas: http://localhost:5000/health" -ForegroundColor Green
Write-Host "El /health respondera 'Sin despliegue' hasta ejecutar el Pipeline." -ForegroundColor Yellow
Write-Host "Clave inicial: docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
