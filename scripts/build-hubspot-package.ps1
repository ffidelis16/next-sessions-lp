param()

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$indexPath = Join-Path $repoRoot 'index.html'
$packageRoot = Join-Path $repoRoot 'docs\hubspot-implementation'
$finalRoot = Join-Path $packageRoot 'entrega-final-plano-a'

$html = Get-Content -LiteralPath $indexPath -Raw -Encoding UTF8
$cssMatch = [regex]::Match($html, '(?s)<style>\s*(?<css>.*?)\s*</style>')
$bodyMatch = [regex]::Match($html, '(?s)<body>(?<body>.*?)<script charset="utf-8" type="text/javascript" src="//js\.hsforms\.net/forms/embed/v2\.js"></script>')
$jsMatch = [regex]::Match($html, '(?s)<script>\s*(?<js>/\* ===== 0\. TRACKING.*?)</script>\s*</body>')

if (-not ($cssMatch.Success -and $bodyMatch.Success -and $jsMatch.Success)) {
  throw 'Não foi possível extrair CSS, corpo ou JavaScript do index.html.'
}

$css = $cssMatch.Groups['css'].Value.Trim()
$body = $bodyMatch.Groups['body'].Value.Trim()
$js = $jsMatch.Groups['js'].Value.Trim()
$assets = Get-ChildItem -LiteralPath $repoRoot -File |
  Where-Object { $_.Extension -in '.png', '.webp', '.jpg', '.ico' } |
  Sort-Object { $_.Name.Length } -Descending

function Convert-AssetReferences {
  param(
    [Parameter(Mandatory)][string]$Content,
    [Parameter(Mandatory)][string]$Prefix
  )

  $result = $Content
  foreach ($asset in $assets) {
    $result = $result.Replace($asset.Name, "$Prefix/$($asset.Name)")
  }
  return $result
}

$bodyPlanA = Convert-AssetReferences -Content $body -Prefix '{{ event_asset_base }}'

$planATemplate = @'
<!--
  templateType: page
  isAvailableForNewContent: true
  enableDomainStylesheets: false
  label: Evento presencial Nuvemshop Next · 26/08
-->
{% set event_asset_base = "__EVENT_ASSET_BASE_URL__" %}
<!doctype html>
<html lang="{{ html_lang }}" dir="{{ html_lang_dir }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#00102E">
  <title>{{ page_meta.html_title }}</title>
  <meta name="description" content="{{ page_meta.meta_description|escape_attr }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  __ADOBE_FONT_LINK__
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@1,6..96,400;1,6..96,500;1,6..96,600&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap">
  <link rel="preload" as="image" href="{{ event_asset_base }}/asset-hero-sala.webp" imagesrcset="{{ event_asset_base }}/asset-hero-sala-m.webp 1080w, {{ event_asset_base }}/asset-hero-sala.webp 2000w" imagesizes="100vw" fetchpriority="high">
  <link rel="stylesheet" href="{{ get_asset_url('./evento-modelos-negocio.css') }}">
  {{ standard_header_includes }}
  <link rel="icon" href="{{ event_asset_base }}/favicon-next.ico" sizes="any">
</head>
<body class="evento-modelos-negocio-page" data-page-version="1.0.0">
'@

$planATail = @'
<script charset="utf-8" src="https://js.hsforms.net/forms/embed/v2.js"></script>
<script src="{{ get_asset_url('./evento-modelos-negocio.js') }}" defer></script>
{{ standard_footer_includes }}
</body>
</html>
'@

$planAOutput = $planATemplate.TrimEnd() + "`r`n" + $bodyPlanA + "`r`n" + $planATail.TrimStart()
$developerFiles = Join-Path $finalRoot 'developer-files'
$assetsUpload = Join-Path $finalRoot 'assets-upload'

foreach ($directory in @($finalRoot, $developerFiles, $assetsUpload)) {
  New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

Set-Content -LiteralPath (Join-Path $developerFiles 'evento-modelos-negocio.html') -Value $planAOutput -Encoding UTF8
Set-Content -LiteralPath (Join-Path $developerFiles 'evento-modelos-negocio.css') -Value $css -Encoding UTF8
Set-Content -LiteralPath (Join-Path $developerFiles 'evento-modelos-negocio.js') -Value $js -Encoding UTF8

foreach ($asset in $assets) {
  Copy-Item -LiteralPath $asset.FullName -Destination (Join-Path $assetsUpload $asset.Name) -Force
}

$checksumPath = Join-Path $finalRoot 'CHECKSUMS-SHA256.txt'
$checksumLines = Get-ChildItem -LiteralPath $finalRoot -Recurse -File |
  Where-Object { $_.FullName -ne $checksumPath } |
  Sort-Object FullName |
  ForEach-Object {
    $relative = $_.FullName.Substring($finalRoot.Length + 1).Replace('\', '/')
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    "$hash  $relative"
  }
Set-Content -LiteralPath $checksumPath -Value $checksumLines -Encoding UTF8

$zipFinal = Join-Path $packageRoot 'ENTREGA-FINAL-plano-a.zip'
if (Test-Path -LiteralPath $zipFinal) {
  Remove-Item -LiteralPath $zipFinal -Force
}

Compress-Archive -Path (Join-Path $finalRoot '*') -DestinationPath $zipFinal -CompressionLevel Optimal

Write-Output "Entrega final Plano A: $zipFinal"
Write-Output "Assets copiados: $($assets.Count)"
