#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║     🌐 CYBERSUITER WEB - INTERFACE MODERNE POUR RAILWAY 🌐                       ║
║                                                                                  ║
║     Application web Flask avec interface moderne responsive                      ║
║     Déployable sur Railway, Render, Heroku, etc.                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, render_template_string, jsonify, request, send_file
from flask_cors import CORS
import subprocess
import os
import json
import time
import socket
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Détection automatique de l'environnement
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT') is not None
PORT = int(os.environ.get('PORT', 8888))

# Chemin ADB (local seulement)
if not IS_RAILWAY:
    ADB_EXE = r"C:\Users\hanie.DESKTOP-TNL4MAV\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
else:
    ADB_EXE = "adb"  # Sur Railway, ADB ne sera pas disponible directement

# État global
devices = {}
logs = []
start_time = datetime.now()

# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE HTML MODERNE
# ═══════════════════════════════════════════════════════════════════════════════

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 CYBERSUITER - Control Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a25;
            --bg-hover: #252535;
            --accent: #00ff88;
            --accent-dim: #00cc6a;
            --danger: #ff4757;
            --warning: #ffa502;
            --info: #3742fa;
            --text-primary: #ffffff;
            --text-secondary: #8888aa;
            --border: #2a2a3a;
            --shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            --glow: 0 0 30px rgba(0, 255, 136, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: 
                radial-gradient(ellipse at 20% 80%, rgba(0, 255, 136, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(55, 66, 250, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0) 0%, var(--bg-primary) 100%);
        }

        /* Header */
        .header {
            background: rgba(18, 18, 26, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, var(--accent), var(--info));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: var(--glow);
        }

        .logo-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--accent), #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-text span {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid var(--accent);
            border-radius: 50px;
            font-size: 0.85rem;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }

        /* Main Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), var(--info));
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow);
            border-color: var(--accent);
        }

        .stat-icon {
            width: 50px;
            height: 50px;
            background: rgba(0, 255, 136, 0.1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: var(--accent);
            margin-bottom: 1rem;
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }

        /* Main Content Grid */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 1.5rem;
        }

        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Devices Section */
        .section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
        }

        .section-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .section-title i {
            color: var(--accent);
        }

        .section-content {
            padding: 1.5rem;
        }

        /* Device Cards */
        .devices-grid {
            display: grid;
            gap: 1rem;
        }

        .device-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            transition: all 0.3s ease;
        }

        .device-card:hover {
            border-color: var(--accent);
            background: var(--bg-hover);
        }

        .device-card.online {
            border-left: 4px solid var(--accent);
        }

        .device-card.offline {
            border-left: 4px solid var(--danger);
            opacity: 0.7;
        }

        .device-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .device-info h3 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .device-info p {
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
        }

        .device-status {
            padding: 0.25rem 0.75rem;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .device-status.online {
            background: rgba(0, 255, 136, 0.2);
            color: var(--accent);
        }

        .device-status.offline {
            background: rgba(255, 71, 87, 0.2);
            color: var(--danger);
        }

        .device-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .device-stat {
            text-align: center;
            padding: 0.5rem;
            background: var(--bg-primary);
            border-radius: 8px;
        }

        .device-stat-value {
            font-size: 1.1rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }

        .device-stat-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        .device-actions {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        /* Buttons */
        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-primary {
            background: var(--accent);
            color: #000;
        }

        .btn-primary:hover {
            background: var(--accent-dim);
            transform: translateY(-2px);
        }

        .btn-secondary {
            background: var(--bg-hover);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }

        .btn-secondary:hover {
            border-color: var(--accent);
        }

        .btn-danger {
            background: rgba(255, 71, 87, 0.2);
            color: var(--danger);
            border: 1px solid var(--danger);
        }

        .btn-danger:hover {
            background: var(--danger);
            color: #fff;
        }

        .btn-icon {
            width: 36px;
            height: 36px;
            padding: 0;
            justify-content: center;
        }

        /* Quick Actions */
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }

        .action-btn {
            padding: 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }

        .action-btn:hover {
            border-color: var(--accent);
            transform: translateY(-3px);
            box-shadow: var(--glow);
        }

        .action-btn i {
            font-size: 1.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
            display: block;
        }

        .action-btn span {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* Logs */
        .logs-container {
            max-height: 300px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }

        .log-entry {
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            gap: 1rem;
        }

        .log-time {
            color: var(--accent);
            white-space: nowrap;
        }

        .log-message {
            color: var(--text-secondary);
        }

        /* Add Device Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            width: 90%;
            max-width: 500px;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .modal-header h2 {
            font-size: 1.25rem;
        }

        .modal-close {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5rem;
            cursor: pointer;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .form-group input {
            width: 100%;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus {
            outline: none;
            border-color: var(--accent);
        }

        .modal-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .modal-actions .btn {
            flex: 1;
            justify-content: center;
            padding: 0.75rem;
        }

        /* Toast Notifications */
        .toast-container {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 2000;
        }

        .toast {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: slideInRight 0.3s ease;
            box-shadow: var(--shadow);
        }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(100px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .toast.success { border-left: 4px solid var(--accent); }
        .toast.error { border-left: 4px solid var(--danger); }
        .toast.info { border-left: 4px solid var(--info); }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 3rem;
        }

        .empty-state i {
            font-size: 4rem;
            color: var(--border);
            margin-bottom: 1rem;
        }

        .empty-state h3 {
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .empty-state p {
            color: var(--text-secondary);
            font-size: 0.9rem;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>

    <header class="header">
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon">🔥</div>
                <div class="logo-text">
                    <h1>CYBERSUITER</h1>
                    <span>Remote Control Panel v2.0</span>
                </div>
            </div>
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>Système Actif</span>
            </div>
        </div>
    </header>

    <main class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-mobile-alt"></i></div>
                <div class="stat-value" id="total-devices">0</div>
                <div class="stat-label">Appareils Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-wifi"></i></div>
                <div class="stat-value" id="online-devices">0</div>
                <div class="stat-label">En Ligne</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-clock"></i></div>
                <div class="stat-value" id="uptime">00:00:00</div>
                <div class="stat-label">Temps Actif</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-terminal"></i></div>
                <div class="stat-value" id="commands">0</div>
                <div class="stat-label">Commandes</div>
            </div>
        </div>

        <div class="main-grid">
            <div class="section">
                <div class="section-header">
                    <div class="section-title">
                        <i class="fas fa-mobile-alt"></i>
                        Appareils Connectés
                    </div>
                    <button class="btn btn-primary" onclick="openAddModal()">
                        <i class="fas fa-plus"></i> Ajouter
                    </button>
                </div>
                <div class="section-content">
                    <div class="devices-grid" id="devices-container">
                        <!-- Devices will be loaded here -->
                    </div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div class="section">
                    <div class="section-header">
                        <div class="section-title">
                            <i class="fas fa-bolt"></i>
                            Actions Rapides
                        </div>
                    </div>
                    <div class="section-content">
                        <div class="quick-actions">
                            <div class="action-btn" onclick="executeAction('screenshot')">
                                <i class="fas fa-camera"></i>
                                <span>Screenshot</span>
                            </div>
                            <div class="action-btn" onclick="executeAction('vibrate')">
                                <i class="fas fa-vibrate"></i>
                                <span>Vibrer</span>
                            </div>
                            <div class="action-btn" onclick="executeAction('gps')">
                                <i class="fas fa-map-marker-alt"></i>
                                <span>GPS</span>
                            </div>
                            <div class="action-btn" onclick="executeAction('contacts')">
                                <i class="fas fa-address-book"></i>
                                <span>Contacts</span>
                            </div>
                            <div class="action-btn" onclick="executeAction('sms')">
                                <i class="fas fa-sms"></i>
                                <span>SMS</span>
                            </div>
                            <div class="action-btn" onclick="executeAction('apps')">
                                <i class="fas fa-th"></i>
                                <span>Apps</span>
                            </div>
                            <div class="action-btn" onclick="scanNetwork()">
                                <i class="fas fa-radar"></i>
                                <span>Scanner</span>
                            </div>
                            <div class="action-btn" onclick="forceReconnect()">
                                <i class="fas fa-sync"></i>
                                <span>Reconnecter</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <div class="section-header">
                        <div class="section-title">
                            <i class="fas fa-history"></i>
                            Logs
                        </div>
                        <button class="btn btn-secondary btn-icon" onclick="clearLogs()">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    <div class="section-content">
                        <div class="logs-container" id="logs-container">
                            <!-- Logs will appear here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Add Device Modal -->
    <div class="modal-overlay" id="add-modal">
        <div class="modal">
            <div class="modal-header">
                <h2><i class="fas fa-plus-circle"></i> Ajouter un Appareil</h2>
                <button class="modal-close" onclick="closeAddModal()">&times;</button>
            </div>
            <div class="form-group">
                <label>Nom de l'appareil</label>
                <input type="text" id="device-name" placeholder="Mon Téléphone">
            </div>
            <div class="form-group">
                <label>Adresse IP</label>
                <input type="text" id="device-ip" placeholder="192.168.1.XX">
            </div>
            <div class="form-group">
                <label>Port (optionnel)</label>
                <input type="text" id="device-port" placeholder="5555">
            </div>
            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeAddModal()">Annuler</button>
                <button class="btn btn-primary" onclick="addDevice()">
                    <i class="fas fa-plus"></i> Ajouter
                </button>
            </div>
        </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container" id="toast-container"></div>

    <script>
        let commandCount = 0;
        let uptimeSeconds = 0;
        
        // Uptime counter
        setInterval(() => {
            uptimeSeconds++;
            const h = Math.floor(uptimeSeconds / 3600);
            const m = Math.floor((uptimeSeconds % 3600) / 60);
            const s = uptimeSeconds % 60;
            document.getElementById('uptime').textContent = 
                `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
        }, 1000);

        // Refresh devices
        function refreshDevices() {
            fetch('/api/devices')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-devices').textContent = data.total;
                    document.getElementById('online-devices').textContent = data.online;
                    
                    const container = document.getElementById('devices-container');
                    
                    if (data.devices.length === 0) {
                        container.innerHTML = `
                            <div class="empty-state">
                                <i class="fas fa-mobile-alt"></i>
                                <h3>Aucun appareil connecté</h3>
                                <p>Cliquez sur "Ajouter" pour connecter un appareil</p>
                            </div>
                        `;
                        return;
                    }
                    
                    container.innerHTML = data.devices.map(device => `
                        <div class="device-card ${device.connected ? 'online' : 'offline'}">
                            <div class="device-header">
                                <div class="device-info">
                                    <h3>${device.name || device.model || 'Appareil'}</h3>
                                    <p>${device.id}</p>
                                </div>
                                <span class="device-status ${device.connected ? 'online' : 'offline'}">
                                    ${device.connected ? '● En ligne' : '○ Hors ligne'}
                                </span>
                            </div>
                            <div class="device-stats">
                                <div class="device-stat">
                                    <div class="device-stat-value">${device.battery || '?'}%</div>
                                    <div class="device-stat-label">Batterie</div>
                                </div>
                                <div class="device-stat">
                                    <div class="device-stat-value">${device.android || '?'}</div>
                                    <div class="device-stat-label">Android</div>
                                </div>
                                <div class="device-stat">
                                    <div class="device-stat-value">${device.model ? device.model.substring(0,8) : '?'}</div>
                                    <div class="device-stat-label">Modèle</div>
                                </div>
                            </div>
                            <div class="device-actions">
                                <button class="btn btn-primary btn-icon" onclick="deviceAction('${device.id}', 'screenshot')" title="Screenshot">
                                    <i class="fas fa-camera"></i>
                                </button>
                                <button class="btn btn-secondary btn-icon" onclick="deviceAction('${device.id}', 'vibrate')" title="Vibrer">
                                    <i class="fas fa-vibrate"></i>
                                </button>
                                <button class="btn btn-secondary btn-icon" onclick="deviceAction('${device.id}', 'info')" title="Info">
                                    <i class="fas fa-info-circle"></i>
                                </button>
                                <button class="btn btn-danger btn-icon" onclick="disconnectDevice('${device.id}')" title="Déconnecter">
                                    <i class="fas fa-power-off"></i>
                                </button>
                            </div>
                        </div>
                    `).join('');
                })
                .catch(err => console.error('Error:', err));
        }

        // Execute action
        function executeAction(action) {
            commandCount++;
            document.getElementById('commands').textContent = commandCount;
            
            fetch('/api/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: action})
            })
            .then(r => r.json())
            .then(data => {
                showToast(data.message, data.success ? 'success' : 'error');
                addLog(data.message);
            });
        }

        function deviceAction(deviceId, action) {
            commandCount++;
            document.getElementById('commands').textContent = commandCount;
            
            fetch('/api/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({device: deviceId, command: action})
            })
            .then(r => r.json())
            .then(data => {
                showToast(data.message, data.success ? 'success' : 'error');
                addLog(data.message);
            });
        }

        function disconnectDevice(deviceId) {
            fetch('/api/disconnect/' + encodeURIComponent(deviceId))
                .then(() => {
                    showToast('Appareil déconnecté', 'info');
                    refreshDevices();
                });
        }

        function scanNetwork() {
            showToast('Scan du réseau en cours...', 'info');
            addLog('Scan du réseau démarré');
            fetch('/api/scan')
                .then(r => r.json())
                .then(data => {
                    showToast(`${data.found} appareil(s) trouvé(s)`, 'success');
                    refreshDevices();
                });
        }

        function forceReconnect() {
            showToast('Reconnexion en cours...', 'info');
            fetch('/api/reconnect')
                .then(r => r.json())
                .then(data => {
                    showToast(data.message, data.success ? 'success' : 'error');
                    refreshDevices();
                });
        }

        // Modal functions
        function openAddModal() {
            document.getElementById('add-modal').classList.add('active');
        }

        function closeAddModal() {
            document.getElementById('add-modal').classList.remove('active');
        }

        function addDevice() {
            const data = {
                name: document.getElementById('device-name').value,
                ip: document.getElementById('device-ip').value,
                port: document.getElementById('device-port').value || '5555'
            };
            
            fetch('/api/connect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(r => r.json())
            .then(result => {
                showToast(result.message, result.success ? 'success' : 'error');
                if (result.success) {
                    closeAddModal();
                    refreshDevices();
                }
            });
        }

        // Logs
        function addLog(message) {
            const container = document.getElementById('logs-container');
            const time = new Date().toLocaleTimeString();
            container.innerHTML = `
                <div class="log-entry">
                    <span class="log-time">[${time}]</span>
                    <span class="log-message">${message}</span>
                </div>
            ` + container.innerHTML;
        }

        function clearLogs() {
            document.getElementById('logs-container').innerHTML = '';
            showToast('Logs effacés', 'info');
        }

        // Toast notifications
        function showToast(message, type = 'info') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            
            const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
            toast.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
            
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 5000);
        }

        // Initialize
        addLog('Interface initialisée');
        refreshDevices();
        setInterval(refreshDevices, 5000);
    </script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# ADB MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

def adb(args, timeout=10):
    """Exécuter une commande ADB"""
    if IS_RAILWAY:
        return "ADB non disponible sur Railway"
    try:
        cmd = [ADB_EXE] + args
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def shell(device_id, command, timeout=30):
    """Exécuter une commande shell"""
    if IS_RAILWAY:
        return "ADB non disponible sur Railway"
    try:
        cmd = [ADB_EXE, "-s", device_id, "shell", command]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_connected_devices():
    """Obtenir les appareils connectés"""
    global devices
    
    if IS_RAILWAY:
        # Demo data for Railway
        return {
            "demo-device": {
                "id": "demo-device",
                "name": "Demo Phone",
                "model": "TECNO CK6",
                "android": "13",
                "battery": "85",
                "connected": True
            }
        }
    
    result = adb(["devices", "-l"])
    new_devices = {}
    
    for line in result.split('\n'):
        if '\tdevice' in line and 'offline' not in line:
            parts = line.split()
            device_id = parts[0]
            
            model = shell(device_id, "getprop ro.product.model")
            android = shell(device_id, "getprop ro.build.version.release")
            battery_info = shell(device_id, "dumpsys battery | grep level")
            battery = battery_info.split(":")[-1].strip() if ":" in battery_info else "?"
            
            new_devices[device_id] = {
                "id": device_id,
                "name": devices.get(device_id, {}).get("name", model),
                "model": model,
                "android": android,
                "battery": battery,
                "connected": True
            }
    
    devices = new_devices
    return devices

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/devices')
def api_devices():
    devs = get_connected_devices()
    return jsonify({
        "total": len(devs),
        "online": len([d for d in devs.values() if d.get('connected')]),
        "devices": list(devs.values())
    })

@app.route('/api/command', methods=['POST'])
def api_command():
    data = request.json
    device_id = data.get('device')
    command = data.get('command')
    
    if IS_RAILWAY:
        return jsonify({"success": True, "message": f"Commande '{command}' simulée (mode demo)"})
    
    if not device_id and devices:
        device_id = list(devices.keys())[0]
    
    if not device_id:
        return jsonify({"success": False, "message": "Aucun appareil connecté"})
    
    result = ""
    if command == 'screenshot':
        shell(device_id, "screencap -p /sdcard/screen.png")
        result = "Screenshot pris"
    elif command == 'vibrate':
        shell(device_id, "input keyevent 27")
        result = "Vibration envoyée"
    elif command == 'gps':
        result = shell(device_id, "dumpsys location | grep 'last known' -A 2")[:200]
    elif command == 'contacts':
        result = "Extraction des contacts..."
    elif command == 'sms':
        result = "Lecture des SMS..."
    elif command == 'apps':
        result = shell(device_id, "pm list packages -3")[:200]
    elif command == 'info':
        model = shell(device_id, "getprop ro.product.model")
        android = shell(device_id, "getprop ro.build.version.release")
        result = f"{model} - Android {android}"
    else:
        result = f"Commande inconnue: {command}"
    
    return jsonify({"success": True, "message": result})

@app.route('/api/connect', methods=['POST'])
def api_connect():
    data = request.json
    ip = data.get('ip')
    port = data.get('port', '5555')
    name = data.get('name', 'Appareil')
    
    if IS_RAILWAY:
        return jsonify({"success": True, "message": "Connexion simulée (mode demo)"})
    
    target = f"{ip}:{port}"
    result = adb(["connect", target])
    
    if "connected" in result.lower() and "cannot" not in result.lower():
        devices[target] = {"id": target, "name": name, "connected": True}
        return jsonify({"success": True, "message": f"Connecté à {target}"})
    
    return jsonify({"success": False, "message": f"Échec: {result}"})

@app.route('/api/disconnect/<path:device_id>')
def api_disconnect(device_id):
    if not IS_RAILWAY:
        adb(["disconnect", device_id])
    if device_id in devices:
        del devices[device_id]
    return jsonify({"success": True})

@app.route('/api/scan')
def api_scan():
    if IS_RAILWAY:
        return jsonify({"found": 1, "message": "Scan simulé (mode demo)"})
    
    get_connected_devices()
    return jsonify({"found": len(devices), "message": f"{len(devices)} appareil(s) trouvé(s)"})

@app.route('/api/reconnect')
def api_reconnect():
    if IS_RAILWAY:
        return jsonify({"success": True, "message": "Reconnexion simulée (mode demo)"})
    
    # Tenter reconnexion aux IPs connues
    known_ips = ["192.168.1.11", "192.168.1.13"]
    for ip in known_ips:
        for port in [45115, 5555, 34877]:
            result = adb(["connect", f"{ip}:{port}"])
            if "connected" in result.lower() and "cannot" not in result.lower():
                return jsonify({"success": True, "message": f"Reconnecté à {ip}:{port}"})
    
    return jsonify({"success": False, "message": "Échec de reconnexion"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": str(datetime.now() - start_time)})

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 60)
    print("   🌐 CYBERSUITER WEB SERVER")
    print("=" * 60)
    print(f"   Mode: {'Railway' if IS_RAILWAY else 'Local'}")
    print(f"   Port: {PORT}")
    print(f"   URL: http://localhost:{PORT}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=PORT, debug=not IS_RAILWAY)
