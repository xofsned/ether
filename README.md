# 👋 Welcome to Ether

> Ether is an OpenAI toolkit that aims to give users the power to configure their OpenAI experience in Discord using an amnesiac approach
 * See: https://ether-2.gitbook.io/ether
### Model Support
 * gpt-3.5-turbo, gpt-4, gpt-4o, gpt-4-1106-preview, gpt-4-0613, gpt-4-0314, gpt-3.5-turbo-16k-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-1106, gpt-3.5-turbo-0613, gpt-3.5-turbo-0301
 * DALL E 2, DALL E 3
 * GPT Visual
 * Optional: custom endpoints for using with utilities such as LM Studio
   
### Filetype Support
*txt, doc, docx, odt, rtf, python, lua, epub, c, cpp, rust, nim, csv, excel, js, sh, ps1, css, php, html, conf, log, pcap, ocsf, xml, json, sql*

### Visual Support
*jpg, jpeg, png, webp*

### Commands
 * /ether - view stats such as uptime, set schedule, and backlinks to OpenAI status
 * /terms - agree or revoke terms
 * /manager - manage, view, create, stop sessions
 * /openai-options - set the OpenAI options, e.g. model, temperature, tokens, prompt, role, etc
 * /chatbot-options - set the Discord chatbot options, e.g. context amount, context type, mention requirement, etc
 * /association-options - add, view, download or upload associations generated in Ether
 * /sharing-options - allow users or roles specific api access with time limits or iterative limits
 * /advanced-options - initialize bot-to-bot (gpt-to-gpt) chat with logging utilities for generating data
   
### Administrative Keyword Commands
 * banuser - ban a user from using the bot
 * banguild - ban a guild from using the bot
 * unban - unban a user or guild from using bot
 * list - list current bans
 * setstatus - set the schedule object in /ether
 * logout - command the bot to logout
 * leave - command the bot to leave a server

### Primary Keywords
 * draw - generate an image
 * variate - variate an image 
 * embed - initialize an embedded session with the LLM Predictor
 * set - set session variables by message

***
### Installing
1. Requires Python3, pip3
2. Some functionalities require: Libreoffice (specifically soffice package), Tshark (for pcap support)
3. Install requirements from requirements.txt
4. Alter lines 76-85 to contain your role, notification channel and server ID's
5. Search and replace '1130638110196256828' (9 instances) - replace with your bot user ID
6. Add your bot token
   
### Additional Items
1. Will generate databases - terms, blacklist
2. requires temp & data directories for processing data
***

### Ether's Home Server

https://discord.gg/z3S7CUB3QS

### Ether on TopGG

https://top.gg/bot/1130638110196256828

</details>

***
