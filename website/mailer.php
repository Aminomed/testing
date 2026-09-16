<?php
/**
 * Sicheres PHP Mailer-Skript fuer Terminabsagen und Rezeptbestellungen
 * (DSGVO-konform, laeuft lokal auf dem Server)
 */

header('Content-Type: application/json');

// Erlaube nur POST-Requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method not allowed"]);
    exit;
}

// Lese den JSON-Body der Anfrage
$json = file_get_contents('php://input');
$data = json_decode($json, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Invalid JSON payload"]);
    exit;
}

// E-Mail-Einstellungen
$to = "praxisdr.rahemi-pour@hotmail.de";
$subject = isset($data['_subject']) ? $data['_subject'] : "Neue Anfrage über Website";

// Generiere E-Mail-Inhalt aus den JSON-Daten
$message = "Sie haben eine neue Anfrage über Ihre Website erhalten:\n\n";
$message .= "=========================================\n\n";

foreach ($data as $key => $value) {
    // Interne Felder ueberspringen
    if ($key === '_subject' || $key === '_captcha') continue;
    
    // Daten sicher machen
    $safe_key = htmlspecialchars(strip_tags($key));
    $safe_value = htmlspecialchars(strip_tags($value));
    
    $message .= $safe_key . ":\n" . $safe_value . "\n\n";
}

$message .= "=========================================\n";
$message .= "Diese E-Mail wurde automatisch vom System generiert.";

// E-Mail-Header
$headers = "From: webmaster@" . $_SERVER['SERVER_NAME'] . "\r\n";
$headers .= "Reply-To: no-reply@" . $_SERVER['SERVER_NAME'] . "\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

// E-Mail senden
if (mail($to, $subject, $message, $headers)) {
    http_response_code(200);
    echo json_encode(["status" => "success", "message" => "E-Mail erfolgreich gesendet."]);
} else {
    http_response_code(500);
    echo json_encode(["status" => "error", "message" => "Fehler beim Senden der E-Mail."]);
}
?>
