<?php
// Webhook de déploiement — appelé par GitHub Actions
$secret = 'SA_DEPLOY_2024_SECRET';

// Vérifier le token secret
$token = $_SERVER['HTTP_X_DEPLOY_TOKEN'] ?? '';
if (!hash_equals($secret, $token)) {
    http_response_code(403);
    die('Forbidden');
}

// Appeler l'API cPanel en local (pas bloqué par le firewall)
$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL            => 'https://localhost:2083/execute/VersionControl/update',
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => 'repository_root=%2Fhome%2Fgmmlmb57%2Fpublic_html',
    CURLOPT_HTTPHEADER     => ['Authorization: cpanel gmmlmb57:0WNSW7F0QHF0SLFRW9IHO09M3S9EVO'],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_TIMEOUT        => 30,
]);
$result = curl_exec($ch);
$error  = curl_error($ch);
curl_close($ch);

if ($error) {
    http_response_code(500);
    echo "Erreur curl: $error";
} else {
    http_response_code(200);
    echo "Déployé avec succès\n$result";
}
