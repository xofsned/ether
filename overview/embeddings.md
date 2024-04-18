---
description: Embedding custom data into ChatGPT with Ether
---

# 📩 Embeddings

***

{% hint style="warning" %}
Data embedded into ChatGPT through Ether will go through transformations, batching, may be restricted in character limit, and parses in latin-1 or utf-8
{% endhint %}

{% hint style="warning" %}
Ether does not retain any files. Files are processed, embedded, and then disposed. The index is not generated to file or collected (2.1.2024). OpenAPI, as of (2.1.2024) will retain data for 30 days
{% endhint %}

{% hint style="danger" %}
Check embedding price differences on text generative models and choose wisely. For best cost efficiency use GPT 3.5-Turbo
{% endhint %}

{% content-ref url="../terms-faq-help/ether-terms-and-privacy.md" %}
[ether-terms-and-privacy.md](../terms-faq-help/ether-terms-and-privacy.md)
{% endcontent-ref %}

***

## Embedding Methods

_Keyword options..._

{% tabs %}
{% tab title="embed" %}
**@ether embed**

_`[ bot mention ] [ embed ]`_

> Ether will send a direct message requesting the files for embedding if there is no message attachment
{% endtab %}

{% tab title="embed + file" %}
**@ether embed + attachment**

_`[ bot mention ] [ embed ] [ attachment ]`_

> When passing an attachment with the message in the session channel, Ether will begin the embedding without exchange in direct message
{% endtab %}

{% tab title="only file" %}
**@ether + attachment + prompt**

_`[ bot mention ] [ attachment ] [ prompt ]`_

> Passing any supported file type to Ether with a message prompt will initialize a one-time pass embedding combined with the message prompt.&#x20;
>
> <mark style="color:yellow;">Data in one-time pass is limited to 20,000 characters, 5x the Discord message character limit</mark>
{% endtab %}

{% tab title="exit" %}
**@ether exit**

_`[ bot mention ] [ exit ]`_

> Using the keyword `exit` while in an embedded session will discard the predictor instance and detach from the embedded session entirely, chat will resume as normal text generative API requests
{% endtab %}
{% endtabs %}

### Supported Filetypes:

{% tabs %}
{% tab title="Documents" %}
* Doc
* Docx
* PDF
* Text
* EPUB
* ODT
* RTF
{% endtab %}

{% tab title="Datasets" %}
* CSV
* XLSX
* XLS
{% endtab %}

{% tab title="Programming Files" %}
* Python
* Javascript
* Rust
* Powershell
* Linux Shell
* C & C++
* Nim
* Lua
* HTML
* PHP
* CSS
{% endtab %}
{% endtabs %}



{% hint style="info" %}
Additionally, when using '@ether embed\` with no attachments, you may give Ether HTTP or HTTPS links. Ether will fetch the website data and embed it for you.&#x20;
{% endhint %}

{% hint style="info" %}
Ether's draw, variate, and GPT Visual utilities are accessible while in an embedded session
{% endhint %}
