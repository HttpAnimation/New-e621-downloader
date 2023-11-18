<?php
// Implement status page logic here

// Specify the path to the Python script log file
$logFilePath = 'app.log';

// Read the log file content
$logContent = file_get_contents($logFilePath);

// Split the log content into an array of lines
$logLines = explode("\n", $logContent);

// Display the last 10 log entries (adjust as needed)
$lastEntries = array_slice($logLines, -10);

// Print the status page
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Status Page</title>
</head>
<body>
    <h1>Status Page</h1>
    <ul>
        <?php foreach ($lastEntries as $entry): ?>
            <li><?php echo htmlspecialchars($entry); ?></li>
        <?php endforeach; ?>
    </ul>
</body>
</html>
