---
description: 'Last Updated: Feb 2nd, 2024'
---

# 📓 Changelog



<details>

<summary>2/19/2024</summary>

* Repaired known issues from recent update on 17th of Feb, 2024
  * errors in exit\_all
  * missing variables in session save / load
  * hyperlink issue in info embeds
  * iterative deductions when sharing keyword set
* Added exit session method using session number
* Released payment portals for premium use and subscriptions

</details>

<details>

<summary>2/17/2024</summary>



* Bug fixes
* Refactored slash commands (final structure)
* Added DALL E 3 options
  * size options
  * style options
  * render multiple images from one prompt
* Extended file type support (now supporting 22 types):
  * xls, xlsx, html, php, css, log, config
* Added **`set`** keyword for session config by message
* Added sharing options for role, user, iterations, time
* Updated stats command
* Added additional context options
* No mention option to use Ether without mention or reply requirement
* Support in Direct Message (all options other than sharing options)
* Updates to status message embeds from Ether
* Updates to key validator timeout and error handling
* Premium subscription tier release
* Option to reset session defaults
* Better defined _fast embeds_ and _full embeds_
* Added sharing support for full embeds
* Added session config sharing support with **`set`**
* Ability to view a session's associations

</details>

<details>

<summary>12/19/2023</summary>

* Fixed bug with keyword 'extend'
* Performance updates with draw, variate, embed
  * Also fixed errors so Ether will still work if the first keyword is correct, even if there is double space or no space
* Seemingly fixed session extending
  * This always works perfect in testing, but buggy after
* Added error handling in DALL E 3 for session authors
* Updated EtherCereal share link in Ether
* Added utility to update link without reboot if this reoccurs
* Updated documentation
* Implemented possible fix for Ether ignoring 'embed'
  * This error has been anomaly
  * A refactor is in place to hopefully mitigate issue

#### Note on DALL E 3 error handling:

_I could not reproduce an error in testing that I have seen before. OpenAI returns JSON from API call, however the JSON does not have a 'data' object. Instead of logging the error myself, Ether will now print the returned JSON to an embed for the session author to see if there is error. This will help me debug in my own sessions, and it will also allow session authors to have more information on the error as well. Ether will show the session author the returned JSON from DALL E 3 when there is error as a hidden embed._ Hopefully we have moved passed some of the recent bugs and can see some solid uptime

</details>

<details>

<summary>12/16/2023</summary>

1.  #### First and foremost!

    * No changes to privacy, API handling, or data handling!

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) More sessions in free use

    * 4 sessions, 2 extensions per session (8 channels total)

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added Model Options

    * DALLE3 Option Added!!!!
    * DALLE3 Currently does not support multiple renders, size options, or variations
    * Ether will default DALLE3 in images now
    * Select image model in `/ether [image_model]`

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added session saving and loading

    * Downloading a session configuration - Ether will send you a json in direct message
    * After initializing a session you can upload a session configuration
    * Session configurations **do not include associations**
    * See `/ether [manager] [save-config] OR [load-config]`
    * Current objects supported: role, prompt, tokens, context, model, size, number, shared states, nicknames, frequency, presence, top\_p, unique name, temperature, image model, and revised prompt toggle for DALLE3

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added listener jump-starter

    * In the event Discord has an outage, and your session listeners are de-registered, you can jumpstart a session listener
    * In the session channel invoke `/ether [manager] [jump-listener]`
    * NOTE: I cannot test the overall functionality of this, as it would require outages right. It seems fully functional. If we have another outage, we will find out if it works.

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Association Features

    * Add or clear associations with slash command
    * Rename associations by either message command or slash command
    * To rename a trigger, do `triggerName >< newName`
    * Reminder: add trigger `trigger >> object`, clear all objects: `trigger >>` , remove single entry: reply to the bot msg with `trigger >>`

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added command to exit all sessions

    * In the event you cannot access an active session of yours (perhaps you got kicked or banned from a server)
    * See `/ether [manager] [exit_all]`

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Prompt Viewing

    * You can now view lengthy prompts using `/ether [manager] [prompt-view]`
    * You can also clear prompt two ways now - one in `/ether [manager] [prompt-clear]` or by giving keyword "clear" as the new prompt

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Updates to Embeddings

    * All draw, variate, and other features available while having embedding
    * Keep-alive feature: works like key validation - when enabled Ether will send a dummy request to the LLMPredictor every 6 hours to tell OpenAI it is still active
    * Keep-alive feature is enabled by default when an embedding is initialized
    * The keep-alive service will automatically stop when exiting an embedding
    * Toggle on or off with `/ether [manager] [keep-alive]`

    #### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Toggles

    * Toggles options will slowly be released in Ether as we bring back legacy features
    * Current working toggle: _**revised-prompt**_ will make Ether return both the generated image and revised-prompt object from DALLE3
    * Revised prompts are generated by OpenAI and DALLE3 - not by Ether
    * Toggles can only be done after session initialization

    #### ![🪲](https://canary.discord.com/assets/ba43c739de8d7ea1d9d1.svg) Bug Fixes and Embeds

    * Embeds displaying session information received a face lift, however it is best on PC
    * Some of the current active errors have been resolved
2. _\[_10:07 AM_]_Known Limitations in this update: Users who have shared access to create associations cannot create via slash command Note on sharing embed (embed share) - this shares the ability for other users to pass supported file types to Ether with a prompt as a one-time query, with a data limit of 20,000 characters. Primarily this is a side perk for items slightly larger than Discord message limit. For example, you have a json file 8,000 characters long and you want to extract specific data. These one-time pass embeddings do not require the keyword 'embed'. The keyword 'embed' locks you into a perpetual embedding. Note on residual embeds - even with keep-alive the embedding still seems to drop after some time. I am trying to solve this, but it is not an Ether error. Seems to be out of the window of \~12 hours.

</details>

<details>

<summary>12/02/2023</summary>

#### First and foremost!

* No changes to privacy, API handling, or data handling
* Depreciated **`/embed`**
* Depreciated **`/me`**

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added Model Options

* gpt-4-1106-preview, gpt-4-0613, gpt-4-0314, gpt-3.5-turbo-16k-0613, gpt-3.5-turbo-16k, gpt-3.5-turbo-1106, gpt-3.5-turbo-0613, gpt-3.5-turbo-0301, GPT4 Visual
  * GPT 3.5, GPT 4

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added API Options

* top\_P, frequency, presence, temperature range increase (0-2)

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) New way to Embed

* use keyword **'embed'** with or without your attachments and bot mention in an active session
* Embedding into a loop this way can only be done by the session author
* **without attachments:** Ether will send direct message for attachments
* **with attachments:** Ether will begin the embedding in the channel
* Use keyword **'exit'** with bot mention to exit an embedding
* Passing supported filetypes to Ether with no keyword will still perform a one-time pass embedding with your message content as the prompt (20,000 character limit)

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) GPT 4 Visual

* Takes **1 - 2 images**
* Supports **jpg, jpeg, png, webp**
* **No message content:** default prompt sent "describe this graphic"
* **With message content:** message content becomes prompt with image
* For now, to share GPT4 Visual requires Chat+Embed share

#### ![🍡](https://canary.discord.com/assets/78dab75dfb4c036d22e4.svg) Associations Update

* sharing chat no longer shares association creation
  * to allow another user to create associations in your session, use **`/ether [associations_share] [@user]`**
* clear associations option added
* remove a specific association by replying to it
* add multiple objects in one message
  * _examples....._
  * **`@ether this >> that`** associates 'this' with 'that'
  * **`@ether this >> that, though, two`** associates 'this' with 'that', 'though', 'two'
  * _lets say you want to remove specifically 'though'_
  * Reply to the message from Ether containing **'though'** with **`@ether this >>`**
  * **`@ether this >>`** removes all associations with 'this'

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Ether Keywords

* **draw** (anything following 'draw' becomes your prompt)
* **variate** (anything following 'variate' becomes your prompt)
* **embed** (embeds your files into a loop)
* **exit** (exits specifically an embedding session)

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added File Types

* epub, C, C++, Rust, Nim, CSV

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) New Command Structure

* We now use **`/ether [manager]`** to start, view, extend or exit sessions
* Added **`/ether [manager] [help]`** option
* Invoke **`/ether`** with no arguments for Ether or OpenAI status

#### ![➕](https://canary.discord.com/assets/457d314fcaea692b6842.svg) Added feature for extending sessions

* Free use limits **1 extension per session**
* Use session number to select session to extend
* in alternate channel, invoke **`/ether [extend] [session number]`**
* view your session numbers using **`/ether [manager] [sessions]`**
* use the same method for removing extensions as for adding extensions
* channels with extensions from shared sessions are considered a shared channel - only one share instance or one shared extension - per channel globally

#### ![🗒️](https://canary.discord.com/assets/2852bb14280807f44812.svg) Filetype Overlook

* Embeddings:
  * txt, doc, docx, pdf, rtf, odt, epub, js, py, sh, lua, ps1, c, cpp, rs, nim, csv
* GPT 4 Visual:
  * jpg, jpeg, png, webp
* DALL E:
  * jpg, jpeg, png

#### ![🪲](https://canary.discord.com/assets/ba43c739de8d7ea1d9d1.svg) Bug Fixes & Performance

* All current active errors fixed
* Additional performance updates in associations and embeddings

#### ![⏫](https://canary.discord.com/assets/b8998236cbec4e04e106.svg) Premium Features

* Two roles will be released soon in Discord server store and through tip.cc
  * Sessions Role: up to 10 concurrent sessions, 5 extensions per session
  * Data Role: increase in the amount of attachments and character count for embeddings
* No changes for Free users (other than the additional 1 extension per session update)

_**stay tuned for more info on these subscriptions....**_

</details>

<details>

<summary>11/05/2023</summary>

Small update ready for Ether

* fixed issues in variate
* additional timeout and error handling
* fixes for /chat associations download
* performance upgrades in /chat

Let's plan to reboot at 6PM EST today

</details>

<details>

<summary>11/04/2023</summary>

#### First and Foremost

* Ether uses slash commands now! See **`/ether`**
* The previous **`!learn`** command is now **`/embed`**
* **`/image`** removed, DALLE now inside **`/chat`**
* No API structure or privacy changes were made

#### ![:CD\_exit:](https://cdn.discordapp.com/emojis/861250089389391872.webp?size=44\&quality=lossless) Stats and Exit

* You can now remove yourself from terms using **`/terms revoke`**
* **`/chat manager stats`** to see session stats
* **`/status`** now includes OpenAI API status updates
* **`/me`** to view sessions
* **`/chat manager exit`** or **`/me exit sessionNumber`** to exit

#### ![:tadalolhd:](https://cdn.discordapp.com/emojis/666301381333876757.webp?size=44\&quality=lossless) All Features in `/chat`

* Embeds in **`/chat`** are:
  * limited to 20,000 characters (about the size of the average wikipedia page)
  * one time passes (data embedded, prompt given, instance disposed)
* **`@ether draw`** everything after _draw_ becomes your image prompt
* **`@ether variate`** + image attachment, everything after _variate_ becomes your image prompt
* **`@ether what is this?`** + attachment of supported document file type, _what is this?_ becomes prompt
* Session authors can set shared states:(Chat, Chat + Image, Chat + Embed, Chat + Image + Embed)

#### ![:tadalolhd:](https://cdn.discordapp.com/emojis/666301381333876757.webp?size=44\&quality=lossless) Options in **`/embed`**

* Added temperature option in **`/embed`** but this can only be set _before embedding_ and cannot be altered during session

#### ![:tadalolhd:](https://cdn.discordapp.com/emojis/666301381333876757.webp?size=44\&quality=lossless) Associations Utility **`/chat`** Mode

* **`@ether this >> that`** will associate _this_ with _that_, everytime a user messages 'this' Ether will respond with 'that'
* **`@ether this >>`** will erase all associations with the word 'this'
* Ether must be mentioned when creating an association, but not required for Ether to detect associated keywords
* The associations tool can be used for a range of things - keywords, phrases, tenor gifs, web links etc

![⚠️](https://canary.discord.com/assets/1d1dfaa9e1307e5d63df.svg) **Your assocations will be lost on session exit!!**

* **`/chat associations download`** to download your associations
* **`/chat associations upload`** to upload a associations file
* Downloading or uploading associations are done in direct message
* The associations utility is automatically active during `/chat` sessions
* A shared chat session also shares the ability to create associations

#### ![🛠️](https://canary.discord.com/assets/379ef7349e09f2bd41f3.svg) Items Postponed or disabled until next update

* Server wide sharing
* Fine Tuning
* Default sessions
* Dispersing unique roles / prompts
  * _The session author can set a role and/or prompt for themselves and with share mode that will be applied to every user_
* Eco mode is now the default mode while role and prompt distribution is under refactor
* Direct message session support

#### ![:etheremoji4:](https://cdn.discordapp.com/emojis/1167484589216911360.gif?size=44\&quality=lossless) Examples for new **`/chat`** features

* **`@ether draw something cool`**
  * keyword **`draw`** prompt becomes **`something cool`**
* **`@ether variate this image of a spaceman`** + attachment (png, jpg, jpeg)
  * keyword **`viariate`** prompt becomes **`this image of a spaceman`**
* **`@ether what is this?`** + attachment (supported type from **`/embed`**)
  * Single supported attachment with mention, **`what is this`** becomes prompt
* Premium access is being delayed a little longer for completion of server wide session sharing and maximum character embedding benchmarking.
* In the next update we will try for a throwback to re-instate role and prompt distribution, default mode, and advanced chatbot modes

</details>

<details>

<summary>10/18/2023</summary>

#### Changelog

* Fixed `!prompt` error
* Released prompt & role sharing
* Updated Embeds
* Added error reporting in `!status`

#### Prompt and Role Sharing

Now when you share your session you can also share your role and prompt. This way session author can share session access to other users, and also have a role or prompt applied to all users.

Each user who has their own unique session in a channel or has a unique role applied by the session author can have their own prompt. Any user without a session is defaulted to the shared session and shared prompt.

#### Updated `!status`

`!status` now contains both scheduled outages and current reported bugs. Every user should check Ether status with the status command before embedding data. Ether updates will always be coupled with 24 or more hour notice.

#### Updated Embeds

The help commands `!chat info`, `!image info`, `!learn info` now have been updated to reflect `!exit` use case in sessions and also minor repairs. `!learn info` now also contains supported file types.

_tips on role, prompt, and eco...._

If you have your own session, even if it is in the same channel as another shared session, you will default to your session.

If you have your own role and prompt in your own session, you will always use those even if you are in a shared session channel.

Session authors can give any user a role in their shared session, those users can set prompts for themselves.

When a user messages Ether and does not have a role or prompt or their own session they are defaulted to the shared session author role and prompt.

Eco mode (enabled by default) bundles all context with a single role and prompt. Eco mode disabled appends a role to each previous message based on the user role. Role and prompt sharing is not compatible with Eco disabled.

_roles in this context is OpenAI roles - `user` and `system`. System role has the most control over ChatGPT responses_

</details>

<details>

<summary>1-/15/2023</summary>

### Changelog:

* fixed most errors in error-report
* added user id cleaning in !learn (increased token effeciency)
* fixed image label in `!me` while in `!learn`

_I tried to roll out governing prompt, but it failed, it needs more testing. We will push that in next update._

* `!variate` is now working properly

\-- upload image file with `!prompt some details about the image` and Ether will pull the attachment and prompt

* There should also be better error handling when API key is quota limit or when filetype error occurs

</details>

<details>

<summary>10/04/2023</summary>

Changelog:

* removed time limitations in !learn
* fixed recent issues with website embedding
* added timeout on website fetch error
* added repairs to !prompt
* fixed split response truncate issue
* updated some embeds
* code optimizations for faster responses

Note: the current document of Ether Terms is out of date.

* The logic is the same, if you upload files for embedding a directory is made for you, the files are processed in there, after embedding the data into your ChatGPT model, the entire directory is deleted.
* The "Learning Log", "Upvote Log", and "Downvote Logs" seen in the documentation are from legacy features that may return in the future, but currently there is no log generating capabilities.

The documentation will be getting updated very soon! Currently Ether handles each session transactionally with amnesia, there is nothing _saved_ or _retained_.

</details>

<details>

<summary>10/02/2023</summary>

_Note: currently if you have sessions or a default session and you are in another user's shared session channel, Ether will still try to use your sessions. To participate in another users shared session you need to close your sessions._

```
Fixed double responses from chronological error (when starting default session first) 
Repaired session management logic
Repaired shared lambda logic
```

</details>

<details>

<summary>10/02/2023</summary>

_Ether and all updates other than key saving are seemingly functional._ Note: !keys command has been disabled. For now, Ether will not offer key saving, this will be updated within 1-2 weeks. New Primary Command Examples: \[command] \[default] e.g. `!chat default` \[command] \[info] e,g. `!chat info` New Secondary Command Examples: `!share [enable / disable]` `!model [3.5 / 4]` New !me Command Examples: `!me 1 newName` make custom session name `!me 1 exit` exit session 1

</details>

<details>

<summary>10/01/2023</summary>

1.  ### Changelog:

    ```
    added gpt4 option
    added keyring and encryption
    added context to !learn
    altered logic in !keys
    altered logic in file handling
    removed time limits on !chat
    removed time limits on !image
    added default session feature
    updated & decreased embed posting
    updated session manager
    removed !usage command
    removed !flush command
    added !share option
    relieved multi-user channel instances
    ```

    ### Command Changes:

    ```
    removed !usage
    removed !flush
    added !chat, !image, !learn info arg
    added !share
    added !context in !learn
    added !me args
    ```

    ### Updated Info Commands \[command] \[info]

    > _Instead of using **`!usage`** to view options for **`!chat`**, **`!image`**, and **`!learn`**, users can now run 'info' as an argument with the session commands. For example **`!chat info`** will display command options in !chat._

    > _Instead of using **`!flush`** to clear a session when **`!exit`** does not work, the function has been extended into the session manager **`!me`** so users can exit sessions from afar, such as in direct message with Ether. Use **`!me`** to see your sessions, then use session number to exit, for example: **`!me 1 exit`**._

    > _Now when users start a session it is not automatically shared with any users in the channel. Users can decide to share their instances with other users in a channel using **`!share`**._

    > _**`!learn`** now has **`!context`** option for sending previous messages in as context - consider this a experimental feature, as it seemed to confuse the AI._

    ### Updated Directory Structure

    > _I will be updating Ether terms ASAP, however, Ether no longer manages directories by server and instead uses a user instance approach. Therefore, when user creates **`!learn`** instance, their temporary session directory is created inside a unique user directory instance. After files are processed, they are still immediately discarded._

    ### Encryption and Keyring

    > _If a user chooses to save a key, an encryption key is made using unique data including the user ID, which is stored and managed by a keyring. When user saves API keys the API keys are encrypted using the encryption key. All user saved keys will now be encrypted, and the same expiry applies - if the key file seems orphaned it will be discarded by Ether's server security and integrity services._

    > _If and when a user chooses to save keys, a unique key file is created for the user along with a unique user directory. If keys are saved, the user directory will be present as long as the key file does not expire. In any case where the user does not have saved keys, the user directory is treated as temporary along with their session folders and is discarded on every instance._

    Note: session directories are only relevant to key saving and **`!learn`**

    ![🔥](https://canary.discord.com/assets/aece59a42123414f0a07.svg)

    2

    ![🚀](https://canary.discord.com/assets/1ddf8fc00f9071f1019c.svg)

    1
2.  _\[_8:07 PM_]_

    ### Removed Time Limits in **`!chat`** and **`!image`**

    > _Ether will no longer restrict time in **`!chat`** and **`!image`** modes. However the free access to Ether is still limited to 2 concurrent sessions, and there is still a time limit in Ether's **`!learn`** mode._

    ### New Default Session Feature \[command] \[default]

    > _Default session feature is a new and experimental feature that will likely be updated more in time. To generate a default session, you may pass 'default' as an argument when starting a session, for example: **`!chat default`****.**_

    > _Default sessions are fall back sessions for when the session channel ID does not match. If you have a default session, Ether will use your default session to respond to you anywhere you go that is outside of your other active channel sessions._

    ### Direct Message Support

    > _Ether now supports any sessions to be generated and used in direct message with Ether. Users can also view or exit any of their current sessions with Ether in direct message._

    ### Updates for **`!usage`**

    > _Users can now reference possible options for Ether's different modes by running the command with argument 'info' for example: **`!chat info`** or **`!image info`****.**_

    ### Removeed **`!flush`**

    > _It is still quite important a user can exit a session without being in the session channel. Instead of using **`!flush`** users can now exit any of their sessions from any where using the **`!me`** session manager. Pass the session number as an argument with 'exit', for example: **`!me 1 exit`** or **`!me 2 exit`** would exit session 1 or session 2._

    ### GPT-4.0 Option

    > _In **`!chat`** users can now invoke **`!model`** with a model argument, for example: **`!me model 4`**. The default is 3.5 - turbo. The options for **`!model`** are **`3.5`** & **`4`**._

    ### New **`!share`** Logic

    > _When a user initializes a session with Ether in a channel, Ether will only respond to the author of the session. At any point an author of a session can invoke **`!share enable`** in the session channel. When a session is shared, Ether will respond to any user in that channel. Ether will enforce that there is only one shared session per channel. At every instance in that channel that the session author is not resolved, Ether will respond using the shared session._

    ### New Session Channel Logic

    > _In the past Ether restricted one session per channel globally. Now, with the restriction is applied in the **`!share`** option instead. What this means is many users can have their own unique instances with Ether in the same channel. Additionally, for anyone in that channel who does not have a session, a user can share their session by invoking **`!share enable`** in the session channel. Any user who cannot be resolved as having their own session in that channel will be defaulted to the channel's shared session._

    ![🔥](https://canary.discord.com/assets/aece59a42123414f0a07.svg)

    1

    ![🚀](https://canary.discord.com/assets/1ddf8fc00f9071f1019c.svg)

    1
3.  _\[_8:07 PM_]_

    ### In Short!!

    > 1: Keys users choose to save are now encrypted 2: gpt4 is an option in !chat 3: Ether works in direct message 4: Your sessions are not _shared_ by default 5: Exit sessions using !me 6: Initialize a default session to have Ether respond anywhere you go 7: !context option in !learn 8: Get mode info using command argument 9: Enjoy no time limits in !chat and !image 10: No longer sorting user directories by server

</details>

<details>

<summary>09/15/2023</summary>

_It has been brought to my attention that the recent increase in token parameters in the !learn function is leading to over token limit responses, some of the parameters are slightly out of bounds, leading to a lack of response in Ether during !learn sessions from this last update..._

I will need to reboot Ether with a decreased token parameter. I will plan to do this **11:00 AM EST Today** Expected downtime - 1 minute.

</details>

<details>

<summary>09/14/2023</summary>

**Changelog**

```
increased session limit for free users
increased session limit for unlimited users
released eco mode in !chat
updated some embeds
relieved special character errors in !prompt
```

Session Limit Increases

_Free users can now have up to two concurrent sessions, unlimited users can have up to ten concurrent sessions_

New `!eco` Mode

_In this update !chat will be in a 'eco' mode by default. Users can disable this mode for technical purposes such as utalizing user roles to shape GPT in a multi-user environment. use `!eco disable / enable` in `!chat`_

Example of eco mode enabled versus disabled: _When eco mode = false and context > 0, we apply custom role to each user message_

```
[{'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'Hi, how are you?'}, {'role': 'user', 'content': 'I am good thank you, please share some recipes?'}, {'role': 'assistant', 'content': 'Sure thing, I can share recipes with you!]
```

_When we are in eco mode we apply all messages to a single role_

```
[{'role': 'user', 'content': 'hello Hi, how are you? I am good thank you, please share some recipes? Sure thing, I can share recipes with you!'}]
```

_In eco mode, when context is greater than zero, all previous messages are bound together. With eco mode disabled, users can more strategically prompt GPT with each user respective role applied to each of their previous messages, and 'assistant' role applied to ChatGPT responses. Users without custom roles get the 'user' role by default._ If you have previously gotten the error indicating the context length exceeds the max tokens - the eco mode will help to pull more context with less tokens. This mode can also be beneficial with programming, so the code in context is more robust.

</details>

<details>

<summary>09/12/2023</summary>

**Changelog**

```
added primary command !me
added secondary command !advanced
added secondary command !variate
added secondary command !mention
added secondary command !number
added secondary command !size
removed default learning log feature
removed embed style responses in !image
set static reacts in !learn as optional
set static reacts in !image as optional
bug fixes and additional error handling
updated !ether & !usage to reflect recent updates
added error handling in !prompt in !learn
code upgrades for faster processing
code upgrades for faster embedding
initialized the unlimited features
increased processing queue
additional msc. updates
```

**New `!me` Command**

!me is a command for managing sessions. Single session users can use this to locate their active session, multiple session users can use this to manage all of their sessions. Additionally, users can add custom naming to each of their sessions.

**New `!advanced` Command** _Note: this command is disabled temporarily_

!advanced will allow users to toggle on the static reacts in !image and !learn mode. The static reacts are getting an upgrade. Once the upgrade is done, this command will become available.

**New `!variate` Command**

In !image mode, users can now give their own images to Ether for DALL E 2 to variate. The argument must be passed while in !image mode. Additionally, you will need two arguments - your prompt and your attachment (image file). Ether is built to handle your file and prepare it for DALL E 2 - and will accept JPG, JPEG, or PNG.

**New `!mention` Command**

Specifically for !learn mode. In !learn mode, Ether will now default to requiring a mention or reply to respond. In !learn users can invoke !mention with an argument to enable or disable the mention mode. Whem mention is disabled, you do not have to mention or reply to Ether to get a response, rather Ether will respond to all user messages.

**New `!number` Command**

In !image, users can invoke the !number command with a integer argument in the range of 1 - 10, which represents the number of images DALL E 2 should return.

**New `!size` Command**

In !image, users can invoke the !size command with an integer argument in the range of 1 - 3, which represents which image size DALL E 2 should render in. OpenAI offers three sizes: 256x256, 512x512, and 1024x1024. Images given to Ether with !variate also render in this selected size.

**Removed Default learning log from !learn**

Going forward !learn mode will only allow for session authors to generate upvote, downvote logs, or bookmark AI responses, in !advanced mode. The overall learning log will no longer be generated.

**Unlimited Features**

With the upcoming unlimited Ether role, users can upload 10 attachments and 5 weblinks in a single session. Additionally, the character count for embedding is increased from 2 million to 10 million characters. The unlimited role also allows for eight concurrent sessions - still 1 session per channel.

**Looking into the future....** **1)** Ether will have more options in learn mode for initializing the temperature, selecting model to use, and also an embed extension feature where users can extend the embedded data without exiting the session. **2)** Ether will offer model options for the !chat mode **3)** Exit sessions using session manager feature **4)** CSV support (will include processing CSV data for natural language) **5)** Additional file type support **6)** Additional AI API support - such as Stable Diffusion **7)** Eco mode in !chat (incredibly cost efficient feature) **8)** Expanded static emoji react functionality such as embedding an AI response into an active session

</details>

<details>

<summary>09/04/2023</summary>

```
extended data support: js, py, sh, lua, ps1
added !status command
added !terms command
removed !notify
added more context to embeds
updated !ether & !usage embeds
increased timeout duration on api key request & check
```

**New Script Support**

You can now give Ether scripts in !learn mode. GPT is a great code interpreter. This feature has been tested and is incredible. Combined with Ether's other data options, it is possible to give Ether coding resources including both documentation and actual code in a single session. Users can now give Ether Python, Javascript, Lua, Shell, or Powershell scripts, and they will be embedded into the AI session.

**!status Command**

`!status` is now available, which will show Ether's server count, uptime, and any scheduled outages. I removed the `!notify` - Ether's push notifications. Instead, I will update the schedule variable when posting outage announcements. At any time you can invoke `!status` and see if there are any scheduled outages.

**!terms Command**

Users no longer _have_ to be a member of EtherCereal to use Ether. To use Ether, users can simply run `!terms` for information about the Terms and Privacy. Also, users can invoke `!terms agree` and will be able to use Ether without being a server member.

**Updated Embeds**

Updated `!ether`, `!usage`, and key error embeds to give more context and reflect recent updates, such as the `!flush <userID> *or* [@usermention]` command.

</details>

<details>

<summary>09/01/2023</summary>

Updates:

```
Fixed integrated chatbot issues
Added context to key error prompt
Added optional continue / cancel to errored key re-prompt
Fixed raw react errors
Expanded !flush to session authors
```

If you ever have a session get hung where Ether is unresponsive, even to !exit, you can use !flush to flush out the session. Only session authors and guild owners can perform the act of flushing.

```
!flush useridnumber
```

For example:

```
!flush 775445008672489525
```

I will add support for flushing by mention as well.

</details>
