# ddas_project
```bash
pip install fastapi uvicorn sqlalchemy databases asyncpg redis supabase
```
pip install python-multipart

To run
```
python run.py
```
just git clone


Remember to increase buffer if necessaryy while pushing 
git config --global http.postBuffer 157286400


![Project GIF](https://media.giphy.com/media/G1vplGMypxBcp7kx32/giphy.gif?cid=790b7611az3g0bdnvl64f1vc1iudbkw7gg7io20b4t89wgq6&ep=v1_gifs_search&rid=giphy.gif&ct=g)



# 🛡️ Data Download Duplication Alert System (DDAS)

> **Smart India Hackathon 2024 Finalist Project**  
> A real-time file deduplication and monitoring system designed to prevent storage bloat, enhance workflow efficiency, and alert users of duplicate data downloads.

---

## 📌 Overview

**DDAS** is a desktop-based intelligent alert system that detects duplicate files during downloads or uploads, helping users avoid unnecessary storage usage. The system calculates the file's hash in real-time, compares it against a centralized database, and alerts users if a duplicate is detected. It also monitors folders for changes and maintains a history of previously handled files.

This system is ideal for organizations, academic institutions, and personal users looking to streamline file management and avoid redundancy.

---

## 🚀 Features

- ✅ Real-time **duplicate file detection** using SHA-256 hashing
- 🔁 Continuous folder monitoring to detect new or modified files
- 🔔 Instant **notification alerts** for duplicates
- 📁 Upload and compare files across multiple locations
- 🌐 RESTful API endpoints for file upload, hash checking, and metadata retrieval
- 📦 Integration with **Supabase** for cloud-based, real-time storage
- ⚡ Fast and efficient backend built with **FastAPI**
- 🖥️ **Electron.js-based cross-platform desktop app**
- 📊 Saves bandwidth and reduces storage by up to **60%**
- 🔒 Privacy-first architecture and scalable design

---

## 📂 System Architecture

```
User Action (Download / Upload / Modify)
       ↓
Real-time File Hashing (SHA-256)
       ↓
Cross-check with Supabase Database
       ↓
If Duplicate → Alert User
Else → Store Metadata in DB
```

---

## 🛠️ Tech Stack

| Component     | Technology        |
|---------------|-------------------|
| Frontend      | Electron.js       |
| Backend       | FastAPI (Python)  |
| Database      | Supabase (PostgreSQL) |
| File Hashing  | SHA-256 Algorithm |
| API Layer     | RESTful APIs      |

---

## 🧠 How It Works

1. **Hash Calculation**  
   Each file is hashed using the SHA-256 algorithm to generate a unique identifier.

2. **Metadata Comparison**  
   File metadata (name, size, path) and hash are checked against a Supabase-stored database.

3. **Duplicate Detection**  
   If a match is found, the user receives an alert with options to proceed or cancel the download/upload.

4. **Monitoring**  
   The Electron app watches specified folders and triggers the backend pipeline for every new or updated file.

---

## 🔧 Installation

### Backend (FastAPI)

```bash
git clone https://github.com/your-username/ddas-backend.git
cd ddas-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (Electron.js)

```bash
git clone https://github.com/your-username/ddas-electron.git
cd ddas-electron
npm install
npm start
```

> ⚠️ Ensure your Supabase credentials are properly configured in the `.env` file.

---

## 📈 Impact & Benefits

- 💾 **Storage Optimization**: Prevents up to 40–60% redundant data usage.
- 🌐 **Bandwidth Savings**: Reduces unnecessary file transfers.
- ⚙️ **Workflow Efficiency**: Detects duplication before action, improving productivity.
- 🧩 **Plug-and-Play Integration**: Easy to integrate in institutional systems or personal workflows.
- 📣 **Real-Time Alerts**: Keeps users informed immediately of potential duplicates.

---

## 📚 Research & References

- [Supabase Docs](https://supabase.com/docs)  
- [FastAPI Docs](https://fastapi.tiangolo.com)  
- [File Deduplication Strategies](https://hivo.co/blog/cutting-clutter-strategies-for-file-deduplication)  
- [TMDB API](https://www.themoviedb.org/documentation/api)

---

## 🧪 Future Enhancements

- Role-based access control (RBAC) for secure multi-user environments  
- Cloud sync support for OneDrive/Google Drive  
- File preview support and duplicate resolution suggestions  
- Analytics dashboard for tracking storage savings

---

## 👨‍💻 Authors

- Atharva Gaikwad  
- Team Ctrl + Alt + Elite (Smart India Hackathon 2024)

---

## 📃 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

