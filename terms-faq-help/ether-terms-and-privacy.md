---
description: By using Ether you agree to and acknowledge the subjects below
---

# ✅ Ether terms & privacy

***

{% hint style="info" %}
The following terms apply 11/11/2024 reflecting the refactor from Ether v29\~ to a new v30 (min)
{% endhint %}

You acknowledge and agree to the following conditions:

* Ether will not store or redistribute information
* Ether no longer operates in the Cloud (see tip below)
* Ether is for free and fun AI use in Discord, there are no intentions to:
  * monitize Ether
  * collect user data
  * redistribute data
* Ether, while in operation, will store user id's to map the user's selected model and prompt when bundling the AI call
* Ether's AI is hosted by the developer, with the models used listed in `/ether-status`

{% hint style="info" %}
The terms below are depreciated as of 11/11/2024, per the removal of OpenAPI API support and LM Studio support. Please refer to the details above.
{% endhint %}

### You agree that Ether will relay your OpenAI key, messages, and provided files to OpenAI

> Ether is a toolkit / relay system using a class instance. In your initialized instance, your OpenAPI key is stored as a local temporary variable while the session is active. This looped session will process and send your OpenAI API key, your message for ChatGPT, and files you choose to embed to OpenAI.

> Ether does not retain any files or messages. Ether does not retain an OpenAI key as a variable outside of an active session. When a session has been terminated, all variables are destroyed.

### You agree that your files will be transformed and processed for embedding

> Files given to Ether are processed and batched into a raw text format suitable for embedding. Ether is not responsible for copyright management, and should not be used to infringe on copyright. The user acknowledges that the transformation of copyrighted data or the redistribution of copyrighted data through AI is also considered copyright infringement.&#x20;

### You are also subject to OpenAI terms of service

> Ether should not be used for, and is not built for, circumventing OpenAI's terms of service. Ether should not be used in anyway to abuse OpenAI's API. In using Ether, you acknowledge that OpenAI will associate your usage with your organization, and any users you share sessions with can impact your account. Ether is in no way responsible for the termination of user accounts who abuse OpenAI API or OpenAI's services using Ether.

> Additionally, Ether is built to offer only the same options that OpenAI offers. Ether will never operate outside of the expected API use cases or OpenAI API terms of service.

### You acknowledge that Ether operates in the Google Cloud

> Ether as an application operates in a Debian Linux instance in a Google Cloud Compute Instance. This instance is minimal and hardened with additional security systems.
>
> * Malware protection & routine malware scans
> * Intrusion detection and routine audits
> * Google DDOS protection
> * Google incident event detection and logging
> * TLS and SSL

### Ether's Built-in AI Chat

> Ether's built-in chat is hosted and supported by Ether's developer using AI models from HuggingFace. No Discord user information is generated, collected, or redistributed. No additional information is stored or needed for this service. Ether will respond to any user who does not have a session and in channels where there are no shared sessions - by ping or reply only (user requested interaction).
>
> Ether parses API requests to LM Studio through a domain web server service hosting TLS and certificates, with an API endpoint protected by firewalls and security protocols as is the bot itself on the Google cloud.
>
> Models hosted in Ether and their status can be viewed in the command /ether.
