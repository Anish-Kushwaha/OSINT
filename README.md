## Social Media Finder OSINT Tool (OSINT)

![Python Version](https://img.shields.io/badge/python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 🌐 Overview

**Social Media Finder OSINT Tool** is a Python-based, open-source OSINT (Open Source Intelligence) tool designed to **find social media accounts linked to phone numbers** using publicly available information.  
It helps ethical hackers, security researchers, and OSINT enthusiasts track social media presence in a legal and educational way.

The tool searches the following platforms:

- Facebook  
- Instagram  
- LinkedIn  
- Twitter  
- Telegram  
- WhatsApp  
- GitHub  
- Public phone directories (Truecaller-like services)  

> ⚠️ **Disclaimer:** Only use this tool for educational or legal OSINT purposes. Unauthorized access or privacy violations are illegal.

---

## 🛠 Features

- **Cross-platform search:** Covers Facebook, Instagram, LinkedIn, Twitter, Telegram, WhatsApp, GitHub, and public phone directories.  
- **Phone number parsing:** Supports international phone numbers, validates numbers, and provides carrier and region information.  
- **Multiple search methods:** Uses account recovery flows, Google search patterns, direct links, and directory lookups.  
- **Comprehensive reporting:** Generates detailed reports showing platform, username, URL, search method, and details.  
- **Rate-limited queries:** Built-in `time.sleep()` between requests to avoid IP bans or blocking.  
- **Modular design:** Easy to add new platforms or modify existing search patterns.  

---

## 📂 Repository Structure
