param(
  [Parameter(Mandatory)]
  [ValidatePattern('^https://')]
  [string]$AssetBaseUrl,

  [ValidatePattern('^$|^https://')]
  [string]$AdobeFontCssUrl = ''
)

$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'developer-files\evento-modelos-negocio.html'
$destination = Join-Path $PSScriptRoot 'developer-files\evento-modelos-negocio-pronto.html'
$content = Get-Content -LiteralPath $source -Raw -Encoding UTF8
$fontLink = if ($AdobeFontCssUrl) { "<link rel=`"stylesheet`" href=`"$AdobeFontCssUrl`">" } else { '' }
$content = $content.Replace('__EVENT_ASSET_BASE_URL__', $AssetBaseUrl.TrimEnd('/'))
$content = $content.Replace('__ADOBE_FONT_LINK__', $fontLink)
Set-Content -LiteralPath $destination -Value $content -Encoding UTF8
Write-Output "Template pronto: $destination"
