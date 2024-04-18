---
description: Getting started with Ether
---

# 🌿 Basic Use

***

{% hint style="warning" %}
Use caution when holding an API key in a clipboard (copy / paste) and use caution with regard to key exposure when exchanging API keys with Ether. Consider clearing your chat history with Ether to reduce API key presence in chat history.
{% endhint %}

{% hint style="info" %}
By using Ether you agree that Ether will handle transferring your API key, messages, and / or files to OpenAI. Files you give Ether will undergo transformations for embedding. By using Ether you are also subject to OpenAI terms of service.
{% endhint %}

{% content-ref url="../terms-faq-help/ether-terms-and-privacy.md" %}
[ether-terms-and-privacy.md](../terms-faq-help/ether-terms-and-privacy.md)
{% endcontent-ref %}

***

## Getting Started

To begin with Ether, first initialize a session in a channel where you want Ether to chat.

```python
/manager [ session_management ] [ start ]
```

<details>

<summary>Start</summary>

_`/manager [ session_management ] [ start ]`_

Initialize a new session in the channel the command is being invoked in, Ether will send a direct message requesting an API key. The API key is validated for authenticity, then the session is initialized in the channel the command was invoked in.

</details>

<details>

<summary>View sessions </summary>

_`/manager [ session_management ] [ view_sessions ]`_

View all of your active sessions and their respective extensions, source channel, unique name, and session number.

</details>

<details>

<summary>Session configuration </summary>

_`/manager [ session_management } [ session_config ]`_

View the session configuration of the current session. Only works in the root session channel and not within session extensions.

</details>

<details>

<summary>Save session</summary>

_`/manager [ session_management } [ save_session ]`_

Save a session to Json, Ether will accumulate session variables applicable for storage - such as the chatbot configuration and OpenAI configuration. These items are sent to the session author in direct message as a Json, which can be used later to upload into a session.

Example json:

```
{"tokens": 2000, "context": 6, "model": "gpt-3.5-turbo", "size": "512x512", "number": 1, "sharedChat": true, "sharedImage": false, "sharedEmbed": false, "sharedVisual": false, "nicknames": "False", "role": [{"user_id": 775445008672489525, "user_role": "system", "prompt": "respond as a sassy and esoteric bluemoon goddess named Ether with less than 40 words."}], "frequency": 0, "presence": 0, "top_p": 0, "unique_name": "Chat", "temperature": 1.8, "image_model": "dalle3", "toggle_prompt": false}
```

</details>

<details>

<summary>Load session</summary>

_`/manager [ session_management ] [ load_session ]`_

Load a session configuration from json. Ether will send you a direct message requesting the json to apply to the session.

</details>

<details>

<summary>Load session defaults</summary>

`/manager [ session_management ] [ load_session_defaults ]`

Loads the session defaults for OpenAI and chatbot related options

</details>

<details>

<summary>Name a session</summary>

`/manager [ session_name ]`

Give a session a unique name that will be displayed for you when viewing sessions

</details>

<details>

<summary>Extend a session</summary>

`/manager [ extend_session ]`

Extends a session into an additional channel. First obtain the number for the session to extend either in session config or by viewing all sessions, then in new channel use extend session command with the session number to extend

</details>

<details>

<summary>Utilities</summary>

`/manager [ utilities ]`

* keep\_alive
  * enables sending dummy request every 6 hours to llmpredictor when having active embeddings
* jump\_listener
  * is designed to execute the session listener object in the event a Discord outage has de-registered bot listeners, while the user still has active sessions

</details>

<details>

<summary>Exit</summary>

_`/manager [ session_management } [ exit ]`_

Exit the current session, should be invoked in the channel of the active session to exit.

</details>

<details>

<summary>Exit all</summary>

_`/manager [ session_management } [ exit_all ]`_

Exit all of your active sessions.

</details>

{% hint style="info" %}
Whenever supplying Ether with an API key, or requesting to save or load a session configuration, Ether will send you a direct message for these exchanges. All saved sessions or other saved data is saved by the user and sent to the user as a file.&#x20;
{% endhint %}

### Keywords

> @ether _**draw**_, @ether _**variate**_, @ether _**embed**_, @ether _**set**_, @ether _**exit**_

{% tabs %}
{% tab title="Draw" %}
_`@ether draw`_

_`[ bot mention ] [ draw ] [ prompt ]`_

> The keyword draw will tell Ether to bundle your message content as the image prompt and parse the API request to the selected image model

Example:

> @ether draw a sunset in the horizon cresting over snow capped mountains
{% endtab %}

{% tab title="Variate" %}
_`@ether variate + attachment`_

_`[ bot mention ] [ variate ] [ attachment ]`_

> Using keyword variate along with message attachments will tell Ether to process your image attachments for, and to parse API with DALL E

Note:&#x20;

> as of 2.1.2024, variations are only available with DALL E 2
>
> variations are limited to a single image attachment
{% endtab %}

{% tab title="Embed" %}
_`@ether embed, OR, @ether embed + attachment`_

_`[ bot mention ] [ embed ] [ with or without attachment ]`_

> Mentioning Ether with keyword embed and without attachment prompts Ether to send you a direct message for a file or data exchange
>
> Mentioning Ether with keyword embed with an attachment in the session channel will initialize an embedding with the attachment without direct message exchange requirement

Note:

> As of 2.1.2024, Ether provides HTTP & HTTPS support when in direct message exchange
{% endtab %}

{% tab title="Set" %}
_`@ether set ....`_

_`[ bot mention ] [ set ] [ configuration description ]`_

> Using keyword set tells Ether you are attempting to alter your session configuration by message command. This will send your message to ChatGPT, then ChatGPT returns a json which is applied to your session configuration.

Note:

> If there are errors, the user may use slash command to repair the variable, reset the session, or apply a previous session configuration to repair, restore, or reset the session state.

Example:

> _@ether set the temperature to 0.8, context to 4, and the tokens to 500, with a prompt "you are a friendly assistant"_
{% endtab %}

{% tab title="Exit" %}
_`@ether exit`_

_`[ bot mention ] [ exit ]`_

> Only applicable while in an embedding, with keyword exit Ether will discard the embedding and begin routing messages back into normal text generative models instead of the predictor instance.
{% endtab %}
{% endtabs %}
