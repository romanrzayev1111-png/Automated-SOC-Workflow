# Transcribed from WEEK2.docx image59. C:\SCA-Lab exists from the prior export.
# Review the local policy and preserve the before.inf export before running.
$dir = "C:\SCA-Lab"
$template = @"
[Unicode]
Unicode=yes
[Version]
signature="`$CHICAGO`$"
Revision=1
[System Access]
PasswordHistorySize = 24
"@

Set-Content -Path "$dir\fix.inf" -Value $template -Encoding Unicode
secedit /configure /db "$dir\fix.sdb" /cfg "$dir\fix.inf" /overwrite /areas SECURITYPOLICY /log "$dir\fix.log"
if ($LASTEXITCODE -ne 0) {
    throw "Security policy configuration failed. Check C:\SCA-Lab\fix.log"
}
secedit /export /cfg "$dir\after.inf" /areas SECURITYPOLICY
Select-String -Path "$dir\after.inf" -Pattern "PasswordHistorySize"
