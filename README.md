# Ether
Ether Discord bot OpenAI toolkit
## Supports 
Most text generative models, DALL E 2, DALL E 3, GPT Visual, with option to change endpoint
## Filetype support 
txt, doc, docx, odt, rtf, python, lua, epub, c, cpp, rust, nim, csv, excel, js, sh, ps1, css, php, html, conf, log, pcap, ocsf, xml, json, sql
## Slash commands
/ether, /manager, /openai-options, /chatbot-options, /sharing-options, /association-options, /terms
## Administrative commands
banuser, banguild, unban, list, setstatus, logout, leave
## Will create / requires
1. data & temp directories (for image and file processing)
2. terms db, blacklist db (users who agree to terms, users or servers blocked from using bot)
## Setup for Linux 
*to use Windows substitute Linux libraries such as soffice, tshark*
1. Install requirements listed below
2. Add ID's in these places:
   ```
   Lines 78 - 87 admin id, guild id, roles, dev, notification channels
   ```
3. Change bot ID in these places (or search / replace using 1147188428048437358):
   ```
   366, 4351, 4366, 4509, 4619 + 4620, 4778, 5030, 5037
   ```
4. Add your bot token
## Requirements
**Apt** 
```
libreoffice (soffice) 
tshark (pcap processing)
python 3.10, pip3
```
**Pip3** 
```
discord-py-slash-command==2.3.2
discord-py-slash-command==2.3.2
discord-py-slash-command==2.3.2
discord-py-slash-command==1.7
discord.py==1.7
langchain==0.0.148
gpt_index==0.4.24
docx==0.2.4
python-docx
openai==0.28.1
beautifulsoup4
ebooklib
sqlparse
pyshark
pymupdf
aiofiles
python-magic
feedparser
pyshark
sqlite3
```
## Gitbook knowledgebase
https://ether-2.gitbook.io/ether/
## Support server
https://discord.com/invite/gSMNvfDGa2
## Developer
https://www.linkedin.com/in/nicholas-dustin-065560108/


