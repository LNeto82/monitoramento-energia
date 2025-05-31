<?php
require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

if ($_SERVER['REQUEST_METHOD'] == 'GET' && $_SERVER['REQUEST_URI'] == '/equipments') {
    header('Content-Type: application/json');
    echo json_encode([
        'equipamentos' => ['guindaste', 'tubo de perfuração', 'bomba hidráulica']
    ]);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_SERVER['REQUEST_URI'] == '/dispatch') {
    $data = json_decode(file_get_contents('php://input'), true);

    $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
    $channel = $connection->channel();
    $channel->queue_declare('logistica', false, true, false, false);

    $msg = new AMQPMessage(json_encode($data));
    $channel->basic_publish($msg, '', 'logistica');

    $channel->close();
    $connection->close();

    echo "Mensagem enviada ao RabbitMQ";
}
