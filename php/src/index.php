<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health & Wellness IoT Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        h1, h2 { color: #333; }
        .container { display: flex; gap: 40px; }
        .data-section { flex: 1; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #eef; }
    </style>
</head>
<body>

    <h1>Health & Wellness IoT Dashboard</h1>
    <div class="container">
        <div class="data-section">
            <h2>Live Heart Rate Readings (SQL)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Device ID</th>
                        <th>Heart Rate (BPM)</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    try {
                        $pdo = new PDO('sqlite:/var/www/health_data.db');
                        $stmt = $pdo->query("SELECT timestamp, device_id, heart_rate FROM heart_rate_readings ORDER BY timestamp DESC LIMIT 20");
                        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                            echo "<tr>";
                            echo "<td>" . date('Y-m-d H:i:s', (int)$row['timestamp']) . "</td>";
                            echo "<td>" . htmlspecialchars($row['device_id']) . "</td>";
                            echo "<td>" . htmlspecialchars($row['heart_rate']) . "</td>";
                            echo "</tr>";
                        }
                    } catch (Exception $e) {
                        echo "<tr><td colspan='3'>Could not connect to SQLite database: " . $e->getMessage() . "</td></tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>

        <div class="data-section">
            <h2>Physical Activity Logs (MongoDB)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Steps</th>
                        <th>Calories Burned</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    try {
                        $mongoClient = new MongoDB\Driver\Manager("mongodb://mongodb:27017");
                        $query = new MongoDB\Driver\Query([], ['sort' => ['timestamp' => -1], 'limit' => 20]);
                        $cursor = $mongoClient->executeQuery('health_wellness_db.activity_logs', $query);

                        foreach ($cursor as $document) {
                            echo "<tr>";
                            echo "<td>" . date('Y-m-d H:i:s', (int)$document->timestamp) . "</td>";
                            echo "<td>" . htmlspecialchars($document->metrics->steps_taken) . "</td>";
                            echo "<td>" . htmlspecialchars($document->metrics->calories_burned) . "</td>";
                            echo "</tr>";
                        }
                    } catch (Exception $e) {
                        echo "<tr><td colspan='3'>Could not connect to MongoDB: " . $e->getMessage() . "</td></tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>