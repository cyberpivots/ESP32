param(
  [Parameter(Mandatory = $true)]
  [string]$Ssid,

  [Parameter(Mandatory = $true)]
  [string]$Passphrase,

  [Parameter(Mandatory = $true)]
  [string]$Out,

  [string]$WifiInterfaceAlias = "",
  [string]$WiredInterfaceAlias = "",
  [string]$ControlProbeHost = "192.168.200.153",
  [int]$ControlProbePort = 22,
  [string]$BaseUrl = "",
  [int]$TimeoutSeconds = 45,
  [string]$ProfileName = ""
)

$ErrorActionPreference = "Stop"
$profileAdded = $false
$connected = $false
$exitCode = 0

if ([string]::IsNullOrWhiteSpace($ProfileName)) {
  $ProfileName = "DOSC-BBS-COMPANION-TEMP-{0}" -f ([Guid]::NewGuid().ToString("N").Substring(0, 8))
}

function ConvertTo-PlainObject {
  param([object]$Value)
  if ($null -eq $Value) {
    return $null
  }
  return $Value | ConvertTo-Json -Depth 32 | ConvertFrom-Json
}

function Get-Field {
  param(
    [object]$Value,
    [string[]]$Path
  )
  $current = $Value
  foreach ($key in $Path) {
    if ($null -eq $current) {
      return $null
    }
    if ($current -is [System.Collections.IDictionary]) {
      $current = $current[$key]
    } else {
      $property = $current.PSObject.Properties[$key]
      if ($null -eq $property) {
        return $null
      }
      $current = $property.Value
    }
  }
  return $current
}

function New-WlanProfileXml {
  param(
    [string]$Name,
    [string]$NetworkSsid,
    [string]$Key
  )
  $escapedName = [Security.SecurityElement]::Escape($Name)
  $escapedSsid = [Security.SecurityElement]::Escape($NetworkSsid)
  $escapedKey = [Security.SecurityElement]::Escape($Key)
  return @"
<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
  <name>$escapedName</name>
  <SSIDConfig>
    <SSID>
      <name>$escapedSsid</name>
    </SSID>
  </SSIDConfig>
  <connectionType>ESS</connectionType>
  <connectionMode>manual</connectionMode>
  <MSM>
    <security>
      <authEncryption>
        <authentication>WPA2PSK</authentication>
        <encryption>AES</encryption>
        <useOneX>false</useOneX>
      </authEncryption>
      <sharedKey>
        <keyType>passPhrase</keyType>
        <protected>false</protected>
        <keyMaterial>$escapedKey</keyMaterial>
      </sharedKey>
    </security>
  </MSM>
</WLANProfile>
"@
}

function Get-ConnectedWifi {
  param([string]$ExpectedSsid)
  $text = (netsh wlan show interfaces) -join "`n"
  $blocks = $text -split "(\r?\n){2,}"
  foreach ($block in $blocks) {
    if ($block -match "(?m)^\s*State\s*:\s*connected\s*$" -and
        $block -match "(?m)^\s*SSID\s*:\s*$([regex]::Escape($ExpectedSsid))\s*$") {
      $name = ""
      if ($block -match "(?m)^\s*Name\s*:\s*(.+?)\s*$") {
        $name = $Matches[1]
      }
      return [ordered]@{
        connected = $true
        interfaceAlias = $name
        raw = $block
      }
    }
  }
  return [ordered]@{
    connected = $false
    interfaceAlias = ""
    raw = $text
  }
}

function Invoke-CompanionRequest {
  param(
    [string]$Method,
    [string]$Uri,
    [object]$Body = $null
  )
  $record = [ordered]@{
    method = $Method
    uri = $Uri
    ok = $false
    response = $null
    error = $null
  }
  try {
    if ($null -eq $Body) {
      $response = Invoke-RestMethod -Method $Method -Uri $Uri -TimeoutSec 10
    } else {
      $json = $Body | ConvertTo-Json -Compress
      $record["body"] = ConvertTo-PlainObject $Body
      $response = Invoke-RestMethod -Method $Method -Uri $Uri -TimeoutSec 10 -ContentType "application/json" -Body $json
    }
    $record["ok"] = $true
    $record["response"] = ConvertTo-PlainObject $response
  } catch {
    $record["error"] = $_.Exception.Message
    if ($_.Exception.Response -and $_.Exception.Response.GetResponseStream()) {
      $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
      $record["responseText"] = $reader.ReadToEnd()
    }
  }
  return $record
}

function Test-ControlNetwork {
  param(
    [string]$HostName,
    [int]$Port,
    [string]$ExpectedWiredAlias
  )
  $record = [ordered]@{
    ok = $false
    host = $HostName
    port = $Port
    wiredAdapterUp = $false
    wiredInterfaceAlias = $ExpectedWiredAlias
    probe = $null
    route = $null
    error = $null
  }
  try {
    if ([string]::IsNullOrWhiteSpace($ExpectedWiredAlias)) {
      $wired = Get-NetAdapter -Physical | Where-Object {
        $_.Status -eq "Up" -and $_.InterfaceDescription -notmatch "Wireless|Wi-Fi|802\.11"
      } | Select-Object -First 1
    } else {
      $wired = Get-NetAdapter -Name $ExpectedWiredAlias -ErrorAction Stop
    }
    if ($wired) {
      $record["wiredAdapterUp"] = $wired.Status -eq "Up"
      $record["wiredInterfaceAlias"] = $wired.Name
    }
    $probe = Test-NetConnection -ComputerName $HostName -Port $Port -InformationLevel Detailed -WarningAction SilentlyContinue
    $record["probe"] = ConvertTo-PlainObject $probe
    try {
      $route = Find-NetRoute -RemoteIPAddress $HostName -ErrorAction Stop |
        Sort-Object -Property RouteMetric, InterfaceMetric |
        Select-Object -First 1
      $record["route"] = ConvertTo-PlainObject $route
    } catch {
      $record["routeError"] = $_.Exception.Message
    }
    $record["ok"] = [bool]($record["wiredAdapterUp"] -and $probe.TcpTestSucceeded)
  } catch {
    $record["error"] = $_.Exception.Message
  }
  return $record
}

$proof = [ordered]@{
  schema = "esp32.bbs_companion_softap_windows_proof.v1"
  generatedAt = (Get-Date).ToUniversalTime().ToString("o")
  tool = "scripts/companion_softap_windows_proof.ps1"
  ssid = $Ssid
  profileName = $ProfileName
  passphrase = "<redacted>"
  physicalOutputClaim = $false
  wifi = [ordered]@{}
  controlNetwork = [ordered]@{}
  requests = [ordered]@{}
  cleanup = [ordered]@{
    disconnected = $false
    temporaryProfileDeleted = $false
  }
  failures = @()
}

try {
  $profileXml = New-WlanProfileXml -Name $ProfileName -NetworkSsid $Ssid -Key $Passphrase
  $profilePath = Join-Path $env:TEMP "$ProfileName.xml"
  Set-Content -LiteralPath $profilePath -Value $profileXml -Encoding UTF8
  try {
    $addArgs = @("wlan", "add", "profile", "filename=$profilePath", "user=current")
    if (-not [string]::IsNullOrWhiteSpace($WifiInterfaceAlias)) {
      $addArgs += "interface=$WifiInterfaceAlias"
    }
    $addOutput = netsh @addArgs
    $profileAdded = $true
    $proof["wifi"]["profileAdd"] = $addOutput

    $connectArgs = @("wlan", "connect", "name=$ProfileName", "ssid=$Ssid")
    if (-not [string]::IsNullOrWhiteSpace($WifiInterfaceAlias)) {
      $connectArgs += "interface=$WifiInterfaceAlias"
    }
    $proof["wifi"]["connectCommand"] = netsh @connectArgs
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
      Start-Sleep -Seconds 2
      $status = Get-ConnectedWifi -ExpectedSsid $Ssid
      if ($status.connected) {
        $connected = $true
        break
      }
    } while ((Get-Date) -lt $deadline)
    $proof["wifi"]["status"] = $status
    if (-not $connected) {
      throw "Wi-Fi did not connect to $Ssid before timeout"
    }

    $wifiAlias = $WifiInterfaceAlias
    if ([string]::IsNullOrWhiteSpace($wifiAlias)) {
      $wifiAlias = $status.interfaceAlias
    }
    $ipConfig = Get-NetIPConfiguration -InterfaceAlias $wifiAlias -ErrorAction Stop
    $gateway = $ipConfig.IPv4DefaultGateway.NextHop | Select-Object -First 1
    if ([string]::IsNullOrWhiteSpace($gateway)) {
      throw "Connected Wi-Fi interface has no IPv4 default gateway"
    }
    $proof["wifi"]["interfaceAlias"] = $wifiAlias
    $proof["wifi"]["gateway"] = $gateway
    $proof["wifi"]["ipv4"] = ConvertTo-PlainObject $ipConfig.IPv4Address

    $proof["controlNetwork"] = Test-ControlNetwork -HostName $ControlProbeHost -Port $ControlProbePort -ExpectedWiredAlias $WiredInterfaceAlias

    if ([string]::IsNullOrWhiteSpace($BaseUrl)) {
      $BaseUrl = "http://$gateway"
    }
    $proof["baseUrl"] = $BaseUrl
    $proof["requests"]["state"] = Invoke-CompanionRequest -Method "GET" -Uri "$BaseUrl/api/state"
    $proof["requests"]["allOff"] = Invoke-CompanionRequest -Method "POST" -Uri "$BaseUrl/api/all-off" -Body @{seq = 1}
    $proof["requests"]["dummyOutput"] = Invoke-CompanionRequest -Method "POST" -Uri "$BaseUrl/api/dummy-output/1" -Body @{seq = 2; active = $true}
  } finally {
    Remove-Item -LiteralPath $profilePath -Force -ErrorAction SilentlyContinue
  }
} catch {
  $exitCode = 2
  $proof["failures"] += $_.Exception.Message
} finally {
  if ($connected) {
    try {
      $disconnectArgs = @("wlan", "disconnect")
      if (-not [string]::IsNullOrWhiteSpace($WifiInterfaceAlias)) {
        $disconnectArgs += "interface=$WifiInterfaceAlias"
      }
      $proof["cleanup"]["disconnectCommand"] = netsh @disconnectArgs
      $proof["cleanup"]["disconnected"] = $LASTEXITCODE -eq 0
    } catch {
      $proof["cleanup"]["disconnectError"] = $_.Exception.Message
    }
  }
  if ($profileAdded) {
    try {
      $deleteArgs = @("wlan", "delete", "profile", "name=$ProfileName")
      if (-not [string]::IsNullOrWhiteSpace($WifiInterfaceAlias)) {
        $deleteArgs += "interface=$WifiInterfaceAlias"
      }
      $proof["cleanup"]["deleteProfileCommand"] = netsh @deleteArgs
      $proof["cleanup"]["temporaryProfileDeleted"] = $LASTEXITCODE -eq 0
    } catch {
      $proof["cleanup"]["deleteProfileError"] = $_.Exception.Message
    }
  }
  $outPath = [System.IO.Path]::GetFullPath($Out)
  $outDir = [System.IO.Path]::GetDirectoryName($outPath)
  if (-not [string]::IsNullOrWhiteSpace($outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
  }
  $proof["completedAt"] = (Get-Date).ToUniversalTime().ToString("o")
  $proof | ConvertTo-Json -Depth 32 | Set-Content -LiteralPath $outPath -Encoding UTF8
}

if (-not (Get-Field -Value $proof -Path @("controlNetwork", "ok"))) {
  $exitCode = 2
}
if ((Get-Field -Value $proof -Path @("requests", "state", "response", "status")) -ne "ok") {
  $exitCode = 2
}
if ((Get-Field -Value $proof -Path @("requests", "allOff", "response", "status")) -ne "ok") {
  $exitCode = 2
}
if ((Get-Field -Value $proof -Path @("requests", "dummyOutput", "response", "reason")) -ne "dummy_output_disabled") {
  $exitCode = 2
}
if (-not (Get-Field -Value $proof -Path @("cleanup", "temporaryProfileDeleted"))) {
  $exitCode = 2
}
if (-not (Get-Field -Value $proof -Path @("cleanup", "disconnected"))) {
  $exitCode = 2
}
exit $exitCode
