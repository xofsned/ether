# 👋 Welcome to Ether
---> For > v30 (min) 11/11/2024
The legacy Ether has depreciated OpenAI, LMStudio, and user sessions support - due to recent dangers in *build your own chatbot* chatbots. 
See `ether.min.py` - a minimal system for LM Studio with model, temperature, tokens, and prompt options.
Built for multi-user environments with a user options approach.

---> For < v29 (no longer being hosted or maintained as of 11/11/2024)
> Ether is an AI toolkit that aims to give users the power to configure their OpenAI or LM Studio experience in Discord using an amnesiac approach
 * See: https://ether-2.gitbook.io/ether
### AI Support
 * OpenAI Models - chat, visual, DALL E (2 & 3) and embeddings
 * LM Studio Text Generative Models
   
### Filetype Support
*txt, doc, docx, odt, rtf, python, lua, epub, c, cpp, rust, nim, csv, excel, js, sh, ps1, css, php, html, conf, log, pcap, ocsf, xml, json, sql*

### Visual Support
*jpg, jpeg, png, webp*

### Additional Features
- Save and load sessions by JSON
- Create, save, and load associations
- Generate unique access with options such as per channel, per role, or per user access
- Give users unique prompts and the ability to have segmented context 
- Options for context compilation and formatting
- Options for bot-to-bot chat
- Session management utilities for starting, stopping, or extending sessions
- Class for built-in AI use (outside of user sessions)

### Commands
 * /ether - view stats such as uptime, set schedule, and backlinks to OpenAI status
 * /terms - agree or revoke terms
 * /manager - manage, view, create, stop sessions
 * /openai-options - set the OpenAI options, e.g. model, temperature, tokens, prompt, role, etc
 * /chatbot-options - set the Discord chatbot options, e.g. context amount, context type, mention requirement, etc
 * /lmstudio-options - configure for LM Studio endpoint
 * /b2b-options - add, view, download or upload associations generated in Ether
 * /sharing-options - allow users or roles specific api access with time limits or iterative limits
   
### Administrative Keyword Commands
 * banuser - ban a user from using the bot
 * banguild - ban a guild from using the bot
 * unban - unban a user or guild from using bot
 * list - list current bans
 * setstatus - set the schedule object in /ether
 * logout - command the bot to logout
 * leave - command the bot to leave a server
 * - Also adjust new built in chat (EthersSession class)

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
