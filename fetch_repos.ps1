$response = Invoke-RestMethod -Uri 'https://api.github.com/users/wanyview/repos?per_page=100&sort=updated'
$response | ForEach-Object { 
    $name = $_.name
    $desc = $_.description
    if ($desc -eq $null) { $desc = "" }
    Write-Host "$name - $desc"
}
