Add-Type -AssemblyName System.Device
$GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher
$GeoWatcher.Start()
while (($GeoWatcher.Status -ne 'Ready') -and ($GeoWatcher.Permission -ne 'Denied')) { Start-Sleep -Milliseconds 100 }
if ($GeoWatcher.Permission -eq 'Denied') {
    Write-Output "Access to location is denied."
} else {
    $GeoWatcher.Position.Location.Latitude
    $GeoWatcher.Position.Location.Longitude
}
