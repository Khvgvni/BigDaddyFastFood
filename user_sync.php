<?php
/**
 * API для синхронизации данных пользователей между Telegram ботом и мини-приложением
 * Версия: 1.0
 */

// Настройки
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Путь к CSV файлу
define('CSV_FILE', __DIR__ . '/../bigdaddy_ff/user.csv');
define('CSV_LOCK_FILE', CSV_FILE . '.lock');

// Обработка preflight запросов
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

/**
 * Логирование (опционально)
 */
function logMessage($message) {
    $logFile = __DIR__ . '/sync_log.txt';
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($logFile, "[$timestamp] $message\n", FILE_APPEND);
}

/**
 * Чтение CSV файла с блокировкой
 */
function readCSV() {
    if (!file_exists(CSV_FILE)) {
        // Создаем файл с заголовками если не существует
        $headers = "telegram_id,name,phone,dob,addr,username\n";
        file_put_contents(CSV_FILE, $headers);
        return [['telegram_id', 'name', 'phone', 'dob', 'addr', 'username']];
    }
    
    $fp = fopen(CSV_FILE, 'r');
    if (!$fp) {
        return false;
    }
    
    // Получаем shared lock для чтения
    flock($fp, LOCK_SH);
    
    $data = [];
    while (($row = fgetcsv($fp)) !== false) {
        $data[] = $row;
    }
    
    flock($fp, LOCK_UN);
    fclose($fp);
    
    return $data;
}

/**
 * Запись CSV файла с блокировкой
 */
function writeCSV($data) {
    $fp = fopen(CSV_FILE, 'w');
    if (!$fp) {
        return false;
    }
    
    // Получаем exclusive lock для записи
    flock($fp, LOCK_EX);
    
    foreach ($data as $row) {
        fputcsv($fp, $row);
    }
    
    flock($fp, LOCK_UN);
    fclose($fp);
    
    return true;
}

/**
 * Поиск пользователя в CSV
 */
function findUser($telegramId, $data) {
    foreach ($data as $index => $row) {
        if ($index === 0) continue; // Пропускаем заголовок
        if ($row[0] === $telegramId) {
            return [
                'index' => $index,
                'data' => [
                    'telegram_id' => $row[0],
                    'name' => $row[1] ?? '',
                    'phone' => $row[2] ?? '',
                    'dob' => $row[3] ?? '',
                    'addr' => $row[4] ?? '',
                    'username' => $row[5] ?? ''
                ]
            ];
        }
    }
    return null;
}

/**
 * Валидация данных
 */
function validateUserData($data) {
    $errors = [];
    
    // Валидация телефона (если указан)
    if (!empty($data['phone']) && !preg_match('/^\+?[0-9]{10,15}$/', $data['phone'])) {
        $errors[] = 'Неверный формат телефона';
    }
    
    // Валидация даты рождения (если указана)
    if (!empty($data['dob'])) {
        $date = DateTime::createFromFormat('Y-m-d', $data['dob']);
        if (!$date || $date->format('Y-m-d') !== $data['dob']) {
            $errors[] = 'Неверный формат даты рождения';
        }
    }
    
    return $errors;
}

// Основная логика
try {
    // Получаем метод запроса
    $method = $_SERVER['REQUEST_METHOD'];
    
    if ($method === 'GET') {
        // Чтение данных
        $data = readCSV();
        if ($data === false) {
            throw new Exception('Не удалось прочитать CSV файл');
        }
        
        echo json_encode([
            'success' => true,
            'data' => $data,
            'count' => count($data) - 1 // Минус заголовок
        ]);
        
    } elseif ($method === 'POST') {
        // Сохранение данных
        $input = file_get_contents('php://input');
        $request = json_decode($input, true);
        
        if (!$request) {
            throw new Exception('Неверный формат JSON');
        }
        
        $action = $request['action'] ?? '';
        $telegramId = $request['telegram_id'] ?? '';
        $userData = $request['data'] ?? [];
        
        if (empty($telegramId)) {
            throw new Exception('Не указан telegram_id');
        }
        
        // Валидация данных
        $errors = validateUserData($userData);
        if (!empty($errors)) {
            throw new Exception('Ошибки валидации: ' . implode(', ', $errors));
        }
        
        if ($action === 'save') {
            // Читаем текущие данные
            $data = readCSV();
            if ($data === false) {
                throw new Exception('Не удалось прочитать CSV файл');
            }
            
            // Ищем пользователя
            $user = findUser($telegramId, $data);
            
            $row = [
                $telegramId,
                $userData['name'] ?? '',
                $userData['phone'] ?? '',
                $userData['dob'] ?? '',
                $userData['addr'] ?? '',
                $userData['username'] ?? ''
            ];
            
            if ($user) {
                // Обновляем существующего пользователя
                $data[$user['index']] = $row;
                logMessage("Обновлен пользователь: $telegramId");
            } else {
                // Добавляем нового пользователя
                $data[] = $row;
                logMessage("Добавлен новый пользователь: $telegramId");
            }
            
            // Сохраняем данные
            if (!writeCSV($data)) {
                throw new Exception('Не удалось записать CSV файл');
            }
            
            echo json_encode([
                'success' => true,
                'message' => 'Данные сохранены',
                'telegram_id' => $telegramId,
                'action' => $user ? 'updated' : 'created'
            ]);
            
        } elseif ($action === 'load') {
            // Загрузка данных конкретного пользователя
            $data = readCSV();
            if ($data === false) {
                throw new Exception('Не удалось прочитать CSV файл');
            }
            
            $user = findUser($telegramId, $data);
            
            if ($user) {
                echo json_encode([
                    'success' => true,
                    'data' => $user['data']
                ]);
            } else {
                echo json_encode([
                    'success' => false,
                    'error' => 'Пользователь не найден'
                ]);
            }
            
        } else {
            throw new Exception('Неизвестное действие: ' . $action);
        }
        
    } else {
        throw new Exception('Метод не поддерживается');
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
    logMessage("Ошибка: " . $e->getMessage());
}
?>

