---
description: 'Last Updated: Feb 2nd, 2024'
---

# 🐛 bugs

{% hint style="info" %}
✅ = resolved, ❌ = active, ✖️ = anomaly
{% endhint %}

<details>

<summary>✅ Using slash command to add prompt shows both success and fail response, process is success</summary>

Additionally, using prompt add, prompt view, prompt clear, are early returns, which faults combined arguments

Use prompt add and prompt management in isolation as arguments

Use the keyword set to set the prompt by message instead of by slash command

</details>

<details>

<summary>✅ Error in association view / download, command fail</summary>

Investigating...

</details>

<details>

<summary>✅ Error when trying to view prompt</summary>

Resolve ready...

</details>

<details>

<summary>✅ Keywords such as draw not applied in message reply</summary>

Resolve ready...

</details>

<details>

<summary>✅ Errors in stacked context in default prompt when user prompt is none</summary>

Resolve ready...

</details>

<details>

<summary>✅ After embed, message shows backlink to direct message channel instead of session channel when embedding through direct message</summary>

Resolve ready...

</details>

<details>

<summary>✅ Process cancellation message displays in direct message at times when exiting embed in a session channel</summary>

Resolve ready...

</details>

<details>

<summary>❌ Attachment sent by author in session channel when Ether awaits files for embedding in direct message, attachments are obtained from session channel (author intercepts)</summary>

Resolve ready...

</details>

<details>

<summary>❌ Reaching maximum extensions errors ability to remove an extension</summary>

Resolve ready...

\
Bypass: in the extended channel, add the channel to a different session, this will move the extension from one session to the other allowing you to remove and manage extensions in the original session

</details>

<details>

<summary>✅ Iterations deducted even on API error when sharing set</summary>



</details>

<details>

<summary>✅ Command for exit_all is not functioning</summary>



</details>

<details>

<summary>✅ Hyperlink error when using keyword embed without attachments</summary>



</details>

<details>

<summary>✅ Saving and loading session config does not contain all possible variables</summary>



</details>

<details>

<summary>✅ Two critical errors that have lead to Ether going offline</summary>

1. Embedding large CSV (beyond capacity of current free use)
   * replicated in 74k row CSV
2. Rate limiting and non GPT4 access error handling
   * Non access to GPT-4 models or DALLE 3

In events when user does not have access to a model or is rate limited, an error can lead to Ether losing Discord heartbeat These errors will have attempted mitigations in next update

</details>

<details>

<summary>✅ Ether doesn't reply to user in other users shared session when original user has a session in some other location.</summary>

This is from Ether's _has session_ check, which helps manage shared sessions and mitigate multiple bot replies. This check should go by channel so users can still engage with other shared sessions and only default to their own when it is in the same channel. This is easy fix and I'll pin it in Todo list..

</details>

<details>

<summary>✅ It seems when embedding into a previously active chat session, sometimes ether does not embed the files.</summary>

However if starting a fresh session and beginning with embedding, it seemed fine to enter, exit, and enter various embeddings.

Will investigate this issue soon.

</details>

<details>

<summary>✅ Invoking <code>/ether [manager] [start]</code> in an active session clears the prompt</summary>



</details>

<details>

<summary>✅ After adding users with association_share the <code>/ether [manager] [session-config]</code> command throws error.</summary>

In coming weeks I will resolve, the error is from multiple users from association\_share, and displaying those users in session-config.

</details>

<details>

<summary>✅ Most recent update allows session authors to access associations from outside their session containing associations</summary>

Seems to only be in other sessions by the author.

This was new performance update that might need slight adjustments.

To clarify: author sets associations in session channel, but then in their other sessions they can trigger associations from their first session.

Session authors used to have overrides that were not governed by channel / location, if this logic gets budged it allows the author to use their sessions outside of their channels.

It is non critical, only effecting session authors.

</details>

<details>

<summary>✅ Error in <strong>variate</strong></summary>

Resolved in developer version, release repair in update later today

</details>

<details>

<summary>✅ Ether is still having some session extension issues seemingly when exceeding 5 sessions, so I don't think it will effect most users.</summary>

Additionally earlier a session corrupted and I had to restart it, so there is some error that may cause session hang.

</details>

<details>

<summary>✅ There seems to still be some error in extensions. I theorize it is cross server or after surpassing a certain number of sessions.</summary>

Error: when selecting a session number to extend, the process does not extend the desired session.

I plan to do additional testing, if I can resolve error by Tuesday night I will push fix in that update.

</details>

<details>

<summary>✅ When session author uses keyword 'extend' with their message to Ether, Ether may reply from all of the user's current active sessions.</summary>

The extend feature was keyword based in beta. It has been replaced by slash command, however the keyword beta part has not been removed.

This bug only effects session authors. Session authors should avoid the keyword 'extend' until Tuesday night to avoid receiving multiple bot responses.

</details>

<details>

<summary>✅ Ether seemingly stop responding when leaving embedding unattended for some time.</summary>

I have a solution ready for this error, will be resolved soon.

</details>

<details>

<summary>✅ When awaiting API response and checking session config concurrently, session config listing fails to launch, until after API response.</summary>

_The API processing process is locked in that moment, so Ether cannot obtain the details of your session in that point of time_ Wait a moment for your api calls to complete, then re-invoke the stat card

</details>

<details>

<summary>✅ Setting shared chat + embed during session initialization is not setting embed as True.</summary>

Altering share state in active session works.

</details>

<details>

<summary>✅ New options: frequency, presence, top_P, not being changed while in session.</summary>

Error identified. For now, these are working during session initialization, but not being altered during session.

</details>

<details>

<summary>✅ Error in new extensions feature.</summary>

Seemingly effective when exceeding three sessions, so may not effect users currently. _When extending a session, extension drops. Initializing additional session causes multiple replies. Additional session count offset in sessions over three._

</details>

<details>

<summary>✅ Some parameters corrupting Ether upon embedding data.</summary>



1.  Under investigation. Likely related to:

    * Too high of temperature
    * Too much context
    * Using Prompt

    _Currently Ether does not support prompting in embeds..._ (edited)
2.  _\[_7:12 PM_]_

    ### active

    * When replying to an association to remove the single instance,
      * when the association is a discord emoji wrapped in :colonemoji:
      * removing single instance wipes entire association instance

    Ether saves assocations as: `trigger: object1, object2, object3` Discord emoji with colon is voiding the _remove a single object from associations_ feature. Will implement a fix for this in next update.

</details>

<details>

<summary>✅ Issues with /me command?</summary>

Today /me is not working for _me_ not sure if it's error in my sessions or if this is wider issue..

</details>

<details>

<summary>✅ Embedded sessions not exiting correctly, intermittent session offset on exit in /me</summary>



</details>

<details>

<summary>✅ Association errors adter uploading, Ether not responding to variate</summary>



</details>

<details>

<summary>✅ Command false positive fail downloading or uploading associations</summary>



</details>

<details>

<summary>✅ Image returning error in 'data'</summary>



</details>

<details>

<summary>✅ Multiple errors with responding and roles, random session closing</summary>



* Error 1 is from API drops during key validation, in the next update there will be timeout to better handle this error.
* Error 2 is synonymous, at times we message Ether and the API call is made but the API does not return a response from gateway error or other.

All of these issues will be resolved in the next update. For anyone who has these errors, please be patient ![🙂](https://canary.discord.com/assets/6e72cca8dcf91e01fac8.svg) I will be working very hard to push the next Ether release very soon.

</details>

<details>

<summary>✅ user initializes session, doesn't receive direct message, then Ether says they already have a session</summary>

This is not an error, but the incident of causation could be handled more gracefully, so we can pin this in the next update.

What happens is - user has direct messages disabled, Ether fails to send the message but the process continues anyway.

Within, if I recall, 2 minutes, it will expire. That process is designed to expire if no response is received.

If you do not receive direct message check your discord privacy settings. If you do not have the direct message to respond to, be patient and it should timeout after two minutes.

</details>

<details>

<summary>✅ !keys is still shown as a command in !ether</summary>

Ether does not currently have a keys command. It previously did, but it is not good to have key saving without encryption. This feature was being secured in other ways no doubt, but not to the degree it should be. A new keyring and encryption module was introduced to ether developer version and was faced with issue with Google cloud KMS. _In time I hope to release key and session saving using encryption and Google KMS_

#### Additionally

The `!chat info`, `!image info`, and `!learn info` are missing the `!exit` option. `!exit` only works as a direct command in the session and session channel. Additionally users can exit using `!me 1 exit` or `!me 2 exit` for example, using correlating number for the session. Use `!me` to see your active sessions. _These issues will be updated in the next release_

</details>

<details>

<summary>✅ In !chat in !prompt, prompt not saving</summary>

Semi random error I just noticed, must be from the failed governing prompt. We will definitely see this solved, and governing prompt released very soon.

</details>

<details>

<summary>✅ extending error from !learn, session hang beyond !me scope</summary>

In !image, !learn, on key error and filetype check error, session hangs and cannot exit.

* In !learn on sending code via text file (more so Lua & Token Contracts Open Source Codes)
* In !image (possibly other) on invalid key quota error - error handling error

_I will work to fix these asap!! We will make plans to roll out emergency update within 48hr_

</details>

<details>

<summary>✅ Ether not embedding data? from .txt</summary>

If anyone ever notices error in Ether it is tremendous help if they report the error. ~~I see there is error. I will try to solve this asap.~~ Error Determined: _Some text files containing code are triggering the text file filetype circumvention_

* The code in the text file faults the file type check

_Error handling fail_

* This error is rare (only when giving programming code in text file)

_Ether should display an error alerting the user the file check errored_

* Error check function was not in connection like it should be

Fix for error handling already solved, will roll out in next update. Additionally - I will look to better handle text files containing code. Note: If the session hangs beyond the scope of exiting with `!me` it will timeout automatically, but it seems to take a while. I will work to add additional timeout code for events like this, but the original error handling handles this error properly, however was not nested properly in this last iteration.

</details>

<details>

<summary>✅ <strong>Error</strong> in !context</summary>

_After switching from context 0 to context > 0 and back to context 0, the session errors and does not exit correctly with !me._

I just discovered this error and will look into it tomorrow. I will also plan a small patch update for this error and the error in !variate asap.

</details>

<details>

<summary>✅ <strong>Error</strong> in !variate</summary>

_Indeed it is quite challenging sometimes to keep it 'all together' LOL_

The !variate function is invoking an exit proceedure, I can work on fixing this in coming days, but everything else seems good to go.

</details>

<details>

<summary>✅ <strong>Error</strong> in !learn</summary>

Ether not fetching websites properly, session hanging beyond `!me exit` scope.

Have traced this bug / error and will solve in the AM _Tentative plan to reboot Ether by 10 AM EST with minor repairs_

</details>

<details>

<summary>✅ <strong>Error</strong> in !prompt</summary>

Not sure what the error is, will look into it soon.

If you session bricks after !prompt use !me to exit session

</details>

<details>

<summary>✅ <strong>Limitation:</strong> Ether doesn't respond to replies in direct message</summary>

I actually am surprised I was able to make it chat in DM. I will see what I can do to make direct message more interactive, but reply seems to be a different event type than mention..

</details>

<details>

<summary>✅ <strong>Error</strong> Traceback error found in !exit <em>at times</em></summary>

_If you have issues with exit....._

use the !me command `!me 1 exit` or `!me 2 exit`

I will look into the error ~~asap~~later, marked as non-critical and conditional error.

</details>

<details>

<summary>✅ <strong>Issue</strong> Ether double posts when having default session</summary>

_Some small error in the update process, will patch this asap_

</details>

<details>

<summary>✅ <strong>Issue</strong> Ether does not respond to specific messages</summary>

_A few of us were troubleshooting some code, and everytime we pasted the code to Ether, Ether would not respond..._

I determined this error is from Ether's web link filter. There was a web link in the code block that was causing the loop to skip the iteration.

Ether's code to ignore web links is actually old code from its legacy feature of not requiring mentioning. It allowed us to share web links, gifs, and other with each other while being in a session.

Ether's ability to converse without mention or reply is adapting in time, and the web link filter will be removed in this next update.

For now, if you find Ether is not responding to a specific message, please check web links and break their syntax by removing the web link entirely, or, by deleting the http/https part so the link is not recognized as a valid web link.

</details>

<details>

<summary>✅ <strong>Issue:</strong> Ether seems to be missing a word at the end of its first response in split message conditions</summary>

_This is from Ether's split response code. ChatGPT tends to return messages just barely exceeding the bot limit, so Ether attempts to split the response into two bot responses. Currently there is a small issue in my logic causing for roughly 1 word to be removed in the response split._

I will work to repair this issue asap and will push in the next update.

</details>

<details>

<summary>✅ Error after supplying Ether with OpenAI API key</summary>

_user gives Ether API key in direct message, Ether does not respond.._

Some users have reported the above issue. This is coming from Ether's key validator, which is currently having an issue - not telling the user when the key had an error.

If Ether does not respond after giving a key, this means there was an error with the key in terms of OpenAI accepting it. Notibly, when the key is getting an error "exceeded quota" https://discord.com/channels/907301373387898950/1139905745945640980/1147210665308737546 I will be fixing Ether to notify the user when there is error and push it in the next update.

However -

1: if your session freezes in this way, use `!flush @authormention` in the session channel to reset the session. 2: if your key is valid, Ether will take it and initialize session properly.

If Ether does not respond - currently, that means your key is either invalid or had an error return from OpenAI.

</details>

<details>

<summary>✅ Error in !prompt (not critical)</summary>

When setting a prompt, for now, avoid using symbols in your prompt. Currently the apostrophe used in a prompt using !prompt can cause Ether to stop responding.

If you ever have a case where Ether is not responding in a session, use the !flush command to clear the session. This event is becoming more rare and eventually will be mitigated entirely.

Example of !flush command: `!flush @usermention` OR `!flush userIDnumber`

Session authors can flush their own session, and server owners can also flush users sessions in their server if needed.

</details>

<details>

<summary>✅ Issus with new !terms command not working</summary>

Will be repairing this asap!!

</details>

<details>

<summary>✅ Error with !context</summary>

_context builds leading to token limit error with context_

Will attempt to implement update for this error tomorrow

</details>

<details>

<summary>✅ Ether having file validation errors with Lua scripts. This seemed to be an error with specifically processing a lua as a raw text.</summary>

Until I figure out the error, if you have issues with giving scripts, try putting the script in as .doc, .docx, or pdf, instead of raw text.

Note: I've only come across one lua so far that had errors, others did not. For some reason, certain lua scripts are triggering Ether's file validation system, and flagging them as possible file type circumvention.

</details>

<details>

<summary>✅ Prompting Error in !chat</summary>

First role assigned by session author must also be the first role to set a prompt. _index error_ currently requires first person given a role to be first person to set prompt, or the session hangs.

Will implement a fix for this in coming days.

</details>

<details>

<summary>✅ Error: key validation approving keys that have quota limit error</summary>

Error: Ether responded after session closing _This was the integrated chat that should only work in here, error will be solved today_

</details>

<details>

<summary>✅ Discovered error with prompt</summary>

_User's prompts are not saving_ Will mitigate this error today. _other updated below_

</details>
